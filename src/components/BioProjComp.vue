<script>
export default {
  props: ["data"],
  methods: {},
};
</script>
<!-- 
<template>
     <div>BioProjects of {{ scientificName }}</div> -->
<!-- <tr>
        BioProjects of {{ data[0].ScientificName ? data[0].ScientificName : data[0].TaxId }}
    </tr>
    <ul v-for="proj in data">
        <div class="origin">
            BioProject: ({{ proj.BioSamples.length }})
        </div>
        <a :href="'https://www.ncbi.nlm.nih.gov/bioproject/' + proj.BioProjectId" target = "_blank">
            {{ proj.BioProjectId }}
        </a>
        <ul>
            <tr>
                <td v-for="sample in proj.BioSamples">
                    <div class="origin">
                        BioSample: ({{ sample.Experiments.length }})
                    </div>
                    <a :href="'https://www.ncbi.nlm.nih.gov/biosample/' + sample.BioSampleId" target = "_blank">
                        {{ sample.BioSampleId }}
                    </a>
                    <ul>
                        <tr>
                            <td v-for="exp in sample.Experiments">
                                <div class="origin">
                                    Experiment: ({{ exp.Runs.length }})
                                </div>
                                <a :href="'https://www.ncbi.nlm.nih.gov/sra/' + exp.ExperimentId" target = "_blank">
                                    {{ exp.ExperimentId }}
                                </a>
                                <ul v-for="run in exp.Runs">
                                    <tr>
                                        <td>
                                            <div class="origin">
                                                Run:
                                            </div>
                                            <a :href="'https://trace.ncbi.nlm.nih.gov/Traces?run=' + run" target = "_blank">
                                                {{ run }}
                                            </a>
                                        </td>
                                    </tr>
                                </ul>
                            </td>
                        </tr>
                    </ul>
                </td>
            </tr>
        </ul>
        <div v-if="proj.ImagesPath && proj.ImagesPath.length > 0" style="margin-top: 40px;">
            HeatMap & Volcano Images of the BioProject {{ proj.BioProjectId }}
            <div>
                 <span class="span-underline" style="color: pink;">pink</span>: case <span class="span-underline" style="color: blue; margin-left: 20px;">blu</span>:control
            </div>
        </div>
        <div v-if="proj.ImagesPath && proj.ImagesPath.length > 0" style="display: flex; gap: 50px;">
            
            <div v-for="img in proj.ImagesPath">
                <img class="projimg" :src="img" alt="Prova">
            </div>
        </div>
    </ul> -->

<!-- </template> -->

<template>
  <div>
    <div>
      BioProjects of
      {{ data[0].ScientificName ? data[0].ScientificName : data[0].TaxId }}
    </div>

    <ul v-for="proj in data" :key="proj.BioProjectId">
      <div class="origin">BioProject: ({{ proj.BioSamples.length }})</div>
      <a
        :href="'https://www.ncbi.nlm.nih.gov/bioproject/' + proj.BioProjectId"
        target="_blank"
      >
        {{ proj.BioProjectId }}
      </a>

      <!-- Use a table for the BioSamples data -->
      <table>
        <!-- Table header inside thead -->
        <thead>
          <tr>
            <th>BioSample</th>
            <th>Experiments</th>
            <th>Runs</th>
          </tr>
        </thead>

        <!-- Table body inside tbody -->
        <tbody>
          <tr v-for="sample in proj.BioSamples" :key="sample.BioSampleId">
            <td>
              <div class="origin">
                BioSample: ({{ sample.Experiments.length }})
              </div>
              <a
                :href="
                  'https://www.ncbi.nlm.nih.gov/biosample/' + sample.BioSampleId
                "
                target="_blank"
              >
                {{ sample.BioSampleId }}
              </a>
            </td>
            <td v-for="exp in sample.Experiments" :key="exp.ExperimentId">
              <div class="origin">Experiment: ({{ exp.Runs.length }})</div>
              <a
                :href="'https://www.ncbi.nlm.nih.gov/sra/' + exp.ExperimentId"
                target="_blank"
              >
                {{ exp.ExperimentId }}
              </a>
            </td>
            <td>
              <ul v-for="run in exp.Runs" :key="run">
                <li>
                  <div class="origin">Run:</div>
                  <a
                    :href="'https://trace.ncbi.nlm.nih.gov/Traces?run=' + run"
                    target="_blank"
                  >
                    {{ run }}
                  </a>
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Optional images for each project -->
      <div
        v-if="proj.ImagesPath && proj.ImagesPath.length > 0"
        style="margin-top: 40px"
      >
        HeatMap & Volcano Images of the BioProject {{ proj.BioProjectId }}
        <div>
          <span class="span-underline" style="color: pink">pink</span>: case
          <span class="span-underline" style="color: blue; margin-left: 20px"
            >blue</span
          >: control
        </div>
      </div>
      <div
        v-if="proj.ImagesPath && proj.ImagesPath.length > 0"
        style="display: flex; gap: 50px"
      >
        <div v-for="img in proj.ImagesPath" :key="img">
          <img class="projimg" :src="img" alt="Prova" />
        </div>
      </div>
    </ul>
  </div>
</template>

<style>
.origin {
  color: rgb(172, 172, 172);
}
.projimg {
  width: 600px;
  height: 600px;
}

.projimg:hover {
  width: 800px;
  height: 800px;
}
</style>
