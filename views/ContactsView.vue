
<!-- frontend/src/components/MetadataSearch.vue -->
<template>
  <div class="metadata-search-container">
    <h1>NCBI Assembly Metadata Lookup</h1>
    
    <div class="search-section">
      <input 
        type="text" 
        v-model="assemblyAccession" 
        placeholder="Enter Assembly Accession (comma-separated)"
        @keyup.enter="fetchMetadata"
      />
      <div class="button-group">
        <button 
          @click="fetchMetadata" 
          :disabled="isLoading"
          class="btn btn-primary"
        >
          {{ isLoading ? 'Searching...' : 'Search Metadata' }}
        </button>
        <button 
          @click="viewCSV" 
          :disabled="isLoading"
          class="btn btn-secondary"
        >
          View Saved CSV
        </button>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Fetching metadata...</p>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Metadata Display -->
    <div v-if="metadata" class="metadata-results">
      <div 
        v-for="(data, accession) in metadata" 
        :key="accession" 
        class="metadata-card"
      >
        <h2>Assembly: {{ accession }}</h2>
        
        <template v-if="!data.error">
          <div 
            v-for="(value, key) in data" 
            :key="key" 
            class="metadata-property"
            v-show="key !== 'assembly_accession'"
          >
            <strong>{{ formatKey(key) }}:</strong>
            <span>{{ value }}</span>
          </div>
        </template>
        
        <div v-else class="error-details">
          <p>Error: {{ data.error }}</p>
        </div>
      </div>
    </div>

    <!-- CSV Display -->
    <div v-if="csvData" class="csv-display">
      <h2>Saved CSV Data</h2>
      <table>
        <thead>
          <tr>
            <th v-for="header in csvHeaders" :key="header">
              {{ formatKey(header) }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in csvData" :key="index">
            <td v-for="(value, key) in row" :key="key">
              {{ value }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  data() {
    return {
      assemblyAccession: '',
      metadata: null,
      csvData: null,
      csvHeaders: [],
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    formatKey(key) {
      return key.replace(/_/g, ' ').toUpperCase()
    },
    async fetchMetadata() {
      if (!this.assemblyAccession.trim()) {
        this.errorMessage = 'Please enter at least one assembly accession'
        return
      }

      this.resetState()
      this.isLoading = true

      try {
        const response = await axios.get(`/fetch_metadata`, {
          params: { accession: this.assemblyAccession }
        })
        this.metadata = response.data
        this.errorMessage = ''
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Error fetching metadata'
      } finally {
        this.isLoading = false
      }
    },
    async viewCSV() {
      this.resetState()
      this.isLoading = true

      try {
        const response = await axios.get('/view_csv')
        this.csvData = response.data
        
        // Extract headers from first row
        if (this.csvData.length > 0) {
          this.csvHeaders = Object.keys(this.csvData[0])
        }
        
        this.errorMessage = ''
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Error viewing CSV'
      } finally {
        this.isLoading = false
      }
    },
    resetState() {
      this.metadata = null
      this.csvData = null
      this.csvHeaders = []
      this.errorMessage = ''
    }
  }
}
</script>

<style>
.metadata-search-container {
  max-width: 1000px;
  margin: 0 auto;
}

</style>