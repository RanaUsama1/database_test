<!-- <dropdown class="my-dropdown-toggle"
          :options="arrayOfObjects" 
          :selected="object" 
          v-on:updateOption="methodToRunOnSelect" 
          :placeholder="'Select an Item'"
          :closeOnOutsideClick="boolean">
</dropdown> -->

<script>
    // import AppDropdown from './components/AppDropdown.vue'
    // import AppDropdownContent from './components/AppDropdownContent.vue'
    // import AppDropdownItem from './components/AppDropdownItem.vue'
    // import dropdown from 'vue-dropdowns';
    
export default{
    data: function () {
        return {
            token: null,
            some_data: null,
            errormsg: null,
			dataBool: false,
            active: false,
            arrayOfObjects: [],
            object: {
              name: 'Object Name',
            }            
        }
    },
    // components: {
    //         'dropdown': dropdown,
    //     },

    methods:{
        async info(){
			// let response = await this.$axios.get("/");
			// this.some_data = response.data;

        },
        methodToRunOnSelect(payload) {
            this.object = payload;
        }
    },
    async mounted(){
        await this.info()
    }
}


</script>
<template>
    <header>
        <hgroup style="display:flex; margin-top: 5%;">
            <img src="/images/MicroAlgae_logo.png" alt="Micro Algae Logo" title="Micro Algae Logo" style="width:10%; height: auto; margin-top:-30px;">
            <h1>MicroAlgae DB</h1>
        </hgroup>
        <nav>
            <ul class="left">
                <li>
                    <RouterLink to="/">
                        Home
					</RouterLink>
                </li>
                <!-- <li>
                    <RouterLink to="/">
                        here goes Drop-down menu (that have to comprehend Search, Taxonomy and SRA)
					</RouterLink>
                </li> -->
                <li>
                    <RouterLink to="/taxon">
                        Search
					</RouterLink>
                </li>
                <li>
                    <RouterLink to="/taxonomy">
                        Taxonomy
					</RouterLink>
                </li>
                <li>
                    <RouterLink to="/sra">
                        SRA
					</RouterLink>
                </li>
            </ul>
            <ul class="right">
                <li>
                    <RouterLink to="/help">
                        Help
					</RouterLink>
                </li>
                <li>
                    <RouterLink to="/contacts">
                        Contacts
					</RouterLink>
                </li>
            </ul>
        </nav>
    </header>
    <div style="padding-top: 270px">
    <RouterView/>
    </div>
    <footer>
        <div style="margin-top:20px; margin-bottom:20px">
        <div class="banners">
            <div class="image">
                <img src="/images/unitus.png" style="width:70%; height:70%; margin-top: 20px;">
            </div>
            <div class="image">
                <img src="/images/Stemma_sapienza.png" style="width:100%; height:100%">
            </div>
            <div class="image">
                <img src="/images/cnr.png" style="width:80%; height:100%; margin-top:15px;">
            </div>
        </div>
        <RouterLink to="/contacts">
            <p>
                Team di Biologia Computazionale 2023, Università La Sapienza<br>
            </p>
		</RouterLink>
        <div style="margin-top: 12px;">
            <a href="https://github.com/BITSapienza" target="_blank" >Github project</a>
        </div>
    </div>
    </footer>
</template>

<style>
.image{
    width: 100%
}
.banners{
    display: inline-flex;
    text-align:center;
    margin-bottom: 30px;
}

</style>
