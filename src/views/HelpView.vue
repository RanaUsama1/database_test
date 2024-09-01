<script>
export default {
	data: function() {
		return {
		}
	},
}
</script>

<template>
    <br>
	<div class="TitlePageHome">
		About MicroAlgae DB
	</div>
    <div class="bodyHome">
		<div class="sectionHome">
            What is this Webapp
        </div>
        <div class="contentHome">
            This platform was born as university project for a computational biology exam, 
            computer science course at <pan class="span-bold">La Sapienza</pan> University of Rome.
            It is served as is, without guarantee of any kind, under MIT license. During its development, 
            we retrieved a lot of data, and for some of them it has been necessary to follow an approach
            of cross-link among other web platform. The idea behind MicroAlgae DB is to make data accessible
            in an easy way without consult different platforms about microalgae that have great CO2 capture properties.
            We hope that this project will continue to be manteined and developed, because its potential are 
            of interest for everyone.
        </div>
        <div class="sectionHome">
            How it is composed
        </div>
        <div class="contentHome">
			<ul class="circle-dot">
				<li>
					- Home
				</li>
				<li>
					- Views:
				</li>
				<ul class="square-dot">
					<li>
						-- Search
					</li>
					<li>
						-- Taxonomy
					</li>
					<li>
						-- SRA
					</li>
				</ul>
				<li>
					- Help
				</li>
				<li>
					- Contacts
				</li>
			</ul>
        </div>
        <div class="sectionHome">
            Home
        </div>
        <div class="contentHome">
            Roba qui
        </div>
        <div class="sectionHome">
            Views
        </div>
        <div class="contentHome">
            Analisi di Search
        </div>
        <div class="sectionHome">
            Analisi di Taxonomy
        </div>
        <div class="contentHome">
            Analisi di SRA
        </div>
        <div class="sectionHome">
            Help
        </div>
        <div class="contentHome">
            Questa pagina
        </div>
        <div class="sectionHome">
            Contacts
        </div>
        <div class="contentHome">
            Dobbiamo davvero spiegarla?
        </div>
    </div>
</template>

<style>
.contentHome{
	margin-left: 3%;
	margin-right: 3%;
	margin-top: 2%;
	font-size: 16px;
	word-wrap:break-word;
	text-align: justify;
	text-justify: inter-word;
}
.circle-dot{
	list-style-type: circle;
}
.square-dot{
	list-style-type: square;
}
</style>