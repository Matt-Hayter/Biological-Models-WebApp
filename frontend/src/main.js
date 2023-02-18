import Vue from "vue";
import App from "./App.vue";
import router from "./router";
//Bootstrap modules
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
//Katex module and stylesheet for equations
import VueKatex from "vue-katex";
import "katex/dist/katex.min.css";

import { store } from "./store";

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VueKatex)

new Vue({
  store,
  router,
  render: (h) => h(App),
}).$mount("#app");
