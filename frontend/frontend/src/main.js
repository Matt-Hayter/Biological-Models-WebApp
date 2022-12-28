import Vue from "vue";
import App from "./App.vue";
import router from "./router";
//Bootstrap modules
import "bootstrap/dist/css/bootstrap.css";
import BootstrapVue from "bootstrap-vue";
import "jquery";
import "popper.js";

Vue.config.productionTip = false;

Vue.use(BootstrapVue);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
