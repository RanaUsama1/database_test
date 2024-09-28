import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import HelpView from "../views/HelpView.vue";
import ContactsView from "../views/ContactsView.vue";
import Taxonomy from "../views/TaxonomyView.vue";
import SearchTable from "../views/SearchTable.vue";
import OrganismView from "../views/OrganismView.vue";
import SRAView from "../views/SRAView.vue";
import NotFoundView from "../views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || "/"),
  routes: [
    { path: "/", component: HomeView },
    { path: "/help", component: HelpView },
    { path: "/contacts", component: ContactsView },
    { path: "/taxonomy", component: Taxonomy },
    { path: "/taxonomy/:taxid", component: Taxonomy },
    { path: "/taxon", component: SearchTable },
    { path: "/organism/:taxid/nucleotides", component: OrganismView },
    { path: "/organism/:taxid/proteins", component: OrganismView },
    { path: "/sra", component: SRAView },
    {
      path: "/team",
      beforeEnter(to, from, next) {
        window.location.replace("https://www.youtube.com/watch?v=uDLVHywMGfE");
      },
    },
    { path: "/:pathMatch(.*)", component: NotFoundView },
  ],
});

export default router;
