<script>
export default {
	data: function() {
		return {
			errormsg: null,
			loading: false,
			some_data: ""
		}
	},
	methods: {
        data(){
        },
	},
	async mounted(){
		try{
            let response = await this.$axios.get(`/`);
        } catch(e){
            this.errormsg = e.message
        }
	}
}
</script>

<template>
	<div class="TitlePageHome">
			Micro Algae Database
	</div>
	<div v-if="errormsg">
		Error:
		<ErrorMsg :msg="errormsg"></ErrorMsg>
	</div>
	<div class="bodyHome">
		<div class="sectionHome">
			First Micro Algae Platform
		</div>
		<div class="contentHome">
			<span class="span-bold">
				Welcome to the world's first database of the genomic resources of microalgae
				with high CO2 removal capacity.</span>
				Here you will find a vast collection of carefully curated information on
				microalgae, specially selected for their unique ability to capture atmospheric
				CO2. Our database provides immediate access to valuable genomic data,
				including complete genomes, transcriptomics, proteomics and more. .
				MicroAlgae DB is a database for browsing taxonomic, nucleotide and protein
				data on over 900+ microalgae species.
				With this state-of-the-art research tool, scholars, scientists and innovators will
				have the opportunity to explore the genetic properties and metabolic
				pathways involved in CO2 removal by microalgae. We are confident that this
				database will become the reference source for anyone interested in
				understanding, harnessing and developing innovative solutions to address the
				global challenge of climate change.
			<div class="imagesHome">
				<img src="/images/Chlorella_img.jpg" alt="Chlorella" title="Chlorella">
				<img src="/images/Scenedesmus_img.jpg" alt="Scenedesmus" title="Scenedesmus">
			</div>
			<div style="display:flex;">
				<figcaption>Chlorella Vulgaris</figcaption>
				<figcaption class="right-fig">Scenedesmus Obliquus</figcaption>
			</div>

		</div>
		<div class="sectionHome">
			Currently in MicroAlgae DB Platform
		</div>
		<div class="contentHome">
			<span class="span-underline">969</span> species, <span class="span-underline">510.440</span> nucleotide and <span class="span-underline">612.654</span> protein entries, <span class="span-underline">21</span> genomes data and <span class="span-underline">12</span> species with <span class="span-underline">30</span> bioprojects.
		</div>
	</div>
</template>

<style>
.TitlePageHome {
    font-size: 48px;
	text-align: center;
    color: orange;
}
.TitlePageHome:hover, .TitlePageHome:focus, .TitlePageHome:active { 
    /* color:#ffcc00;  */
    text-shadow: 0 4px 6px #000; 
}
.bodyHome{
	margin-top: 5%;
}
.sectionHome {
	margin-top: 3%;
	font-size: 28px;
	color:#757575;
}
.sectionHome:hover, .sectionHome:focus, .sectionHome:active { 
    /* color:#ffcc00;  */
    text-shadow: 0 4px 6px #000; 
}
.contentHome{
	margin-left: 3%;
	margin-right: 3%;
	margin-top: 2%;
	font-size: 16px;
	word-wrap:break-word;
	text-align: justify;
	text-justify: inter-word;
}
.contentHome:hover {
	text-shadow: 0 6px 8px #000; 
}
.imagesHome{
	margin-top: 2%;
	gap: 10%;
	display:flex;
}
.imagesHome img{
	width: 400px;
	height: 400px;
}

.right-fig{
	margin-left: 364px;
}

.span-underline {
  text-decoration: underline;
}

.span-bold {
	font-weight: bold;
}

</style>