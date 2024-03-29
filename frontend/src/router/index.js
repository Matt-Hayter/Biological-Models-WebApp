import Vue from "vue";
import VueRouter from "vue-router";
import PredatorPrey from "@/views/predator-prey/PredatorPrey.vue";
import CompetingSpecies from "@/views/competing-species/CompetingSpecies.vue";
import SIR from "@/views/sir/Sir.vue";
import SEIDR from "@/views/seidr/Seidr.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "PredatorPrey",
    component: PredatorPrey,
  },
  {
    path: "/CompetingSpecies",
    name: "CompetingSpecies",
    component: CompetingSpecies,
  },
  {
    path: "/SIR",
    name: "SIR",
    component: SIR,
  },
  {
    path: "/SEIDR",
    name: "SEIDR",
    component: SEIDR,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
