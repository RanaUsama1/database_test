<template>
  <div class="bodyHome">
    <!-- Error Message -->
    <div v-if="errormsg" class="error-message">
      {{ errormsg }}
    </div>

    <!-- Important Information Banner -->
    <div v-if="hasSearched" class="info-banner">
      <p>
        <strong>Note:</strong> Due to NCBI API restrictions, some newer
        accessions may only show basic information here. For complete metadata,
        please click the "View Full Details on NCBI Website" link.
      </p>
    </div>

    <h1>NCBI Database Search</h1>

    <!-- Tabs for Databases -->
    <div class="tabs">
      <button
        v-for="db in databases"
        :key="db"
        :class="{ active: selectedDatabase === db }"
        @click="selectedDatabase = db"
      >
        {{ db }}
      </button>
    </div>

    <form id="searchForm" @submit.prevent="searchDatabase">
      <!-- Assembly Database Form -->
      <div v-if="selectedDatabase === 'assembly'" class="database-form">
        <div class="search-options">
          <label><input type="radio" v-model="searchType" value="organism"> Search by Organism</label>
          <label><input type="radio" v-model="searchType" value="accession"> Search by Accession</label>
        </div>

        <div v-if="searchType === 'organism'" class="organism-search">
          <label for="organism">Organism Name:</label>
          <input type="text" id="organism" v-model="organism" placeholder="e.g., Escherichia coli"/>
          
          <label for="taxid">Taxonomic ID (optional):</label>
          <input type="number" id="taxid" v-model="taxid" placeholder="e.g., 562"/>
        </div>

        <div v-if="searchType === 'accession'" class="accession-search">
          <label for="accessionIds">Assembly Accessions:</label>
          <textarea 
            id="accessionIds" 
            v-model="accessionIds" 
            placeholder="GCF_000005845.2, GCA_000005845.2"
            rows="3"
          ></textarea>
          <small>Enter RefSeq (GCF_) or GenBank (GCA_) accessions, comma-separated</small>
        </div>
      </div>

      <!-- Nucleotide Database Form -->
      <div v-else-if="selectedDatabase === 'nucleotide'" class="database-form">
        <label for="query">Search Query:</label>
        <input type="text" id="query" v-model="query" placeholder="e.g., BRCA1 gene or NM_001301717.1"/>
        
        <label for="organism">Organism (optional):</label>
        <input type="text" id="organism" v-model="organism" placeholder="e.g., Homo sapiens"/>
        
        <label for="accessionIds">Accession Numbers (optional):</label>
        <textarea 
          id="accessionIds" 
          v-model="accessionIds" 
          placeholder="NM_001301717.1, NC_000001.11"
          rows="2"
        ></textarea>
        <small>Enter nucleotide accessions (NM_, NC_, NR_), comma-separated</small>
      </div>

      <!-- Gene Database Form -->
      <div v-else-if="selectedDatabase === 'gene'" class="database-form">
        <label for="query">Gene Search:</label>
        <input type="text" id="query" v-model="query" placeholder="e.g., TP53 or insulin"/>
        
        <label for="organism">Organism (optional):</label>
        <input type="text" id="organism" v-model="organism" placeholder="e.g., Homo sapiens"/>
      </div>

      <!-- Taxonomy Database Form -->
      <div v-else-if="selectedDatabase === 'taxonomy'" class="database-form">
        <label for="organism">Organism Name:</label>
        <input type="text" id="organism" v-model="organism" placeholder="e.g., Escherichia coli"/>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Searching..." : "Search" }}
      </button>
    </form>

    <!-- Quick Search Suggestions -->
    <div class="search-suggestions" v-if="!hasSearched">
      <p><strong>Quick Search Examples:</strong></p>
      <div class="suggestion-buttons">
        <button @click="quickSearch('Homo sapiens')">Human</button>
        <button @click="quickSearch('Mus musculus')">Mouse</button>
        <button @click="quickSearch('Saccharomyces cerevisiae')">Yeast</button>
        <button @click="quickSearch('Streptococcus pneumoniae')">S. pneumoniae</button>
        <button @click="quickSearch('Mycobacterium tuberculosis')">M. tuberculosis</button>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      Loading...
    </div>

    <!-- Data Source Banner -->
    <div v-if="metadataSource && hasSearched && !loading" class="data-source-banner" :class="metadataSource">
      <div v-if="metadataSource === 'ncbi'">
        <h4>✅ Complete NCBI Data</h4>
        <p>Showing full metadata directly from NCBI</p>
      </div>
      <div v-else-if="metadataSource === 'ena'">
        <h4>🌐 ENA Fallback Data</h4>
        <p>Showing complete metadata from European Nucleotide Archive (ENA)</p>
      </div>
      <div v-else-if="metadataSource === 'ncbi_limited'">
        <h4>⚠️ Limited NCBI Data</h4>
        <p>Only partial metadata available from NCBI</p>
      </div>
      <div v-else-if="metadataSource === 'error'">
        <h4>❌ Data Retrieval Error</h4>
        <p>Could not retrieve complete metadata</p>
      </div>
    </div>

    <!-- Results Display -->
    <div v-if="validMetadata.length > 0" class="results-container">
      <div
        v-for="(item, index) in validMetadata"
        :key="item.accession || index"
        class="result-card"
      >
        <h3>
          {{
            item.organism?.sci_name || 
            item.organism || 
            "Unknown organism"
          }}
        </h3>

        <div><strong>Accession:</strong> {{ item.accession || "N/A" }}</div>
        <div><strong>Data Source:</strong> {{ item.database || "Unknown" }}</div>

        <!-- Assembly-specific fields -->
        <div v-if="selectedDatabase === 'assembly'">
          <div v-if="item.assembly_name && item.assembly_name !== 'N/A'">
            <strong>Assembly Name:</strong> {{ item.assembly_name }}
          </div>

          <div v-if="item.assembly_level && item.assembly_level !== 'N/A'">
            <strong>Assembly Level:</strong> {{ item.assembly_level }}
          </div>

          <div v-if="item.submission_date && item.submission_date !== 'N/A'">
            <strong>Submission Date:</strong> {{ item.submission_date }}
          </div>

          <!-- Assembly Statistics Section -->
          <div class="statistics-section" v-if="selectedDatabase === 'assembly'">
            <h4>Assembly Statistics</h4>
            
            <div v-if="hasGenomeStats(item)" class="stats-grid">
              <div v-if="item.genome_size && item.genome_size !== 'N/A'" class="stat-item">
                <strong>Genome Size:</strong> {{ formatNumber(item.genome_size) }} bp
              </div>
              <div v-else class="stat-item missing">
                <strong>Genome Size:</strong> Not available
              </div>

              <div v-if="item.contig_n50 && item.contig_n50 !== 'N/A'" class="stat-item">
                <strong>Contig N50:</strong> {{ formatNumber(item.contig_n50) }}
              </div>
              <div v-else class="stat-item missing">
                <strong>Contig N50:</strong> Not available
              </div>

              <div v-if="item.number_of_contigs && item.number_of_contigs !== 'N/A'" class="stat-item">
                <strong>Number of Contigs:</strong> {{ item.number_of_contigs }}
              </div>
              <div v-else class="stat-item missing">
                <strong>Number of Contigs:</strong> Not available
              </div>

              <div v-if="item.gc_percent && item.gc_percent !== 'N/A'" class="stat-item">
                <strong>GC Content:</strong> {{ item.gc_percent }}%
              </div>
              <div v-else class="stat-item missing">
                <strong>GC Content:</strong> Not available
              </div>
            </div>
            
            <div v-else class="no-stats">
              <p>⚠️ Detailed assembly statistics not available in NCBI API response</p>
              <p class="small-note">
                This is common for newer assemblies. Click "View Full Details" 
                to see complete statistics on the official NCBI page.
              </p>
            </div>
          </div>
        </div>

        <!-- Nucleotide-specific fields -->
        <div v-if="selectedDatabase === 'nucleotide'">
          <div v-if="item.definition && item.definition !== 'Unknown'">
            <strong>Definition:</strong> {{ item.definition }}
          </div>

          <div v-if="item.length">
            <strong>Sequence Length:</strong> {{ formatNumber(item.length) }} bp
          </div>

          <div v-if="item.updated_date && item.updated_date !== 'Unknown'">
            <strong>Updated Date:</strong> {{ item.updated_date }}
          </div>

          <div v-if="item.source && item.source !== 'Unknown'">
            <strong>Source:</strong> {{ item.source }}
          </div>

          <div v-if="item.genes && item.genes.length > 0">
            <strong>Genes:</strong> {{ item.genes.join(', ') }}
          </div>
        </div>

        <!-- Common organism fields -->
        <div v-if="item.organism?.sci_name && item.organism.sci_name !== 'Unknown'">
          <strong>Organism:</strong> {{ item.organism.sci_name }}
        </div>

        <div v-if="item.organism?.common_name && item.organism.common_name !== 'Unknown'">
          <strong>Common Name:</strong> {{ item.organism.common_name }}
        </div>

        <div v-if="item.organism?.tax_id && item.organism.tax_id !== 'N/A'">
          <strong>Taxonomy ID:</strong> {{ item.organism.tax_id }}
        </div>

        <!-- Additional fields -->
        <div v-if="item.biosample && item.biosample !== 'N/A'">
          <strong>BioSample:</strong> {{ item.biosample }}
        </div>

        <div v-if="item.bioproject && item.bioproject !== 'N/A'">
          <strong>BioProject:</strong> {{ item.bioproject }}
        </div>

        <!-- Always show the website link -->
        <div class="ncbi-link">
          <a
            :href="getFtpPath(item)"
            target="_blank"
            class="download-link"
          >
            {{ getLinkText(item) }}
          </a>
        </div>

        <!-- Show warning if we only have minimal data -->
        <div v-if="item.additional_info && item.database === 'minimal'" class="warning-message">
          ⚠️ {{ item.additional_info }}
        </div>

        <!-- Toggle Button for Raw Data -->
        <button @click="toggleDetails(index)" class="details-toggle">
          {{
            expandedIndices.includes(index)
              ? "Hide Raw Data"
              : "Show Raw Data"
          }}
        </button>

        <!-- Beautiful JSON Display -->
        <div v-if="expandedIndices.includes(index)" class="raw-data-section">
          <h4>Complete Metadata</h4>
          <div class="json-viewer">
            <pre>{{ JSON.stringify(item, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-else-if="hasSearched && !loading" class="no-results">
      No results found. Try a different search term or check the spelling.
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      databases: ["nucleotide", "assembly", "taxonomy", "gene"],
      selectedDatabase: "assembly",
      searchType: "organism", // "organism" or "accession"
      organism: "",
      query: "",
      accessionIds: "",
      taxid: "",
      minLength: "",
      maxLength: "",
      metadata: [],
      loading: false,
      errormsg: "",
      hasSearched: false,
      expandedIndices: [],
      metadataSource: ""
    };
  },
  computed: {
    validMetadata() {
      return this.metadata.filter(item => {
        return item && item.accession;
      });
    },
  },
  methods: {
    // Quick search for common organisms
    quickSearch(organism) {
      this.organism = organism;
      this.searchType = "organism";
      this.searchDatabase();
    },

    // Get appropriate link text based on data source
    getLinkText(item) {
      if (item.database === 'ena') {
        return 'View on ENA Website';
      } else if (item.database === 'minimal') {
        return 'View on NCBI Website';
      } else {
        return 'View Full Details on NCBI Website';
      }
    },

    getFtpPath(item) {
        // Always provide a valid web URL, never FTP
        if (item.accession) {
          if (this.selectedDatabase === 'assembly') {
            return `https://www.ncbi.nlm.nih.gov/datasets/genome/${item.accession}/`;
          } else if (this.selectedDatabase === 'nucleotide') {
            return `https://www.ncbi.nlm.nih.gov/nuccore/${item.accession}`;
          }
        }
        return '#';
      },

    // Toggle expansion state of an item
    toggleDetails(index) {
      const i = this.expandedIndices.indexOf(index);
      if (i > -1) {
        this.expandedIndices.splice(i, 1);
      } else {
        this.expandedIndices.push(index);
      }
    },

    // Format numbers with commas
    formatNumber(num) {
      if (!num || num === 'N/A') return 'N/A';
      // Remove any non-numeric characters and format
      const cleanNum = num.toString().replace(/[^\d]/g, '');
      if (!cleanNum) return 'N/A';
      return parseInt(cleanNum).toLocaleString();
    },

    // Check if item has genome statistics
    hasGenomeStats(item) {
      return (item.genome_size && item.genome_size !== 'N/A') ||
             (item.contig_n50 && item.contig_n50 !== 'N/A') ||
             (item.gc_percent && item.gc_percent !== 'N/A');
    },

    // Main search entry point
    async searchDatabase() {
      // Basic validation
      if (this.selectedDatabase === 'assembly' && this.searchType === 'organism' && !this.organism.trim()) {
        this.errormsg = "Please enter an organism name for assembly search";
        return;
      }

      if (this.selectedDatabase === 'assembly' && this.searchType === 'accession' && !this.accessionIds.trim()) {
        this.errormsg = "Please enter accession numbers for assembly search";
        return;
      }

      if (this.selectedDatabase === 'nucleotide' && !this.query.trim() && !this.accessionIds.trim()) {
        this.errormsg = "Please enter a search query or accession numbers for nucleotide search";
        return;
      }

      if (this.selectedDatabase === 'gene' && !this.query.trim()) {
        this.errormsg = "Please enter a gene name or search query";
        return;
      }

      if (this.selectedDatabase === 'taxonomy' && !this.organism.trim()) {
        this.errormsg = "Please enter an organism name for taxonomy search";
        return;
      }

      this.loading = true;
      this.errormsg = "";
      this.metadata = [];
      this.hasSearched = true;
      this.expandedIndices = [];
      this.metadataSource = "";

      try {
        if (this.selectedDatabase === "assembly") {
          await this.searchAssembliesDirect();
        } else if (this.selectedDatabase === "nucleotide") {
          await this.searchNucleotide();
        } else if (this.selectedDatabase === "gene") {
          await this.searchGene();
        } else if (this.selectedDatabase === "taxonomy") {
          await this.searchTaxonomy();
        }
      } catch (error) {
        console.error("Search error:", error);
        this.errormsg = error.message || "An unexpected error occurred";
        this.metadataSource = "error";
      } finally {
        this.loading = false;
      }
    },

    // DIRECT assembly search
  // DIRECT assembly search
      async searchAssembliesDirect() {
        try {
          const params = {
            database: "assembly",
            retmax: 50
          };

          if (this.searchType === "organism") {
            // Organism-based search
            if (this.organism?.trim()) {
              params.organism = this.organism.trim();
            }
            if (this.taxid) {
              params.taxid = parseInt(this.taxid, 10);
            }
          } else {
            // Accession-based search - FIX THIS PART
            if (this.accessionIds?.trim()) {
              // Clean up the accession IDs - remove spaces, handle multiple
              const accessions = this.accessionIds.trim()
                .split(',')
                .map(acc => acc.trim())
                .filter(acc => acc.length > 0);
              
              if (accessions.length > 0) {
                params.accession_ids = accessions.join(',');
              }
            }
          }

          // Validate: at least one search criterion must be present
          if (!params.organism && !params.accession_ids) {
            this.errormsg = "Please enter either organism name or accession numbers";
            this.metadataSource = "error";
            return;
          }

          const apiUrl = `${__API_URL__}/search/?${new URLSearchParams(params).toString()}`;
          console.log("API URL:", apiUrl);

          const response = await fetch(apiUrl, {
            method: "GET",
            headers: { 
              "Content-Type": "application/json",
              "Accept": "application/json"
            }
          });

          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API Error: ${response.status} - ${errorText}`);
          }

          const data = await response.json();
          console.log("API Response:", data);

          if (data.metadata && data.metadata.length > 0) {
            this.metadata = data.metadata;
            this.analyzeOverallMetadataQuality(data.metadata);
            
            if (data.failed_accessions && data.failed_accessions.length > 0) {
              console.warn("Failed accessions:", data.failed_accessions);
            }
          } else {
            this.errormsg = data.message || "No assemblies found.";
            this.metadataSource = "error";
          }
        } catch (err) {
          console.error("Assembly search error:", err);
          this.errormsg = err.message || "Failed to connect to the server. Make sure the backend is running on localhost:8000";
          this.metadataSource = "error";
        }
      },

    // Nucleotide search
    async searchNucleotide() {
      try {
        const params = {
          database: "nucleotide",
          retmax: 50
        };

        if (this.query?.trim()) {
          params.query = this.query.trim();
        }

        if (this.organism?.trim()) {
          params.organism = this.organism.trim();
        }

        if (this.accessionIds?.trim()) {
          params.accession_ids = this.accessionIds.trim();
        }

        // Validate: at least one search criterion must be present
        if (!params.query && !params.accession_ids) {
          this.errormsg = "Please enter either a search query or accession numbers";
          this.metadataSource = "error";
          return;
        }

        const apiUrl = `${__API_URL__}/search/?${new URLSearchParams(params).toString()}`;
        console.log("Nucleotide API URL:", apiUrl);

        const response = await fetch(apiUrl, {
          method: "GET",
          headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json"
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Nucleotide API Response:", data);

        if (data.metadata && data.metadata.length > 0) {
          this.metadata = data.metadata;
          this.errormsg = `Found ${data.metadata.length} nucleotide records`;
          this.metadataSource = "ncbi";
        } else {
          this.errormsg = data.message || "No nucleotide records found.";
          this.metadataSource = "error";
        }
      } catch (err) {
        console.error("Nucleotide search error:", err);
        this.errormsg = err.message || "Failed to search nucleotide database";
        this.metadataSource = "error";
      }
    },

    // Gene search
    async searchGene() {
      try {
        const params = {
          database: "gene",
          query: this.query.trim(),
          retmax: 50
        };

        if (this.organism?.trim()) {
          params.organism = this.organism.trim();
        }

        const apiUrl = `${__API_URL__}/search/?${new URLSearchParams(params).toString()}`;
        console.log("Gene API URL:", apiUrl);

        const response = await fetch(apiUrl, {
          method: "GET",
          headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json"
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Gene API Response:", data);

        if (data.metadata && data.metadata.length > 0) {
          this.metadata = data.metadata;
          this.errormsg = `Found ${data.metadata.length} gene records`;
          this.metadataSource = "ncbi";
        } else {
          this.errormsg = data.message || "No gene records found.";
          this.metadataSource = "error";
        }
      } catch (err) {
        console.error("Gene search error:", err);
        this.errormsg = err.message || "Failed to search gene database";
        this.metadataSource = "error";
      }
    },

    // Taxonomy search
    async searchTaxonomy() {
      try {
        const params = {
          database: "taxonomy",
          organism: this.organism.trim(),
          retmax: 20
        };

        const apiUrl = `${__API_URL__}/search/?${new URLSearchParams(params).toString()}`;
        console.log("Taxonomy API URL:", apiUrl);

        const response = await fetch(apiUrl, {
          method: "GET",
          headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json"
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Taxonomy API Response:", data);

        if (data.metadata && data.metadata.length > 0) {
          this.metadata = data.metadata;
          this.errormsg = `Found ${data.metadata.length} taxonomy records`;
          this.metadataSource = "ncbi";
        } else {
          this.errormsg = data.message || "No taxonomy records found.";
          this.metadataSource = "error";
        }
      } catch (err) {
        console.error("Taxonomy search error:", err);
        this.errormsg = err.message || "Failed to search taxonomy database";
        this.metadataSource = "error";
      }
    },

    // Analyze overall metadata quality
    analyzeOverallMetadataQuality(metadata) {
      if (!metadata || metadata.length === 0) {
        this.metadataSource = "error";
        return;
      }

      // Count different data sources
      const sources = {
        assembly: 0,    // NCBI complete
        ena: 0,         // ENA complete  
        minimal: 0,     // Fallback
        other: 0
      };

      let hasCompleteData = false;
      let hasPartialData = false;

      metadata.forEach(item => {
        sources[item.database] = (sources[item.database] || 0) + 1;
        
        // Check if this item has complete data
        if (this.isMetadataComplete(item)) {
          hasCompleteData = true;
        } else if (this.hasBasicOrganismData(item)) {
          hasPartialData = true;
        }
      });

      const resultCount = metadata.length;

      // Determine overall data quality
      if (hasCompleteData && sources.assembly > 0) {
        this.metadataSource = "ncbi";
        this.errormsg = `Found ${resultCount} assemblies with complete NCBI data`;
      } else if (sources.ena > 0) {
        this.metadataSource = "ena";
        this.errormsg = `Found ${resultCount} assemblies using ENA data`;
      } else if (hasPartialData) {
        this.metadataSource = "ncbi_limited";
        this.errormsg = `Found ${resultCount} assemblies with limited metadata`;
      } else {
        this.metadataSource = "error";
        this.errormsg = `Found ${resultCount} assemblies but could not retrieve detailed metadata`;
      }

      console.log("Data sources:", sources);
    },

    // Check if metadata has basic organism data
    hasBasicOrganismData(item) {
      return item.organism && 
             item.organism.sci_name && 
             item.organism.sci_name !== "Unknown" &&
             item.organism.tax_id !== "N/A";
    },

    // Check if metadata is complete
    isMetadataComplete(item) {
      const hasOrganism = this.hasBasicOrganismData(item);
      const hasAssemblyInfo = item.assembly_level && item.assembly_level !== "N/A";
      const hasGenomeStats = item.genome_size && item.genome_size !== "N/A" &&
                            item.contig_n50 && item.contig_n50 !== "N/A";

      return hasOrganism && hasAssemblyInfo && hasGenomeStats;
    }
  }
}
</script>
<style scoped>
.bodyHome {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f8f9fa; /* Light grey background for the whole page */
  min-height: 100vh;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  background: white; /* White background for tabs */
  border-radius: 8px 8px 0 0;
  padding: 10px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-right: 10px;
}

.tabs button.active {
  border-bottom-color: #007acc;
  font-weight: bold;
  color: #007acc;
}

.tabs button:hover {
  background-color: #f5f5f5;
  border-radius: 4px;
}

form {
  background: white;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

label {
  display: block;
  margin: 15px 0 8px;
  font-weight: bold;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #007acc;
  box-shadow: 0 0 0 2px rgba(0,122,204,0.2);
}

button[type="submit"] {
  background: #007acc;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background: #005a9e;
}

button[type="submit"]:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading-indicator {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
  margin: 20px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007acc;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 2s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.data-source-banner {
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  border-left: 5px solid;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.data-source-banner.ncbi {
  background: #e8f5e8;
  border-left-color: #4caf50;
}

.data-source-banner.ena {
  background: #e8f4fd;
  border-left-color: #2196f3;
}

.data-source-banner.ncbi_limited {
  background: #fff3e0;
  border-left-color: #ff9800;
}

.data-source-banner.error {
  background: #ffebee;
  border-left-color: #f44336;
}

.results-container {
  display: grid;
  gap: 20px;
  margin-top: 20px;
}

.result-card {
  border: 1px solid #e1e5e9;
  border-radius: 10px;
  padding: 25px;
  background: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.result-card h3 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 15px;
  font-size: 1.4em;
}

.result-card div {
  margin-bottom: 12px;
  line-height: 1.5;
  color: #555;
}

.result-card strong {
  color: #333;
}

/* Statistics Section */
.statistics-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  border-left: 4px solid #007acc;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.stat-item {
  padding: 12px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #28a745;
}

.stat-item.missing {
  border-left-color: #6c757d;
  background: #f8f9fa;
  color: #6c757d;
}

.no-stats {
  text-align: center;
  padding: 20px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  color: #856404;
}

.small-note {
  font-size: 0.9em;
  margin-top: 10px;
  opacity: 0.8;
}

.ncbi-link {
  margin: 20px 0;
  text-align: center;
}

.download-link {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 12px 24px;
  text-decoration: none;
  border-radius: 6px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.download-link:hover {
  background: #218838;
  text-decoration: none;
  color: white;
}

.warning-message {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
  padding: 15px;
  border-radius: 6px;
  margin: 15px 0;
}

.details-toggle {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  margin: 15px 0;
  transition: background-color 0.3s;
}

.details-toggle:hover {
  background: #5a6268;
}

.raw-data {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 20px;
  margin-top: 15px;
  overflow-x: auto;
}

.raw-data pre {
  margin: 0;
  font-size: 12px;
  white-space: pre-wrap;
  background: #2d3748;
  color: #e2e8f0;
  padding: 15px;
  border-radius: 4px;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 15px 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
  font-weight: bold;
}

.info-banner {
  background: #d1ecf1;
  color: #0c5460;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid #bee5eb;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
  font-style: italic;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-info {
  background: #e9ecef;
  padding: 15px;
  border-radius: 6px;
  margin: 15px 0;
  border-left: 4px solid #6c757d;
}

.search-info small {
  color: #495057;
  line-height: 1.4;
}
.raw-data-section {
  background: #1a1a1a;
  border-radius: 8px;
  padding: 20px;
  margin-top: 15px;
  border: 1px solid #333;
}

.raw-data-section h4 {
  color: #fff;
  margin-bottom: 15px;
  font-family: 'Courier New', monospace;
}

.json-viewer {
  background: #2d2d2d;
  border-radius: 6px;
  padding: 15px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  max-height: 400px;
  overflow-y: auto;
}

.json-line {
  margin-bottom: 8px;
  padding-left: 10px;
  border-left: 2px solid transparent;
}

.json-line:hover {
  border-left-color: #007acc;
  background: rgba(255,255,255,0.05);
}

.json-key {
  color: #ff79c6; /* Pink for keys */
  font-weight: bold;
}

.json-value {
  color: #f1fa8c; /* Yellow for string values */
}

.json-object {
  color: #50fa7b; /* Green for objects */
  white-space: pre-wrap;
}

/* Scrollbar styling */
.json-viewer::-webkit-scrollbar {
  width: 8px;
}

.json-viewer::-webkit-scrollbar-track {
  background: #1a1a1a;
  border-radius: 4px;
}

.json-viewer::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.json-viewer::-webkit-scrollbar-thumb:hover {
  background: #777;
}

</style>
