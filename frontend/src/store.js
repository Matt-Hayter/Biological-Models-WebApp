//Vuex state management

import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

//For storing Vuex state between page refreshes (locally)
const vuexLocal = new VuexPersistence({
  key: "user",
  storage: window.localStorage, //5Mb local storage
  reducer: (state) => ({ user: state.user }), //State properties required after refresh
});

export const store = new Vuex.Store({
  state: {
    user: {
      isActive: false,
      username: null,
      email: null,
    },
    simRunning: false
  },
  mutations: {
    //Updating user credentials upon sign in/out
    userUpdate(state, payload) {
      state.user.isActive = payload.isActive;
      state.user.username = payload.username;
      state.user.email = payload.email;
    },
    usernameUpdate(state, newUsername) {
      state.user.username = newUsername;
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
