import Vue from "vue";
import VueRouter from "vue-router";
import PredatorPrey from "@/views/PredatorPrey.vue";
import CompetingSpecies from "@/views/CompetingSpecies.vue";
import SEIR from "@/views/SEIR.vue";
import SEI3RD from "@/views/SEI3RD.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/PredatorPrey",
    name: "PredatorPrey",
    component: PredatorPrey,
  },
  {
    path: "/CompetingSpecies",
    name: "CompetingSpecies",
    component: CompetingSpecies,
  },
  {
    path: "/SEIR",
    name: "SEIR",
    component: SEIR,
  },
  {
    path: "/SEI3RD",
    name: "SEI3RD",
    component: SEI3RD,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
