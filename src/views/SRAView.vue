<script>
export default{
    data: function () {
        return {
            errormsg: null,
            loading: false,
            genomes: null,
            project: null,
            csvData: [],
        };
    },
    methods: {

        close(taxId){
            this.project = null
            document.getElementById("popup-"+taxId).style.display = "none"

        },

        ProjectsTree(genome) {
            if (this.genomeClick){
                this.close(TaxId)
            }
            this.genomeClick=genome
            document.getElementById("popup-"+genome.TaxId).style.display = "flex"
        },
        openModal(taxId){
          if (this.project){
            return
          }
          document.getElementById("popup-"+taxId).style.display = "flex"
          this.project = taxId
        },
        generateCSVData(data){
            let newcsvdata = []
            for (let i = 0; i < data.length; i++) {
                let proj = data[i]
                for (let j = 0; j < proj.BioSamples.length; j++) {
                    let samp = proj.BioSamples[j]
                    for (let k = 0; k < samp.Experiments.length; k++) {
                        let exp = samp.Experiments[k]
                        for (let l = 0; l < exp.Runs.length; l++) {
                          let run = exp.Runs[l]
                          let newDataImport = {
                              ScientificName: proj.ScientificName ? proj.ScientificName : proj.TaxId,
                              TaxId : proj.TaxId,
                              BioProject : proj.BioProjectId,
                              Sample : samp.BioSampleId,
                              Experiment : exp.ExperimentId,
                              Run : run
                          }
                          newcsvdata.push(newDataImport)
                        }
                      
                    }
                  
                }
                
            }
            this.csvData = newcsvdata
        },

    },
    async mounted(){
        this.loading = true
        try{
            let response = await this.$axios.get(`/analysis`);
            let projects = response.data
            this.generateCSVData(projects)
            let gen = {}
            console.log(projects);
            projects.forEach(proj => {
              if(proj.BioProjectId == "PRJNA496045"){
                proj.ImagesPath = ["/images/heatmap_degs.png","/images/volcanoPlot.png"]
              }
              if(proj.BioProjectId == "PRJNA389600"){
                proj.ImagesPath = ["/images/heatmap_degs_pico.png","/images/volcanoPlot_pico.png"]
              }
              if(!gen[proj.TaxId]){
                gen[proj.TaxId] = []
              }
              gen[proj.TaxId].push(proj)
            });
            this.genomes = gen
            this.loading = false
        } catch(e){
            this.loading = false
            this.errormsg = e.response
        }
    },
}

</script>

<template>
<br/>
<br/>
<div class="TitlePageHome">
  SRA Analysis
</div>
<br/>
<br/>
  <LoadingSpinner :loading="this.loading"/>
  <div v-if="errormsg">
		Error:
		<ErrorMsg :msg="errormsg"></ErrorMsg>
	</div>
  <div v-if="this.genomes && this.csvData">
    <div style="display: flex; gap: 20px;">
      <div>
        <h1>{{ Object.keys(this.genomes).length }} Results</h1>
      </div>
      <div class="download-button">
        <div class="download-text clickable">
          <download-csv
            :data="this.csvData"
            :name="'VULGARIS.SRA_DATA.csv'">
            Download Data
          </download-csv>
        </div>
      </div>
    </div>
    <table id="table">
      <thead>
        <tr>
          <th>Scientific Name</th>
          <th>Number BioProjects</th>
        </tr>
      </thead>
      <tr v-for="genome in this.genomes" :key="genome.TaxId">

        <td class="clickable">
          <div @click="openModal(genome[0].TaxId)" style="cursor: pointer;">
            {{ genome[0].ScientificName ? genome[0].ScientificName : genome[0].TaxId }}
          </div>
          <div class="popup" :id="'popup-'+genome[0].TaxId">
            <div v-if="this.project" class="popup-content">
              <button v-if="this.project" type="button" class="buttonclose" @click="close(genome[0].TaxId)">Close</button>
              <BioProjComp :data="genome"/>
            </div>
          </div>
        </td>
        <td>
          {{ genome.length }}
        </td>
      </tr>
    </table>
  </div>
            
</template>

<style>
.row{
    display: flex;
    gap: 5px;
   }
   #table {
    border-collapse: collapse;
    width: 100%;
   }
   #table td, #table th {
    border: 1px solid #6cace1;
    padding: 20px;
    align-content: center;
   }
   #table .title{
     font-size: 25px;
     background-color: #999999;
     text-align: center;
   }
   /* #table tr:nth-child(even){background-color: #88a3f7;} */
   table tr:hover {background-color: rgb(134, 220, 239,.18);}
   #table th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #04aa6d;
    
   }

.popup{
    background: rgba(0, 0, 0, 0.6);
    position: absolute;
    /* overflow: auto;
    max-height: 100%; */
    top: 10%;
    left: 18%;
    right: 5%;
    /* right: 5%; */
    display: none;
    justify-content: center;
    align-items: center;
    border: 2px solid black;
}

.popup-content{
    overflow-y: auto;
    word-wrap: break-word;
    overflow-x: visible;
    top: 10%;
    bottom: 10%;
    right: 5%;
    left: 5%;
    width: 90%;
    color: #ffffff;
    size: 10px;
    box-shadow: 0 0 5px #0099FF;
    background:rgba(0, 0, 0, 0.9);
    padding: 2px;
    border-radius: 5px;
    position:fixed;
}


.popupclose{
  position: relative;
  bottom: 0px;
  right: 0px;
  border-radius: 5px;
  background-color: #003399;
}


.popup-close{
    position: absolute;
    top: -15px;
    right: -15px;
    background: #fff;
    height: 20px;
    width: 20px;
    border-radius: 50%;
    box-shadow: 6px 6px 29px -4px rgba(0,0,0,0.75);
    cursor: pointer;
}


.buttonclose{
  position: fixed;
  top: 2%;
  right: 5%;
  background-color: #003399;
  border-radius: 5px;
  width:100px;
  height:50px;
}

</style>