<script>
export default {
	props: ['data'],
    methods:{
        async expandContent(item){
            let box = document.getElementById('id-'+item.TaxId)
            let exp = document.getElementById('exp-'+item.TaxId)
            let arr = document.getElementById('arrow-'+item.TaxId)
            if (arr.classList.length > 1){
                arr.setAttribute('class', 'arrow-sep');
                box.style.paddingBottom = '';
                exp.style.display = 'none';
            }
            else{
                arr.setAttribute('class', 'arrow-sep arrow-sep-active');
                box.style.paddingBottom = '80px';
                await sleep(350);
                exp.style.display = 'flex';
            }
            // arr.className += " arrow-sep-active";

            
            
        },
        mouseOver(id,item){
          if (!item || item.length == 0){
            return
          }
          let fin = document.getElementById(id)
          fin.style.visibility = "visible"
        },
        mouseNotOver(id,item){
          if (!item || item.length == 0){
            return
          }
          let fin = document.getElementById(id)
          fin.style.visibility = "hidden"
        },
        
    }
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
</script>

<template>
    <div>
        <ul class="table-drop-ul" >
            <li class="table-drop-li" v-for="item in data" :key="item">
                
                <div class="content-table" :id="'id-'+item.TaxId">
                    <div class="content-info">
                        <div class="subinfo">
                            <h4 class="title">
                                Scientific Name
                            </h4>
                            <RouterLink :to="'/organism/'+item.TaxId + '/nucleotides'">
                                <h1>
                                    {{item.ScientificName}}
                                </h1>
                            </RouterLink>
                            
                        </div>
                    </div>
                    <div class="content-info">
                        <div class="subinfo">
                            <h4 class="title">
                                Genome
                            </h4>
                            <div @mouseleave="mouseNotOver('genome-'+item.TaxId,item.Genomes)" @mouseover="mouseOver('genome-'+item.TaxId,item.Genomes)">
                                <h1>
                                    {{ !item.Genomes || item.Genomes.length > 0 ? 'Link' : '-' }}
                                </h1>
                                <div class="dropdown-genome">
                                    <div :id="'genome-'+item.TaxId" class="dropdown-content-genome">
                                        <a v-if="item.Genomes && item.Genomes.length > 0" :href="item.Genomes[0].Link" target=”_blank”>
                                        <div :style="item.Genomes[0].GBFF ? 'background-color:green;' : 'background-color:red;'" style="text-align: center;">
                                            GCFF
                                        </div>
                                        <div :style="item.Genomes[0].FNA ? 'background-color:green;' : 'background-color:red;'" style="text-align: center;">
                                            FNA
                                        </div>
                                        <div :style="item.Genomes[0].GFF ? 'background-color:green;' : 'background-color:red;'" style="text-align: center;">
                                            GFF
                                        </div>
                                        </a>
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                    <div class="expand-content" @click="expandContent(item)">
                        <svg width="34" height="34" viewBox="0 0 24 24" class="arrow-sep" :id="'arrow-'+item.TaxId">
                            <path d="M12 16.41l-6.71-6.7 1.42-1.42 5.29 5.3 5.29-5.3 1.42 1.42z"></path>
                        </svg>
                    </div>
                </div>
                <div class="content-expansion" :id="'exp-'+item.TaxId">
                    
                    <div class="content-info-exp">
                        <div class="subinfo">
                            <h4 class="title">
                                Tax Id
                            </h4>
                            <RouterLink :to="'/taxonomy/'+item.TaxId">
                                <h1>
                                    {{item.TaxId}}
                                </h1>
                            </RouterLink>
                            
                        </div>
                    </div>
                    <div class="content-info-exp">
                        <div class="subinfo">
                            <h4 class="title">
                                Nucleotides
                            </h4>
                            <h1>
                                {{item.QtyNucleotides}}
                            </h1>
                        </div>
                    </div>
                    <div class="content-info-exp">
                        <div class="subinfo">
                            <h4 class="title">
                                Proteins
                            </h4>
                            <h1>
                                {{item.QtyProteins}}
                            </h1>
                        </div>
                    </div>
                    <div class="content-info-exp">
                        <div class="subinfo">
                            <h4 class="title">
                                Products
                            </h4>
                            <h1>
                                {{item.QtyProducts}}
                            </h1>
                        </div>
                    </div>
                </div>
                <div class="separator">
                    <hr>
                </div>
            </li>
        </ul>
    </div>
</template>



<style>



.separator {
    height: 1px;
    background: #dddddd;
}

.table-drop-ul {
    
    list-style-type: none;
    padding: 0;
    border: 1px solid #dddddd;
    border-radius: 4px;
}

.table-drop-li {
    background: rgba(0, 0, 0, 0.733);
    border-radius: 4px;
}


.content-table {
    display:flex;
    margin-left: 5%;
    margin-right: 5%;
    margin-bottom: 5%;
    padding-top: 5%;
    justify-content:space-between;
    align-items:center;
    transition:0.5s;
}

.content-expansion {
    display:none;
    margin-left: 5%;
    margin-right: 5%;
    margin-top: -6%;
    justify-content:space-between;
    align-items:center;
    transition:0.5s;
    animation-delay: 1s;
}

.content-info {
    width: 33%;
}

.subinfo {
    display: flex;
    flex-direction: column;
}

.subinfo .title {
    color: #adadad;
}

.expand-content {
    float: right;
}

.expand-content:hover {
    background: rgba(209, 209, 209, 0.219);
    border-radius: 50%;
}

.content-info-exp {
    width: 25%;
}

.arrow-sep {
    fill: #dddddd;
    transition:0.5s;
}

.arrow-sep.arrow-sep-active {
    -o-transform:rotate(180deg);
    -ms-transform:rotate(180deg);
    -moz-transform:rotate(180deg);
    -webkit-transform:rotate(180deg);
    transform:rotate(180deg);
}

.dropdown-genome {
  position: relative;
  display: block;
  margin-right: 25px;
}

.dropdown-content-genome {
  visibility: hidden;
  position: absolute;
  min-width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.733);
  z-index: 1;
  align-content: center;
}

.dropdown-genome:hover .dropdown-content-genome {
  display: block;
}

</style>