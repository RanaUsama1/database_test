<!--IDEA: Vue delle ricerche con funzine che prende tipo di ricerca e input e ritorna tabella -->
<script>
import LoadingSpinner from '../components/LoadingSpinner.vue';


export default {
    data: function () {
        return {
            errormsg: null,
            loading: false,
            search: null,
            product: null,
            location: null,
            type: "scientific_name",
            response: [],
            csvData: [],
            nameCsv: "",
            moreCount: 10,
        };
    },
    methods: {
        async nucleotideSearch() {
            this.loading = true;
            this.errormsg = null;
            this.nameCsv = "";
            this.moreCount = 10;
            try {
                //  
                let response = await this.$axios.get("/taxon_term", {
                    params: {
                        search: this.search,
                        type: this.type,
                        product: this.product,
                        location: this.location,
                    }
                });
                this.response = response.data;
                this.responseCut = this.response.slice(0, this.moreCount > this.response.length ? this.response.length : this.moreCount);    
                this.generateCSVData(this.response)
            }
            catch (e) {
                this.loading = false;
                this.errormsg = e.response.data;
                this.response = []
            }
            if(this.search){
              this.nameCsv += "."+this.search
            }
            if(this.product){
              this.nameCsv += "."+this.product
            }
            if(this.location){
              this.nameCsv += "."+this.location
            }
            this.nameCsv = this.nameCsv.replace(/\s+/g, '_').toLowerCase()
            this.loading = false;
        },
        generateCSVData(data){
            let newcsvdata = []
            for (let i = 0; i < data.length; i++) {
                let newDataImport = {
                  ScientificName: data[i].ScientificName,
                  TaxId: data[i].TaxId,
                  QtyNucleotides: data[i].QtyNucleotides,
                  QtyProteins: data[i].QtyProteins,
                  QtyProducts: data[i].QtyProducts,
                  GenomesLink: data[i].Genomes[0] ? data[i].Genomes[0].Link : ""
                }
              newcsvdata.push(newDataImport)
            }
            this.csvData = newcsvdata
        },
        
        updateCuts(){
            this.moreCount += 10
            this.responseCut = this.response.slice(0, this.moreCount > this.response.length ? this.response.length : this.moreCount);
        },

    },
    components: { LoadingSpinner },
    async mounted(){
        
        let product = this.$route.query.product;
        if (!product){
          return
        }
        this.product = product
        this.nucleotideSearch()
      },
}

</script>

<template>
  <div>
    <div class="dropdown">
      <label for="dropdown">
        <h1>
          Type:
        </h1>
      </label>
      <select id="dropdown" name="drop minimal" v-model="type">
        <option value="scientific_name" selected>Scientific Name</option>
        <option value="id">Taxon Id</option>
      </select>
    </div>
    <div class="input">
      <input type="text" class="search-input" id="search-input1" :placeholder="this.type == 'scientific_name' ? 'Input Scientific Name' : 'Input Taxonomy Id'" v-model="search" v-on:keyup.enter="nucleotideSearch()"/>
      <br><br><br>
      <input type="text" class="search-input" id="search-input2" placeholder="Filter for product" v-model="product" v-on:keyup.enter="nucleotideSearch()"/>
      <input type="text" class="search-input" id="search-input3" placeholder="Filter for location" v-model="location" v-on:keyup.enter="nucleotideSearch()"/>
    </div>
  </div>
  <div>
    <button type="button" @click="nucleotideSearch()"> Search</button>
  </div>


<!--TABELLA -->
<br/>
<br/>
<br/>
<br/>
  <LoadingSpinner :loading="this.loading"/>
  <ErrorMsg v-if="errormsg" :msg="errormsg"></ErrorMsg>
  <div v-if="response.length > 0">
    <div style="display: flex; gap: 20px;">
      <div class="result-button-length">
        <h1>{{ response.length }} Results</h1>
      </div>
      <div class="download-button" id="download-button">
        <div class="download-text clickable">
          <download-csv
            :data="this.csvData"
            :name="'VULGARIS'+ this.nameCsv +'.csv'">
            Download Data
          </download-csv>
        </div>
      </div>
    </div>
    <TableComp :data="this.responseCut"/>
    <div v-if="this.response.length > this.moreCount" class="load-more clickable">
        <h1 @click="updateCuts()">
            load more...
        </h1>
    </div>
  </div>


</template>


<style>
.input {
  margin-bottom: 10px;

}

.dropdown {
  margin-bottom: 20px;
}

button {
  padding: 10px;
  background-color: #003399;
  color: white;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0b11bb;
}


.row{
    display: flex;
    gap: 5px;
}


.input input[type="text"] {
    width: 40%;
    padding: 10px;
    left: 50%;
    border: 1px solid #dddddd;
    margin-bottom: 15px;
    box-sizing:border-box;
}

.result-button-length{
    position: fixed;
    font-weight: bold;
    margin-left: -190px;
}

.download-text {
  padding: 10px;
}

.download-button {
  position: fixed;
  cursor: pointer;
  margin-top: 30px;
  font-weight: bold;
  margin-left: -190px;
  font-size: 20px;
  border-radius: 7px;
  width: 165px;
  box-shadow: 0 0 5px #0099FF;
  background: rgba(0,0,0,0.6);
}

.download-button:hover {
  box-shadow: 0 0 8px #0099FF;
}

.search-input{
  color: rgb(166, 166, 166);
  background: rgba(0, 0, 0, 0.397);
}

#dropdown{
  color: rgb(255, 255, 255);
  background: rgba(0, 0, 0, 0.397);
}

.load-more {
    display: flex;
    align-items:center;
    justify-content: space-around
}

.load-more:hover {
    cursor: pointer;
}

</style>