<template>
  <div class="bodyHome">
    <!-- Error Message -->
    <div v-if="errormsg" class="error-message">
      {{ errormsg }}
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

    <!-- Search Form -->
    <form id="searchForm" @submit.prevent="searchDatabase">
      <div v-if="selectedDatabase === 'assembly'">
        <label for="accessionIds">Assembly Accession:</label>
        <input
          type="text"
          id="accessionIds"
          v-model="accessionIds"
          placeholder="Enter accession number"
          required
        /><br />
      </div>
      
      <div v-else>
        <label for="query">Search Term:</label>
        <input
          type="text"
          id="query"
          v-model="query"
          placeholder="Enter search terms"
        /><br />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </form>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      Loading...
    </div>

   <!-- Results Display -->
<div v-if="validMetadata.length > 0" class="results-container">
  <div
    v-for="(item, index) in validMetadata"
    :key="item.assembly?.assembly_accession || index"
    class="result-card"
  >
    <h3>{{ item.assembly?.org?.sci_name || 'Unknown organism' }}</h3>
    <div><strong>Accession:</strong> {{ item.accession || 'N/A' }}</div>
    <div><strong>Assembly Name:</strong> {{ item.assembly_name || 'N/A' }}</div>
    <div><strong>Level:</strong> {{ item.assembly_level || 'N/A' }}</div>
    <div><strong>Submission Date:</strong> {{ item.submission_date || 'N/A' }}</div>
    <div><strong>Organism:</strong> {{ item.organism?.sci_name || 'N/A' }}</div>
    <div><strong>Common Name:</strong> {{ item.organism?.common_name || 'N/A' }}</div>
    <div><strong>Taxonomy ID:</strong> {{ item.organism?.tax_id || 'N/A' }}</div>
    <div><strong>Chromosomes Count:</strong> {{ item.chromosomes_count || 'N/A' }}</div>
    <div><strong>Bioproject Title:</strong> {{ item.bioproject_title || 'N/A' }}</div>
    <div><strong>Annotation Info:</strong> {{ item.annotation_info || 'N/A' }}</div>
    <div><strong>Assembly Statistics:</strong> {{ item.assembly_statistics || 'N/A' }} </div>
    <div v-if="item.assembly?.ftp_path || item.ftp_path">
      <a :href="item.assembly?.ftp_path || item.ftp_path" target="_blank" class="download-link">
        Download Data
      </a>
    </div>

      <!-- Toggle Button -->
      <button @click="toggleDetails(index)">
        {{ expandedIndices.includes(index) ? 'Hide Details' : 'Show More' }}
      </button>
    </div>

    <!-- Collapsible JSON Viewer for Full Metadata -->
    <div v-if="expandedIndices.includes(index)" class="dynamic-metadata">
      <h4>All Metadata:</h4>
      <vue-json-pretty :data="item" :deep="2" />
    </div>
  </div>
</div>

</template>

<script>
import API from "../services/axios"
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
export default {
  components: {
    VueJsonPretty
  },
  data() {
    return {
      databases: ["nucleotide", "assembly"],
      selectedDatabase: "assembly",
      accessionIds: "",
      query: "",
      metadata: [],
      loading: false,
      errormsg: "",
      hasSearched: false,
      expandedIndices: []
    };
  },
  methods: {
    async searchDatabase() {
      this.loading = true;
      this.errormsg = "";
      this.metadata = [];
      this.hasSearched = true;

      try {
        const params = new URLSearchParams();
        params.append("database", this.selectedDatabase);

        if (this.selectedDatabase === "assembly") {
          const accessions = this.accessionIds.trim().split(/[\s,]+/).filter(id => id);
          if (!accessions.length) {
            throw new Error("Please enter at least one accession number");
          }
          accessions.forEach(id => params.append("accession_ids", id));
        } else {
          if (!this.query.trim()) {
            throw new Error("Please enter search terms");
          }
          params.append("query", this.query.trim());
        }

        // const response = await fetch(`http://localhost:8000/search/?${params.toString()}`);
        // const data = await response.json();
        const data = await API.search(params); // 🚀 Use centralized API

        // if (!response.ok) {
        //   throw new Error(data.detail || response.statusText || `Error code: ${response.status}`);
        // }

        // Handle both response formats
        if (data.results) {
          this.metadata = data.results;
        } else if (data.metadata) {
          this.metadata = data.metadata;
        }  else if (data.assemblies) {
          // this.metadata = data.assemblies.map(a => a.assembly); // <-- flatten assembly object
          this.metadata = data.assemblies;
        } else {
          throw new Error("Unexpected response format");
        }
        console.log("Fetched metadata:", JSON.stringify(this.metadata, null, 2));


        // Check for failed accessions
        if (data.failed_accessions?.length > 0) {
          this.errormsg = `Failed to fetch: ${data.failed_accessions.join(', ')}`;
          
          // Suggest removing version if present
          if (data.failed_accessions.some(id => id.includes('.'))) {
            this.errormsg += `. Try using base accession (e.g., GCA_000214015 instead of GCA_000214015.2)`;
          }
        }

      } catch (error) {
        console.error("Search error:", error);
        this.errormsg = error.message || "An unknown error occurred";
      } finally {
        this.loading = false;
      }
    },
    
    toggleDetails(index) {
      const i = this.expandedIndices.indexOf(index);
      if (i > -1) {
        this.expandedIndices.splice(i, 1);
      } else {
        this.expandedIndices.push(index);
      }
    },

    formatValue(value) {
      if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value, null, 2);
      }
      return value;
    }
  },

  computed: {
   validMetadata() {
  return this.metadata.filter(item =>
    item &&
    (
      item.accession ||
      item.assembly?.assembly_accession ||
      item.assembly_name ||
      item.assembly?.display_name
    )
  );
}

  }
};
</script>


<style>
.bodyHome {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.error-message {
  color: #d32f2f;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ffcdd2;
  background-color: #ffebee;
  border-radius: 4px;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  background: #f0f0f0;
  border: none;
  cursor: pointer;
  margin-right: 5px;
}

.tabs button.active {
  background: #1976d2;
  color: white;
}

.results-container {
  margin-top: 30px;
}

.result-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
}

.result-details div {
  margin: 8px 0;
}

.download-link {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 16px;
  background: #1976d2;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 20px 0;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  margin-top: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 4px;
}
.dynamic-metadata {
  background: #463f3f;
  padding: 10px;
  margin-top: 10px;
  font-size: 0.9em;
  border: 1px solid #ddd;
  border-radius: 8px;
  white-space: pre-wrap;
}

.meta-line {
  margin-bottom: 4px;
}

</style>