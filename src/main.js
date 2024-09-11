import { createApp } from "vue";
// import { BModal, BButton } from 'bootstrap-vue-3'
import JsonCSV from "vue-json-csv";
import App from "./App.vue";
import router from "./router/index.js";
import axios from "./services/axios.js";
import ErrorMsg from "./components/ErrorMsg.vue";
import LoadingSpinner from "./components/LoadingSpinner.vue";
import NucleoComp from "./components/NucleotideComp.vue";
import BioProjComp from "./components/BioProjComp.vue";
import TableComp from "./components/TableComp.vue";
// import AppDropdown from './components/AppDropdown.vue'
// import AppDropdownContent from './components/AppDropdownContent.vue'
// import AppDropdownItem from './components/AppDropdownItem.vue'
import "./assets/dashboard.css";
import "./assets/main.css";
import "./assets/login.css";
import "./assets/modal.css";
import "./assets/dropdown.css";
import "./assets/monitor.css";
const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.component("download-csv", JsonCSV);
app.component("ErrorMsg", ErrorMsg);
app.component("NucleoComp", NucleoComp);
app.component("LoadingSpinner", LoadingSpinner);
app.component("BioProjComp", BioProjComp);
app.component("TableComp", TableComp);
app.use(router);
app.mount("#app");
