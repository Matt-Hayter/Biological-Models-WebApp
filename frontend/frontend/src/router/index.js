import Vue from "vue";
import VueRouter from "vue-router";
import Model_selection from "../components/Model_selection.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Model_selection",
    component: Model_selection,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
