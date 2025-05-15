import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import HelpView from "../views/HelpView.vue";
import ContactsView from "../views/ContactsView.vue";
import NucleotideDatabase from "../views/nucleotideView.vue";
import GenomeDatabase from "../views/genomeView.vue";
import OrganismView from "../views/OrganismView.vue";
import SRAView from "../views/SRAView.vue";
import NotFoundView from "../views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || "/"),
  routes: [
    { path: "/", component: HomeView },
    { path: "/help", component: HelpView },
    { path: "/contacts", component: ContactsView },
    { path: "/nucleotide", component: NucleotideDatabase },
    // { path: "/taxonomy/:taxid", component: Taxonomy },
    { path: "/genome", component: GenomeDatabase },
    { path: "/organism/:taxid/nucleotides", component: OrganismView },
    { path: "/organism/:taxid/proteins", component: OrganismView },
    { path: "/sra", component: SRAView },
    { path: "/:pathMatch(.*)", component: NotFoundView },
  ],
});

export default router;
