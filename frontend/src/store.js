//Vuex state management

import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

//For storing Vuex state between page refreshes (locally)
const vuexLocal = new VuexPersistence({
  key: "user",
  storage: window.localStorage, //5Mb local storage
  reducer: (state) => ({ activeUser: state.activeUser }), //State properties required after refresh
});

export const store = new Vuex.Store({
  state: {
    activeUser: {
      isActive: false,
      username: null,
      email: null,
    },
    simRunning: false
  },
  mutations: {
    //Updating user credentials upon sign in/out
    userUpdate(state, payload) {
      state.activeUser.isActive = payload.isActive;
      state.activeUser.username = payload.username;
      state.activeUser.email = payload.email;
    },
    //Update simulation visualisation state
    simRunningChange(state, isRunning) {
      state.simRunning = isRunning;
    }
  },
  plugins: [
    vuexLocal.plugin, //Store state between page refreshes
  ],
});
