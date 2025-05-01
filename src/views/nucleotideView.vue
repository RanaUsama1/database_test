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
    <form id="searchForm">
      <label for="query">Keywords:</label>
      <input
        type="text"
        id="query"
        v-model="query"
        placeholder="Enter keywords (e.g., Homo sapiens)"
      /><br />

      <label for="accessionIds">Accession Numbers (comma-separated):</label>
      <input
        type="text"
        id="accessionIds"
        v-model="accessionIds"
        placeholder="Enter accession numbers"
      /><br />

      <label for="taxid">Taxonomic ID:</label>
      <input
        type="number"
        id="taxid"
        v-model="taxid"
        placeholder="Enter TaxID (e.g., 9606)"
      /><br />
      <!-- Add these to your form -->
      <label for="organism">Organism:</label>
      <input
        type="text"
        id="organism"
        v-model="organism"
        placeholder="Enter organism name (e.g., Homo sapiens)"
      /><br />

      <label for="gene">Gene:</label>
      <input
        type="text"
        id="gene"
        v-model="gene"
        placeholder="Enter gene name (e.g., COX1)"
      /><br />

      <label for="protein">Protein:</label>
      <input
        type="text"
        id="protein"
        v-model="protein"
        placeholder="Enter protein name (e.g., cytochrome oxidase)"
      /><br />

      <label for="moleculeType">Molecule Type:</label>
      <select id="moleculeType" v-model="moleculeType">
        <option value="">Any</option>
        <option value="DNA">DNA</option>
        <option value="RNA">RNA</option>
        <option value="mRNA">mRNA</option>
      </select><br />

      <label for="pubDate">Publication Date:</label>
      <input
        type="text"
        id="pubDate"
        v-model="pubDate"
        placeholder="YYYY/MM/DD or YYYY"
      /><br />
      <button type="button" @click="searchDatabase">Search</button>
    </form>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      Loading...
    </div>

    <!-- Results Section -->
    <div id="results">
      <div v-if="metadata.length > 0" class="results-container">
        <div v-for="(item, index) in metadata" :key="index" class="result-card">
          <h2>{{ item.accession }}</h2>
          <div class="result-details">
            <p><strong>Organism:</strong> {{ item.organism }}</p>
            <p><strong>Definition:</strong> {{ item.definition }}</p>
            <p><strong>Length:</strong> {{ item.length }} bp</p>
            <p><strong>Updated Date:</strong> {{ item.updated_date }}</p>
            <p><strong>Genes:</strong> {{ item.genes.join(", ") }}</p>
          </div>

          <!-- Features Section -->
          <div class="collapsible-section">
            <button class="collapsible" @click="toggleCollapsible($event)">
              View Features
            </button>
            <div class="content">
              <div
                v-for="(feature, i) in item.features"
                :key="i"
                class="feature-item"
              >
                <p><strong>Type:</strong> {{ feature.type }}</p>
                <p><strong>Location:</strong> {{ feature.location }}</p>
                <p><strong>Qualifiers:</strong></p>
                <ul>
                  <li v-for="(value, key) in feature.qualifiers" :key="key">
                    <strong>{{ key }}:</strong> {{ value }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- References Section -->
          <div class="collapsible-section">
            <button class="collapsible" @click="toggleCollapsible($event)">
              View References
            </button>
            <div class="content">
              <div
                v-for="(reference, i) in item.references"
                :key="i"
                class="reference-item"
              >
                <p><strong>Title:</strong> {{ reference.title }}</p>
                <p><strong>Authors:</strong> {{ reference.authors }}</p>
                <p><strong>Journal:</strong> {{ reference.journal }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p v-else-if="!loading" class="no-results">
        No metadata found for the search query.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      databases: [
        "nucleotide",
        "assembly",
        "bioproject",
        "biosample",
        "gene",
        "genome",
      ], // Add more databases
      selectedDatabase: "nucleotide", // Default database
      query: "",
      accessionIds: "",
      taxid: "",
      minLength: "",
      maxLength: "",
      metadata: [],
      organism: "",
      gene: "",
      protein: "",
      moleculeType: "",
      pubDate: "",
      errormsg: "",
      loading: false,
    };
  },
  methods: {
    async searchDatabase() {
      this.loading = true;
      this.errormsg = "";
      this.metadata = [];

      const params = new URLSearchParams();
      params.append("database", this.selectedDatabase);
      if (this.organism) params.append("organism", this.organism);
      if (this.gene) params.append("gene", this.gene);
      if (this.protein) params.append("protein", this.protein);
      if (this.moleculeType) params.append("molecule_type", this.moleculeType);
      if (this.pubDate) params.append("publication_date", this.pubDate); // Add database parameter
      if (this.query) params.append("query", this.query);
      if (this.accessionIds) params.append("accession_ids", this.accessionIds);
      if (this.taxid) params.append("taxid", this.taxid);
      if (this.minLength) params.append("min_length", this.minLength);
      if (this.maxLength) params.append("max_length", this.maxLength);

      const apiUrl = `http://127.0.0.1:8000/search/?${params.toString()}`;

      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        this.metadata = data.metadata || [];
      } catch (error) {
        console.error("Error:", error);
        this.errormsg = error.message;
      } finally {
        this.loading = false;
      }
    },
    toggleCollapsible(event) {
      const content = event.target.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    },
  },
};
</script>

<style>
.collapsible {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 8px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active,
.collapsible:hover {
  background-color: #555;
}

.content {
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #0000;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}
</style>
