# from fastapi import FastAPI, HTTPException, Query
# from typing import List, Optional
# from Bio import Entrez
# from Bio import SeqIO
# from pymongo import MongoClient
# from fastapi.middleware.cors import CORSMiddleware
# import logging
# import time
# import uvicorn
# import traceback
# from Bio.Entrez import Parser
# from Bio.Entrez.Parser import StringElement

# # Configure email for NCBI API
# Entrez.email = "abdullah.1970333@studenti.uniroma1.it"
# MONGO_URI = "mongodb+srv://admin2:Cloud786@clusterfull.tn88z.mongodb.net/taxonomy"

# # Initialize the client and database
# try:
#     client = MongoClient(MONGO_URI)
#     db = client.taxonomy
#     print("Connected to MongoDB successfully!")
#     print("Databases:", client.list_database_names())
# except Exception as e:
#     print("Error connecting to MongoDB:", e)
#     raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")

# # Create FastAPI app
# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running"}

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins; use specific domains in production
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# def fetch_metadata(database, uid):
#     # Check MongoDB cache first
#     cached_data = db.metadata.find_one({"database": database, "accession": uid})
#     if cached_data:
#         logging.info(f"Cache hit for UID: {uid}")
#         cached_data["_id"] = str(cached_data["_id"])
#         return cached_data

#     try:
#         logging.info(f"Fetching {database} data for UID: {uid}")
#         time.sleep(1)  # Add a delay to avoid rate limits
#         handle = Entrez.efetch(db=database, id=uid, rettype="gb", retmode="text")
#         # record = SeqIO.read(handle, "genbank")
#         records = list(SeqIO.parse(handle, "genbank"))
#         if not records:
#             raise HTTPException(status_code=404, detail="No records found")
#         record = records[0]  # Pick the first record
#         handle.close()

#         # Extract metadata (customize this for each database)
#         metadata = {
#             "database": database,
#             "accession": record.id,
#             "organism": record.annotations.get("organism", "Unknown"),
#             "definition": record.description,
#             "length": len(record.seq),
#             "updated_date": record.annotations.get("date", "Unknown"),
#             "genes": [
#                 feature.qualifiers.get("gene", ["Unknown"])[0]
#                 for feature in record.features if feature.type == "gene"
#             ],
#             "features": [
#                 {
#                     "type": feature.type,
#                     "location": str(feature.location),
#                     "qualifiers": {key: ", ".join(val) if isinstance(val, list) else val for key, val in feature.qualifiers.items()}
#                 }
#                 for feature in record.features
#             ],
#             "references": [
#                 {
#                     "title": reference.title,
#                     "authors": ", ".join(reference.authors) if hasattr(reference, "authors") else "Unknown",
#                     "journal": reference.journal
#                 }
#                 for reference in record.annotations.get("references", [])
#             ],
#             "source": record.annotations.get("source", "Unknown"),
#         }

#         # Save to MongoDB cache
#         result = db.metadata.insert_one(metadata)
#         metadata["_id"] = str(result.inserted_id)  # Convert ObjectId to string
#         logging.info(f"Saved metadata for UID {uid} to MongoDB cache")

#         return metadata

#     except Exception as e:
#         logging.error(f"Error fetching/parsing data for UID {uid}: {e}")
#         return None

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the NCBI Database Search API!"}


# @app.get("/search/")
# async def search_nucleotide(
#     database: str = Query(..., description="NCBI database to search (e.g., nucleotide, assembly, bioproject)"),
#     query: Optional[str] = None,
#     accession_ids: Optional[List[str]] = Query(None),
#     taxid: Optional[int] = None,
#     organism: Optional[str] = None,
#     gene: Optional[str] = None,
#     protein: Optional[str] = None,
#     min_length: Optional[int] = None,
#     max_length: Optional[int] = None,
#     molecule_type: Optional[str] = None,
#     publication_date: Optional[str] = None,
#     retmax: int = 10,
# ):
#     """
#     Endpoint to search for sequences or metadata in a specified NCBI database.
#     """
#     try:
#         # Validate query
#         if not (query or accession_ids or taxid):
#             raise HTTPException(status_code=400, detail="No query provided")

#         # Construct search terms
#         search_terms = []

#         # Ensure only one organism filter is applied
#         if taxid and organism:
#             logging.warning("Both taxid and organism provided. Using only organism.")
#         if taxid and not organism:
#             search_terms.append(f"txid{taxid}[Organism]")
#         elif organism:
#             search_terms.append(f'"{organism}"[Organism]')

#         # Only apply Accession ID if it exists and does not conflict
#         if accession_ids:
#             search_terms.append(f"({' OR '.join(accession_ids)})[Accession]")

#         # Only apply Gene filter if it is a valid gene name
#         if gene:
#             search_terms.append(f'"{gene}"[Gene]')

#         if protein:
#             search_terms.append(f'"{protein}"[Protein]')    

#         if min_length or max_length:
#             length_query = f"{min_length or 0}:{max_length or 100000000}[SLEN]"
#             search_terms.append(length_query)

#         if molecule_type:
#             search_terms.append(f'"{molecule_type}"[Molecule Type]')

#         if publication_date:
#             search_terms.append(f'"{publication_date}"[Publication Date]')

#         # Construct final query string
#         search_query = " AND ".join(search_terms)
#         logging.info(f"Constructed search query: {search_query}")

#         # Perform NCBI search
#         handle = Entrez.esearch(db=database, term=search_query, retmax=retmax, retmode="xml")
#         search_results = Entrez.read(handle)
#         handle.close()

#         logging.info(f"Search results: {search_results}")

#         # Check if results were found
#         if not search_results["IdList"]:
#             return {
#                 "query": search_query,
#                 "metadata": [],
#                 "failed_uids": [],
#             }

#         # Fetch metadata for each UID
#         metadata = []
#         failed_uids = []
#         for uid in search_results["IdList"]:
#             data = fetch_metadata(database, uid)  # Pass the database parameter
#             if data:
#                 metadata.append(data)
#             else:
#                 failed_uids.append(uid)

#         # Log and return results
#         logging.info(f"Final metadata: {metadata}")
#         if failed_uids:
#             logging.warning(f"Failed to fetch data for UIDs: {failed_uids}")

#         return {
#             "query": search_query,
#             "metadata": metadata,
#             "failed_uids": failed_uids,
#         }

#     except Exception as e:
#         logging.error(f"Error in /search endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))




# New Code   #######


# from fastapi import FastAPI, HTTPException, Query
# from typing import List, Optional
# from Bio import Entrez
# from Bio import SeqIO
# from pymongo import MongoClient
# from fastapi.middleware.cors import CORSMiddleware
# import logging
# import time
# import uvicorn
# import traceback
# import httpx
# from datetime import datetime
# from Bio.Entrez import Parser
# from Bio.Entrez.Parser import StringElement

# # Configure email for NCBI API
# Entrez.email = "abdullah.1970333@studenti.uniroma1.it"
# MONGO_URI = "mongodb+srv://admin2:Cloud786@clusterfull.tn88z.mongodb.net/taxonomy"

# # Initialize the client and database
# try:
#     client = MongoClient(MONGO_URI)
#     db = client.taxonomy
#     print("Connected to MongoDB successfully!")
#     print("Databases:", client.list_database_names())
# except Exception as e:
#     print("Error connecting to MongoDB:", e)
#     raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")

# # Create FastAPI app
# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# def fetch_nucleotide_metadata(uid):
#     """Fetch metadata for nucleotide records"""
#     try:
#         logging.info(f"Fetching nucleotide data for UID: {uid}")
#         time.sleep(1)  # Add a delay to avoid rate limits
#         handle = Entrez.efetch(db="nucleotide", id=uid, rettype="gb", retmode="text")
#         records = list(SeqIO.parse(handle, "genbank"))
#         if not records:
#             raise HTTPException(status_code=404, detail="No records found")
#         record = records[0]
#         handle.close()

#         metadata = {
#             "database": "nucleotide",
#             "accession": record.id,
#             "organism": record.annotations.get("organism", "Unknown"),
#             "definition": record.description,
#             "length": len(record.seq),
#             "updated_date": record.annotations.get("date", "Unknown"),
#             "genes": [
#                 feature.qualifiers.get("gene", ["Unknown"])[0]
#                 for feature in record.features if feature.type == "gene"
#             ],
#             "features": [
#                 {
#                     "type": feature.type,
#                     "location": str(feature.location),
#                     "qualifiers": {key: ", ".join(val) if isinstance(val, list) else val for key, val in feature.qualifiers.items()}
#                 }
#                 for feature in record.features
#             ],
#             "references": [
#                 {
#                     "title": reference.title,
#                     "authors": ", ".join(reference.authors) if hasattr(reference, "authors") else "Unknown",
#                     "journal": reference.journal
#                 }
#                 for reference in record.annotations.get("references", [])
#             ],
#             "source": record.annotations.get("source", "Unknown"),
#         }

#         return metadata

#     except Exception as e:
#         logging.error(f"Error fetching nucleotide data for UID {uid}: {e}")
#         return None

# # Add at the start of your search_ncbi function

# async def fetch_assembly_metadata(accession):
#     """Fetch metadata for assembly records using NCBI Datasets API"""
#     try:
#         # Validate accession format first
#         if not (accession.startswith('GCA_') or accession.startswith('GCF_')):
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid accession format. Must start with GCA_ or GCF_"
#             )

#         # Check MongoDB cache first
#         cached_data = db.assemblies.find_one({"accession": accession}, {"_id": 0})  # Exclude MongoDB's _id field
#         if cached_data:
#             logging.info(f"Cache hit for assembly: {accession}")
#             cached_data["_id"] = str(cached_data["_id"])
#             return cached_data

#         async with httpx.AsyncClient() as client:
#             # Try both v2alpha and v1 endpoints as fallback
#             endpoints = [
#                 f"https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{accession}/metadata",
#                 f"https://api.ncbi.nlm.nih.gov/datasets/v1/genome/accession/{accession}/metadata"
#             ]
            
#             last_error = None
#             metadata = None
            
#             for endpoint in endpoints:
#                 try:
#                     response = await client.get(
#                         endpoint,
#                         params={"filters.refseq_only": "false"},
#                         headers={"Accept": "application/json"},
#                         timeout=10.0
#                     )
                    
#                     if response.status_code == 404:
#                         continue  # Try next endpoint
                        
#                     response.raise_for_status()
#                     data = response.json()
                    
#                     if "assemblies" not in data or not data["assemblies"]:
#                         continue  # Try next endpoint
                        
#                     assembly = data["assemblies"][0]["assembly"]
#                     metadata = format_assembly_metadata(assembly)
#                     break
                    
#                 except httpx.HTTPStatusError as e:
#                     last_error = e
#                     continue
#                 except Exception as e:
#                     last_error = e
#                     continue

#             if not metadata:
#                 error_msg = f"Assembly {accession} not found in NCBI databases"
#                 if last_error:
#                     error_msg += f" (Error: {str(last_error)})"
#                 raise HTTPException(status_code=404, detail=error_msg)

#             # Save to MongoDB cache
#             result = db.assemblies.insert_one(metadata)
#             metadata["_id"] = str(result.inserted_id)
#             logging.info(f"Saved assembly metadata for {accession} to MongoDB")

#             return metadata

#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Error fetching assembly data for {accession}: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to fetch assembly data: {str(e)}"
#         )

# def format_assembly_metadata(assembly_data):
#     """Standardize the assembly metadata format"""
#     return {
#         "database": "assembly",
#         "accession": assembly_data.get("assembly_accession"),
#         "assembly_name": assembly_data.get("assembly_name"),
#         "organism": {
#             "sci_name": assembly_data["org"].get("sci_name"),
#             "common_name": assembly_data["org"].get("common_name"),
#             "tax_id": assembly_data["org"].get("tax_id")
#         },
#         "submission_date": assembly_data.get("submission_date"),
#         "submitter_org": assembly_data.get("submitter_org"),
#         "assembly_level": assembly_data.get("assembly_level"),
#         "contig_n50": assembly_data.get("contig_n50"),
#         "scaffold_n50": assembly_data.get("scaffold_n50"),
#         "number_of_contigs": assembly_data.get("number_of_contigs"),
#         "chromosomes": assembly_data.get("chromosomes"),
#         "ftp_path": assembly_data.get("ftp_path"),
#         "annotation_metadata": assembly_data.get("annotation_metadata"),
#         "last_updated": datetime.utcnow()
#     }

# def fetch_metadata(database, uid):
#     """Router function to fetch metadata based on database type"""
#     if database == "assembly":
#         # For assembly, we need to use the async function
#         # This will be handled separately in the search endpoint
#         return None
#     elif database == "nucleotide":
#         return fetch_nucleotide_metadata(uid)
#     else:
#         # Add other database types here as needed
#         return None

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the NCBI Database Search API!"}

# @app.get("/search/")
# async def search_ncbi(
#     database: str = Query(..., description="NCBI database to search (e.g., nucleotide, assembly)"),
#     query: Optional[str] = None,
#     accession_ids: Optional[List[str]] = Query(None),
#     taxid: Optional[int] = None,
#     organism: Optional[str] = None,
#     gene: Optional[str] = None,
#     protein: Optional[str] = None,
#     min_length: Optional[int] = None,
#     max_length: Optional[int] = None,
#     molecule_type: Optional[str] = None,
#     publication_date: Optional[str] = None,
#     retmax: int = 10,
# ):
#     """
#     Enhanced endpoint to search both nucleotide and assembly databases
#     """
#     try:
#         # Validate input
#         if not (query or accession_ids or taxid or organism):
#             raise HTTPException(status_code=400, detail="No search criteria provided")

#         # Handle assembly searches differently
#         if database == "assembly":
#             if not accession_ids:
#                 raise HTTPException(status_code=400, detail="Assembly searches require accession numbers")
            
#             metadata = []
#             failed_accessions = []
            
#             for accession in accession_ids:
#                 try:
#                     assembly_data = await fetch_assembly_metadata(accession)
#                     metadata.append(assembly_data)
#                 except Exception as e:
#                     logging.error(f"Failed to fetch assembly {accession}: {e}")
#                     failed_accessions.append(accession)
            
#             return {
#                 "query": f"Assembly accessions: {', '.join(accession_ids)}",
#                 "metadata": metadata,
#                 "failed_accessions": failed_accessions,
#             }

#         # For nucleotide and other standard databases
#         search_terms = []

#         if taxid and organism:
#             logging.warning("Both taxid and organism provided. Using only organism.")
        
#         if taxid and not organism:
#             search_terms.append(f"txid{taxid}[Organism]")
#         elif organism:
#             search_terms.append(f'"{organism}"[Organism]')

#         if accession_ids:
#             search_terms.append(f"({' OR '.join(accession_ids)})[Accession]")

#         if gene:
#             search_terms.append(f'"{gene}"[Gene]')

#         if protein:
#             search_terms.append(f'"{protein}"[Protein]')    

#         if min_length or max_length:
#             length_query = f"{min_length or 0}:{max_length or 100000000}[SLEN]"
#             search_terms.append(length_query)

#         if molecule_type:
#             search_terms.append(f'"{molecule_type}"[Molecule Type]')

#         if publication_date:
#             search_terms.append(f'"{publication_date}"[Publication Date]')

#         # Construct final query string
#         search_query = " AND ".join(search_terms)
#         logging.info(f"Constructed search query: {search_query}")

#         # Perform NCBI search
#         handle = Entrez.esearch(db=database, term=search_query, retmax=retmax, retmode="xml")
#         search_results = Entrez.read(handle)
#         handle.close()

#         if not search_results["IdList"]:
#             return {
#                 "query": search_query,
#                 "metadata": [],
#                 "failed_uids": [],
#             }

#         # Fetch metadata for each UID
#         metadata = []
#         failed_uids = []
#         for uid in search_results["IdList"]:
#             data = fetch_metadata(database, uid)
#             if data:
#                 metadata.append(data)
#             else:
#                 failed_uids.append(uid)

#         return {
#             "query": search_query,
#             "metadata": metadata,
#             "failed_uids": failed_uids,
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Error in /search endpoint: {str(e)}\n{traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=str(e))






#                     ### Code for Genome Database


# def search_ncbi(database: str, query: str, retmax: int = 10):
#     """
#     Searches the NCBI database and returns metadata.
#     """
#     try:
#         logging.info(f"Searching {database} for query: {query}")

#         # Convert organism name to TaxID for assembly searches
#         if database == "assembly":
#             query = f"txid{query}[Organism]"

#         # Perform search
#         handle = Entrez.esearch(db=database, term=query, retmax=retmax, retmode="xml")
#         search_results = Entrez.read(handle)
#         handle.close()

#         # Get list of IDs
#         id_list = search_results.get("IdList", [])
#         if not id_list:
#             return {"query": query, "database": database, "results": []}

#         metadata = []
#         for uid in id_list:
#             time.sleep(1)  # Avoid rate limiting
#             handle = Entrez.efetch(db=database, id=uid, rettype="gb", retmode="text")
#             record = handle.read()
#             handle.close()
#             metadata.append({"uid": uid, "data": record})

#         return {"query": query, "database": database, "results": metadata}

#     except Exception as e:
#         logging.error(f"Error fetching data: {e}")
#         return None

# # Simulated NCBI API call (replace this with real request)
# def fake_ncbi_api_call(database, query):
#     if database == "assembly" and query.lower() == "salamandra":
#         return {"id": 12345, "name": "Salamandra Assembly"}
#     raise Exception("NCBI API rejected the request")



#                     ### Code for Genome Database



# # def validate_accession(database, accession):
# #     """
# #     Validate if the accession number matches the selected database.
# #     """
# #     if database == "nucleotide" and accession.startswith(("NM_", "NC_", "NG_", "NT_", "NW_", "NZ_")):
# #         return True
# #     elif database == "assembly" and accession.startswith(("GCA_", "GCF_")):
# #         return True
# #     elif database == "biosample" and accession.startswith(("SAMN", "SAME")):
# #         return True
# #     elif database == "bioproject" and accession.startswith(("PRJNA", "PRJEB")):
# #         return True
# #     elif database == "gene" and accession.isdigit():
# #         return True
# #     elif database == "taxonomy" and accession.isdigit():
# #         return True
# #     else:
# #         return False


# def fetch_assembly_metadata(accession):
#     """
#     Fetch metadata for a given assembly accession from the NCBI Assembly database.
#     """
#     try:
#         logging.info(f"Fetching assembly data for accession: {accession}")
#         time.sleep(1)  # Add a delay to avoid rate limits

#         # First, search for the UID using esearch
#         handle = Entrez.esearch(db="assembly", term=accession, retmode="xml")
#         record = Entrez.read(handle, validate=False)  # Add validate=False
#         handle.close()
        
#         uid_list = record.get("IdList", [])
#         if not uid_list:
#             raise HTTPException(status_code=404, detail=f"No UID found for accession {accession}")
        
#         uid = uid_list[0]  # Take the first UID

#         # Fetch the assembly metadata using esummary
#         handle = Entrez.esummary(db="assembly", id=uid, retmode="xml")
#         record = Entrez.read(handle, validate=False)  # Add validate=False
#         handle.close()

#         # Check if record contains valid data
#         if "DocumentSummarySet" not in record or "DocumentSummary" not in record["DocumentSummarySet"]:
#             raise HTTPException(status_code=500, detail="Unexpected NCBI response format.")

#         summary = record["DocumentSummarySet"]["DocumentSummary"][0]  # First summary entry

#         metadata = {
#             "database": "assembly",
#             "accession": summary.get("AssemblyAccession", "Unknown"),
#             "organism": summary.get("SpeciesName", "Unknown"),
#             "assembly_name": summary.get("AssemblyName", "Unknown"),
#             "submitter": summary.get("SubmitterOrganization", "Unknown"),
#             "biosample": summary.get("BioSampleAccn", "Unknown"),
#             "assembly_level": summary.get("AssemblyStatus", "Unknown"),
#             "genome_size": int(summary.get("Meta", {}).get("GenomeLength", 0)),
#             "contig_count": int(summary.get("Meta", {}).get("ContigN50", 0)),
#             "gc_percent": float(summary.get("Meta", {}).get("GCPercent", 0.0)),
#             "submission_date": summary.get("SubmissionDate", "Unknown"),
#             "update_date": summary.get("LastUpdateDate", "Unknown"),
#             "related_projects": summary.get("BioProjectAccn", "Unknown"),
#             "ftp_url": summary.get("FtpPath_GenBank", "Unknown"),
#         }

#         logging.info(f"Fetched metadata for accession {accession}")
#         return metadata

#     except Exception as e:
#         logging.error(f"Error fetching assembly metadata for accession {accession}: {e}")
#         raise HTTPException(status_code=500, detail=f"NCBI fetch error: {str(e)}")

# def fetch_assembly_metadata(accession):
#     """
#     Fetch metadata for a given assembly accession from the NCBI Assembly database.
#     Returns all available metadata dynamically.
#     """
#     try:
#         logging.info(f"Fetching assembly data for accession: {accession}")
#         time.sleep(1)  # Avoid rate limits

#         # Step 1: Search for the UID using esearch
#         handle = Entrez.esearch(db="assembly", term=accession, retmode="xml")
#         record = Entrez.read(handle, validate=False)
#         handle.close()
        
#         uid_list = record.get("IdList", [])
#         if not uid_list:
#             raise HTTPException(status_code=404, detail=f"No UID found for accession {accession}")
        
#         uid = uid_list[0]  # Take the first UID

#         # Step 2: Fetch the assembly metadata using esummary
#         handle = Entrez.esummary(db="assembly", id=uid, retmode="xml")
#         record = Entrez.read(handle, validate=False)
#         handle.close()

#         # Debug print the full response
#         print(f"🔍 Full Response from NCBI: {record}")

#         # Validate response structure
#         if "DocumentSummarySet" not in record or not isinstance(record["DocumentSummarySet"], dict):
#             raise HTTPException(status_code=500, detail="Unexpected NCBI response format: Missing 'DocumentSummarySet'.")

#         doc_summary = record["DocumentSummarySet"].get("DocumentSummary", [])

#         if not isinstance(doc_summary, list) or not doc_summary:
#             raise HTTPException(status_code=500, detail="Unexpected NCBI response format: 'DocumentSummary' is missing or invalid.")

#         summary = doc_summary[0]  # Take the first summary entry

#         # 🔍 Ensure the summary is a dictionary
#         if isinstance(summary, StringElement):
#             summary = str(summary)  # Convert to string if necessary

#         if not isinstance(summary, dict):
#             raise HTTPException(status_code=500, detail=f"Unexpected summary type: {type(summary)}")

#         # ✅ Instead of extracting specific fields, return everything dynamically
#         return summary  # Return full metadata

#     except Exception as e:
#         logging.error(f"Error fetching assembly metadata for accession {accession}: {e}")
#         raise HTTPException(status_code=500, detail=f"NCBI fetch error: {str(e)}")



# @app.get("/search/")
# async def search_ncbi(
#     database: str = Query(..., description="NCBI database to search (e.g., nucleotide, assembly)"),
#     query: Optional[str] = None,
#     accession_ids: Optional[List[str]] = Query(None),
#     taxid: Optional[int] = None,
#     min_length: Optional[int] = None,
#     max_length: Optional[int] = None,
# ):
#     """
#     Endpoint to search for sequences or metadata in a specified NCBI database.
#     """
#     try:
#         # Validate query
#         if not (query or accession_ids or taxid):
#             raise HTTPException(status_code=400, detail="No query provided")

#         # Fetch metadata for each accession ID
#         metadata = []
#         failed_uids = []
#         if accession_ids:
#             for uid in accession_ids:
#                 print(f"Processing UID: {uid}")  # Debugging print

#                 # Validate accession number
#                 if not validate_accession(database, uid):
#                     failed_uids.append(uid)
#                     print(f"❌ Invalid accession: {uid}")  # Debugging print
#                     continue

#                 print(f"✅ Valid accession: {uid}, fetching metadata...")  # Debugging print

#                 if database == "assembly":
#                     try:
#                         data = fetch_assembly_metadata(uid)
#                         print(f"📜 Assembly metadata: {data}")  # Debugging print
#                     except Exception as e:
#                         print(f"🚨 Error fetching assembly metadata for {uid}: {e}")  # Debugging print
#                         failed_uids.append(uid)
#                     continue
#                 else:
#                     data = fetch_metadata(database, uid)

#                 if data:
#                     metadata.append(data)
#                 else:
#                     failed_uids.append(uid)
#                 return {
#                    "query": query,
#                    "metadata": metadata,
#                    "failed_uids": failed_uids,
#         }

#     except Exception as e:
#         logging.error(f"Error in /search endpoint: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

                    ### Code for Genome Database


# def fetch_assembly_metadata(accession):
#     """
#     Fetch metadata for a given assembly accession from the NCBI Assembly database.
#     Returns structured metadata in a consistent format.
#     """
#     try:
#         logging.info(f"Fetching assembly data for accession: {accession}")
#         time.sleep(1)  # Avoid rate limits

#         # Step 1: Search for the UID using esearch
#         # handle = Entrez.esearch(db="assembly", term=accession, retmode="xml")
#         # record = Entrez.read(handle, validate=False)
#         # handle.close()
        
#         handle = Entrez.esearch(db="assembly", term=accession+"[Accession]", retmode="xml")
#         record = Entrez.read(handle)
#         handle.close()

#         if not record.get("IdList"):
#             # If no results, try genome database
#             handle = Entrez.esearch(db="genome", term=accession+"[Accession]", retmode="xml")
#             record = Entrez.read(handle)
#             handle.close()
        
#         uid_list = record.get("IdList", [])
#         if not uid_list:
#             raise HTTPException(status_code=404, detail=f"No UID found for accession {accession}")
        
#         uid = uid_list[0]  # Take the first UID

#         # Step 2: Fetch the assembly metadata using esummary
#         handle = Entrez.esummary(db="assembly", id=uid, retmode="xml")
#         record = Entrez.read(handle, validate=False)
#         handle.close()

#         # Validate response structure
#         if "DocumentSummarySet" not in record:
#             raise HTTPException(status_code=500, detail="Unexpected NCBI response format")

#         doc_summary = record["DocumentSummarySet"].get("DocumentSummary", [])
#         if not doc_summary:
#             raise HTTPException(status_code=500, detail="No document summary found")

#         summary = doc_summary[0]

#         # Convert to dict if it's a StringElement
#         if hasattr(summary, 'items'):  # Already a dict-like object
#             summary = dict(summary.items())
#         else:
#             summary = {"raw_data": str(summary)}

#         # Extract key fields with fallbacks
#         metadata = {
#             "database": "assembly",
#             "accession": summary.get("AssemblyAccession", "Unknown"),
#             "organism": summary.get("SpeciesName", "Unknown"),
#             "assembly_name": summary.get("AssemblyName", "Unknown"),
#             "submitter": summary.get("SubmitterOrganization", "Unknown"),
#             "biosample": summary.get("BioSampleAccn", "Unknown"),
#             "assembly_level": summary.get("AssemblyStatus", "Unknown"),
#             "genome_size": int(summary.get("Meta", {}).get("GenomeLength", 0)),
#             "contig_count": int(summary.get("Meta", {}).get("ContigN50", 0)),
#             "gc_percent": float(summary.get("Meta", {}).get("GCPercent", 0.0)),
#             "submission_date": summary.get("SubmissionDate", "Unknown"),
#             "update_date": summary.get("LastUpdateDate", "Unknown"),
#             "related_projects": summary.get("BioProjectAccn", "Unknown"),
#             "ftp_url": summary.get("FtpPath_GenBank", "Unknown"),
#             # Include all additional fields
#             "additional_metadata": {k: v for k, v in summary.items() 
#                                   if k not in ["AssemblyAccession", "SpeciesName", 
#                                               "AssemblyName", "SubmitterOrganization",
#                                               "BioSampleAccn", "AssemblyStatus",
#                                               "Meta", "SubmissionDate", 
#                                               "LastUpdateDate", "BioProjectAccn",
#                                               "FtpPath_GenBank"]}
#         }

#         return metadata

#     except HTTPException:
#         raise  # Re-raise existing HTTP exceptions
#     except Exception as e:
#         logging.error(f"Error fetching assembly metadata: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {str(e)}")

# @app.get("/search/")
# async def search_ncbi(
#     database: str = Query(..., description="NCBI database to search"),
#     query: Optional[str] = None,
#     accession_ids: Optional[List[str]] = Query(None),
#     taxid: Optional[int] = None,
#     min_length: Optional[int] = None,
#     max_length: Optional[int] = None,
# ):
#     """
#     Endpoint to search for sequences or metadata in NCBI databases.
#     """
#     try:
#         if not (query or accession_ids or taxid):
#             raise HTTPException(status_code=400, detail="No query provided")

#         metadata = []
#         failed_uids = []
        
#         if accession_ids:
#             for uid in accession_ids:
#                 try:
#                     if database == "assembly":
#                         data = fetch_assembly_metadata(uid)
#                     else:
#                         data = fetch_metadata(database, uid)
                    
#                     if data:
#                         metadata.append(data)
#                     else:
#                         failed_uids.append(uid)
#                 except HTTPException as e:
#                     failed_uids.append(uid)
#                     logging.warning(f"Failed to fetch {uid}: {e.detail}")
#                 except Exception as e:
#                     failed_uids.append(uid)
#                     logging.error(f"Unexpected error with {uid}: {str(e)}")

#         return {
#             "query": query,
#             "metadata": metadata,
#             "failed_uids": failed_uids,
#         }

#     except Exception as e:
#         logging.error(f"Search error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")





# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8080)  # Change host and port here




from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from Bio import Entrez
from Bio import SeqIO
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import uvicorn
import traceback
import httpx
from datetime import datetime
from Bio.Entrez import Parser
from Bio.Entrez.Parser import StringElement
import json
import asyncio

# Configure email for NCBI API
Entrez.email = "abdullah.1970333@studenti.uniroma1.it"
MONGO_URI = "mongodb+srv://admin2:Cloud786@clusterfull.tn88z.mongodb.net/taxonomy"

# Initialize the client and database
try:
    client = MongoClient(MONGO_URI)
    db = client.taxonomy
    print("Connected to MongoDB successfully!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print("Error connecting to MongoDB:", e)
    raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)

async def check_cache(database: str, identifier: str):
    """Check MongoDB cache for existing metadata"""
    try:
        cached_data = db.metadata.find_one({"database": database, "accession": identifier})
        if cached_data:
            cached_data["_id"] = str(cached_data["_id"])
            logging.info(f"Cache hit for {database} {identifier}")
            return cached_data
        return None
    except Exception as e:
        logging.error(f"Error checking cache: {e}")
        return None

async def save_to_cache(metadata: dict):
    """Save metadata to MongoDB cache"""
    try:
        result = db.metadata.insert_one(metadata)
        metadata["_id"] = str(result.inserted_id)
        logging.info(f"Saved metadata for {metadata['database']} {metadata['accession']} to cache")
        return metadata
    except Exception as e:
        logging.error(f"Error saving to cache: {e}")
        return metadata  # Return metadata even if caching fails

async def fetch_nucleotide_metadata(uid: str):
    """Fetch metadata for nucleotide records with caching"""
    try:
        # Check cache first
        cached_data = await check_cache("nucleotide", uid)
        if cached_data:
            return cached_data

        logging.info(f"Fetching nucleotide data for UID: {uid}")
        await asyncio.sleep(1)  # Add a delay to avoid rate limits
        
        handle = Entrez.efetch(db="nucleotide", id=uid, rettype="gb", retmode="text")
        records = list(SeqIO.parse(handle, "genbank"))
        if not records:
            raise HTTPException(status_code=404, detail="No records found")
        record = records[0]
        handle.close()

        metadata = {
            "database": "nucleotide",
            "accession": record.id,
            "organism": record.annotations.get("organism", "Unknown"),
            "definition": record.description,
            "length": len(record.seq),
            "updated_date": record.annotations.get("date", "Unknown"),
            "genes": [
                feature.qualifiers.get("gene", ["Unknown"])[0]
                for feature in record.features if feature.type == "gene"
            ],
            "features": [
                {
                    "type": feature.type,
                    "location": str(feature.location),
                    "qualifiers": {key: ", ".join(val) if isinstance(val, list) else val for key, val in feature.qualifiers.items()}
                }
                for feature in record.features
            ],
            "references": [
                {
                    "title": reference.title,
                    "authors": ", ".join(reference.authors) if hasattr(reference, "authors") else "Unknown",
                    "journal": reference.journal
                }
                for reference in record.annotations.get("references", [])
            ],
            "source": record.annotations.get("source", "Unknown"),
        }

        # Save to cache
        return await save_to_cache(metadata)

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching nucleotide data for UID {uid}: {e}")
        return None

def format_assembly_metadata(api_data, accession):
    """Handle RefSeq and GenBank response formats from /genome/accession/ endpoint"""
    try:
        # Extract 'assembly' from the correct nested location
        if "assemblies" in api_data and api_data["assemblies"]:
            assembly = api_data["assemblies"][0].get("assembly", {})
            org = assembly.get("org", {})
            return {
                "database": "assembly",
                "accession": accession,
                "organism": {
                    "sci_name": org.get('sci_name', 'Unknown'),
                    "common_name": org.get('common_name', 'Unknown'),
                    "tax_id": org.get('tax_id')
                },
                "assembly_name": assembly.get('display_name', 'N/A'),
                "assembly_level": assembly.get('assembly_category', 'N/A'),
                "submission_date": assembly.get('submission_date', 'N/A'),
                "ftp_path": assembly.get('ftp_path', ''),
                "last_updated": datetime.utcnow().isoformat()
            }

        # fallback if somehow no assemblies were returned
        logging.warning(f"No valid 'assemblies' found in API data for {accession}")
        return {
            "database": "assembly",
            "accession": accession,
            "organism": {"sci_name": "Unknown"},
            "assembly_name": "N/A",
            "assembly_level": "N/A",
            "submission_date": "N/A",
            "ftp_path": "",
            "last_updated": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logging.error(f"Formatting error for {accession}: {str(e)}")
        return {
            "database": "assembly",
            "accession": accession,
            "organism": {"sci_name": "Unknown"},
            "assembly_name": "N/A",
            "assembly_level": "N/A",
            "submission_date": "N/A",
            "ftp_path": "",
            "last_updated": datetime.utcnow().isoformat()
        }

async def fetch_via_entrez(accession):
    """Entrez fallback for assembly data with better error handling"""
    try:
        handle = Entrez.esearch(db="assembly", term=f"{accession}[Accession]", retmax=1)
        search_results = Entrez.read(handle)
        handle.close()
        
        if not search_results["IdList"]:
            raise HTTPException(status_code=404, detail="Assembly not found in Entrez")
        
        handle = Entrez.esummary(db="assembly", id=search_results["IdList"][0])
        summary = Entrez.read(handle)
        handle.close()
        
        return {
            "database": "assembly",
            "accession": accession,
            "organism": {
                "sci_name": summary["DocumentSummarySet"]["DocumentSummary"][0]["SpeciesName"],
                "tax_id": int(summary["DocumentSummarySet"]["DocumentSummary"][0]["Taxid"])
            },
            "assembly_name": summary["DocumentSummarySet"]["DocumentSummary"][0]["AssemblyName"],
            "assembly_level": summary["DocumentSummarySet"]["DocumentSummary"][0]["AssemblyStatus"],
            "submission_date": summary["DocumentSummarySet"]["DocumentSummary"][0]["SubmissionDate"],
            "ftp_path": summary["DocumentSummarySet"]["DocumentSummary"][0]["FtpPath_Assembly_rpt"],
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entrez error: {str(e)}")

async def fetch_assembly_metadata(accession):
    """Main assembly metadata fetcher with enhanced GCA handling and caching"""
    try:
        # Check cache first
        cached_data = await check_cache("assembly", accession)
        if cached_data:
            return cached_data

        base_accession = accession.split('.')[0]
        url = f"https://api.ncbi.nlm.nih.gov/datasets/v1/genome/accession/{base_accession}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            logging.info(f"API response for {accession}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    raise HTTPException(status_code=404, detail="Empty API response")
                
                metadata = format_assembly_metadata(data, accession)
                return await save_to_cache(metadata)
            
            raise HTTPException(status_code=response.status_code, detail="API request failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to fetch {accession}: {str(e)}")
        try:
            metadata = await fetch_via_entrez(accession)
            return await save_to_cache(metadata)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"All methods failed: {str(e)}")

@app.get("/search/")
async def search_ncbi(
    database: str = Query(..., description="NCBI database to search (e.g., nucleotide, assembly)"),
    query: Optional[str] = None,
    accession_ids: Optional[List[str]] = Query(None),
    taxid: Optional[int] = None,
    organism: Optional[str] = None,
    gene: Optional[str] = None,
    protein: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    molecule_type: Optional[str] = None,
    publication_date: Optional[str] = None,
    retmax: int = 10,
):
    """
    Unified endpoint to search NCBI databases (nucleotide and assembly) with caching.
    
    For assembly searches, provide accession_ids.
    For nucleotide searches, use any combination of filters.
    """
    try:
        # Handle assembly searches differently
        if database == "assembly":
            if not accession_ids:
                raise HTTPException(status_code=400, detail="Assembly searches require accession numbers")
            
            metadata = []
            failed_accessions = []
            
            for accession in accession_ids:
                try:
                    assembly_data = await fetch_assembly_metadata(accession)
                    metadata.append(assembly_data)
                except HTTPException as he:
                    logging.error(f"Failed to fetch assembly {accession}: {he.detail}")
                    failed_accessions.append(accession)
                except Exception as e:
                    logging.error(f"Unexpected error fetching assembly {accession}: {str(e)}")
                    failed_accessions.append(accession)
            
            return {
                "database": database,
                "query": f"Assembly accessions: {', '.join(accession_ids)}",
                "metadata": metadata,
                "failed_accessions": failed_accessions,
            }

        # For nucleotide and other standard databases
        search_terms = []
        if query:
            search_terms.append(query)
        
        if taxid and organism:
            logging.warning("Both taxid and organism provided. Using only organism.")
        
        if taxid and not organism:
            search_terms.append(f"txid{taxid}[Organism]")
        elif organism:
            search_terms.append(f'"{organism}"[Organism]')

        if accession_ids:
            search_terms.append(f"({' OR '.join(accession_ids)})[Accession]")

        if gene:
            search_terms.append(f'"{gene}"[Gene]')

        if protein:
            search_terms.append(f'"{protein}"[Protein]')    

        if min_length or max_length:
            length_query = f"{min_length or 0}:{max_length or 100000000}[SLEN]"
            search_terms.append(length_query)

        if molecule_type:
            search_terms.append(f'"{molecule_type}"[Molecule Type]')

        if publication_date:
            search_terms.append(f'"{publication_date}"[Publication Date]')

        # Construct final query string
        search_query = " AND ".join(search_terms).strip()

        if not search_query:
            raise HTTPException(status_code=400, detail="Search query is empty. Please provide valid filters.")

        logging.info(f"Constructed search query: {search_query}")

        # Perform NCBI search
        handle = Entrez.esearch(db=database, term=search_query, retmax=retmax, retmode="xml")
        search_results = Entrez.read(handle)
        handle.close()

        if not search_results["IdList"]:
            return {
                "database": database,
                "query": search_query,
                "metadata": [],
                "failed_uids": [],
            }

        # Fetch metadata for each UID
        metadata = []
        failed_uids = []
        for uid in search_results["IdList"]:
            try:
                if database == "nucleotide":
                    data = await fetch_nucleotide_metadata(uid)
                else:
                    # For other databases, we'd need to implement specific handlers
                    data = None
                
                if data:
                    metadata.append(data)
                else:
                    failed_uids.append(uid)
            except Exception as e:
                logging.error(f"Error fetching metadata for UID {uid}: {str(e)}")
                failed_uids.append(uid)

        return {
            "database": database,
            "query": search_query,
            "metadata": metadata,
            "failed_uids": failed_uids,
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in /search endpoint: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Unified NCBI Metadata API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)