<script>

export default {
  data: function () {
    return {
      token: null,
      some_data: null,
      errormsg: null,
      dataBool: false,
      active: false,
      arrayOfObjects: [],
      object: {
        name: "Object Name",
      },
    };
  },

  methods: {
    async info() {
    },
    methodToRunOnSelect(payload) {
      this.object = payload;
    },
  },
  async mounted() {
    await this.info();
  },
};
</script>
<template>
  <div class="main-content">
    <header>
      <hgroup style="display: flex; margin-top: 5%">
        <img
          src="/src/images/MicroAlgae_logo.png"
          alt="Micro Algae Logo"
          title="Micro Algae Logo"
          style="width: 10%; height: auto; margin-top: -30px"
        />
        <h1>MicroAlgae DB</h1>
      </hgroup>
      <nav>
        <ul class="left">
          <li>
            <RouterLink to="/"> Home </RouterLink>
          </li>
          <li>
            <RouterLink to="/genome"> Taxonomy </RouterLink>
          </li>
          <li>
            <RouterLink to="/taxonomy"> Nucleotide </RouterLink>
          </li>
          <!-- <li>
          <RouterLink to="/sra"> SRA </RouterLink>
        </li> -->
        </ul>
        <ul class="right">
          <li>
            <RouterLink to="/help"> Help </RouterLink>
          </li>
          <li>
            <RouterLink to="/contacts"> Contacts </RouterLink>
          </li>
        </ul>
      </nav>
    </header>
    <div style="padding-top: 20px">
      <RouterView />
    </div>
  </div>
  <footer class="containerr">
    <div style="text-align: center">
      <div class="banners">
        <div class="image">
          <img
            src="/src/images/unitus.png"
            style="width: 70%; height: 70%; margin-top: 20px"
          />
        </div>
        <div class="image">
          <img
            src="/src/images/Stemma_sapienza.png"
            style="width: 100%; height: 100%"
          />
        </div>
        <div class="image">
          <img
            src="/src/images/cnr.png"
            style="width: 80%; height: 100%; margin-top: 15px"
          />
        </div>
      </div>
      <RouterLink to="">
        <p>
          Team di Biologia Computazionale 2025, Università La Sapienza<br />
        </p>
      </RouterLink>
      <div style="margin-top: 12px">
        <a href="https://github.com/BITSapienza" target="_blank"
          >Github project</a
        >
      </div>
    </div>
  </footer>
</template>

<style>
.banner image {
  width: 100%;
  flex: 1;
  text-align: center;
  padding: 0 15px;
}
.banners {
  display: inline-flex;
  text-align: center;
  margin-bottom: 30px;
}
.containerr {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
