import Vue from "vue";
import VueRouter from "vue-router";
import Navigation_bar from "../components/Navigation_bar.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Navigation_bar",
    component: Navigation_bar,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
