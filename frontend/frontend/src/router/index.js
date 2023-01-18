import Vue from "vue";
import VueRouter from "vue-router";
import PredatorPrey from "@/views/PredatorPrey.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/PredatorPrey",
    name: "PredatorPrey",
    component: PredatorPrey,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
