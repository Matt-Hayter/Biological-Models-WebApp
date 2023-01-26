<template>
  <div class="predator-prey-view">
    <TheNavBar 
      @showPageAlert="showSubmissionAlert"
      @loadPresets="getAllPresets"
      @initPresets="initPresets"
      />
    <!--Pass props to child component and handle emitted events for configuration bar-->
    <ConfigBar
      :tabs-data="tabsData"
      :config-tab-titles="configTabTitles"
      :param-suggestions="paramSuggestions"
      :sim-param-data="simParamData"
      :user-presets="userPresets"
      @showPageAlert="showSubmissionAlert"
      @presetNameInput="handlePresetName"
      @selectedPreset="onClickPreset"
      @changeN0="updateN0"
      @changea="updatea"
      @changeb="updateb"
      @changeP0="updateP0"
      @changec="updatec"
      @changed="updated"
      @tabOneActive="activateTabOne"
      @tabTwoActive="activateTabTwo"
    />
    <div class="rhs-page-component" style="margin-left: 25em">
      <!--Upon sucessful sign up, sign in or preset save-->
      <TempAlert :alert-message="alertMessage" :alert-variant="alertVariant" :show-alert="showAlert" :alert-secs="alertSecs" @resetAlert="resetSubmissionAlert" />
      <div class="top-section">
        <div class="title-and-formula">
          <h4 class="tex2jax_ignore" style="float: left">Predator-Prey (Lotka-Voltera) Model</h4>
          <div class="formula">
            <vue-mathjax formula="$$\Large\frac{dN}{dt}=N(a-bP)$$"></vue-mathjax>
            <br>
            <vue-mathjax formula="$$\Large\frac{dP}{dt}=P(cN-d)$$"></vue-mathjax>
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            Some text
          </b-card-text>
          <b-card-text>
            Some more text
          </b-card-text>
        </ModelInfo>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"; //For making client-side http requests
import TheNavBar from "@/components/TheNavBar/TheNavBar.vue";
import ConfigBar from "@/components/ConfigBar/ConfigBar.vue";
import ModelInfo from "@/components/common/ModelInfo.vue";
import TempAlert from "@/components/common/TempAlert.vue";

export default {
  components: {
    TheNavBar,
    ConfigBar,
    ModelInfo,
    TempAlert,
  },
  data() {
    return {
      //Params initially at slider's min values
      simParamData: [
        //Prey
        10, //N0
        10, //a
        1, //b
        //Predator
        10, //P0
        10, //c
        1, //d
      ],
      //Contains user's presets
      userPresets: [],
      //Contains data for each paramater tab
      tabsData: [
        //Tab one
        {
          data: [
            {
              label: "$N_{0}$",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeN0",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "$a$",
              emitEventName: "changea",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "$b$",
              emitEventName: "changeb",
              min: 1,
              max: 10,
              step: 1,
            },
          ],
          isActive: true,
        },
        //Tab two
        {
          data: [
            {
              label: "$P_{0}$",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeP0",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "$c$",
              emitEventName: "changec",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "$d$",
              emitEventName: "changed",
              min: 1,
              max: 10,
              step: 1,
            },
          ],
          isActive: false,
        },
      ],
      configTabTitles: ["Prey", "Predator"],
      paramSuggestions: [
        {
          id: 1,
          content: "This is the first suggestions. This willl caryry on here",
        },
        {
          id: 2,
          content:
            "Tklsnf dlzk zldfjilzdjf if jzidjlwd  djdlzidld jzd zld jzd jzldldji",
        },
      ],
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: null,
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
    };
  },
  computed: {
    //Access Vuex store containing active user info
    activeUser() {
      return this.$store.state.activeUser;
    },
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateN0(newN0) {
      this.simParamData[0] = newN0;
      console.log(this.simParamData[0], "N0-change");
    },
    updatea(newa) {
      this.simParamData[1] = newa;
      console.log(this.simParamData[1], "a-change");
    },
    updateb(newb) {
      this.simParamData[2] = newb;
      console.log(this.simParamData[2], "b-change");
    },
    updateP0(newP0) {
      this.simParamData[3] = newP0;
      console.log(this.simParamData[3], "P0-change");
    },
    updatec(newc) {
      this.simParamData[4] = newc;
      console.log(this.simParamData[4], "c-change");
    },
    updated(newd) {
      this.simParamData[5] = newd;
      console.log(this.simParamData[5], "d-change");
    },
    //Respond to emitted "change active parameter tab" events
    activateTabOne() {
      this.tabsData[0].isActive = true;
      this.tabsData[1].isActive = false;
      console.log("opened prey tab");
    },
    activateTabTwo() {
      this.tabsData[1].isActive = true;
      this.tabsData[0].isActive = false;
      console.log("opened predator tab");
    },
    //Recieve alert varient change
    alertVariantChanged(incomingVariant) {
      this.alertVariant = incomingVariant;
    },
    showSubmissionAlert(submissionObj) {
      this.showAlert = true;
      this.alertMessage = submissionObj.message;
      this.alertVariant = submissionObj.variant;
    },
    resetSubmissionAlert() {
      this.showAlert = false;
    },
    activateUsername(username) {
      this.activeUsername = username;
    },
    activateEmail(email) {
      this.activeEmail = email;
    },
    //Triggered upon a preset save
    handlePresetName(presetName) {
      const presetPayload = {
        //Active user's email for database identification
        userEmail: this.$store.state.activeUser.email,
        presetName: presetName,
        presetData: this.simParamData,
      };
      this.addPreset(presetPayload);
      this.getAllPresets(); //Update presets list
    },
    async addPreset(payload) {
      try {
        const path = "http://localhost:5000/PredPrey/AddPresets";
        await axios.post(path, payload);
        const successAlertPayload = {
          message: `Added ${payload.presetName} to Predator-Prey presets`,
          variant: "success",
        };
        this.showSubmissionAlert(successAlertPayload);
        console.log("Preset added");
      } catch (error) {
        const failureAlertPayload = {
          message: "Unable to save preset, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Preset not added, server problem");
      }
    },
    //Bring user's presets to client-side
    async getAllPresets() {
      try {
        const path = "http://localhost:5000/PredPrey/AllPresets";
        const payload = {
          userEmail: this.$store.state.activeUser.email
        };
        const response = await axios.post(path, payload) //Identify user with email
        this.userPresets = response.data["presets"] //Update frontend presets with those in database
        console.log("Loaded user's Pred-Prey presets")
      } catch (error) {
        //Only show alert upon failure
        const failureAlertPayload = {
          message: "Unable to fetch presets, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Presets not loaded, server problem");
      }
    },
    //User has selected a preset from dropdown
    onClickPreset(presetIndex) {
      const payload = { //Unique data required to extract preset data
        userEmail: this.$store.state.activeUser.email, //Identify user
        presetName: this.userPresets[presetIndex][0] //Identify preset
      }
      this.getPresetParams(payload)
    },
    //Upon selecting a preset, get params from server
    async getPresetParams(payload) {
      try {
        const path = "http://localhost:5000/PredPrey/PresetParams";
        const response = await axios.post(path, payload);
        //Set sim data (and slider values) to preset data
        this.simParamData[0] = Number(response.data["preset_params"][0]); //N0
        this.simParamData[1] = Number(response.data["preset_params"][1]); //a
        this.simParamData[2] = Number(response.data["preset_params"][2]); //b
        this.simParamData[3] = Number(response.data["preset_params"][3]); //P0
        this.simParamData[4] = Number(response.data["preset_params"][4]); //c
        this.simParamData[5] = Number(response.data["preset_params"][5]); //d
        const successAlertPayload = {
          message: `Loaded ${payload.presetName} preset`,
          variant: "success",
        };
        console.log(this.simParamData)
        this.showSubmissionAlert(successAlertPayload);
        console.log("Preset added");
      } catch (error) {
        const failureAlertPayload = {
          message: "Unable to load preset, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Preset not loaded, server problem");
      }
    },
    initPresets() { //Clear presets
      this.userPresets = []
    }
  },
  mounted() {
    if (this.$store.state.activeUser.isActive) { //Don't load presets if no one is logged in
      this.getAllPresets()
    }
  },
};
</script>

<style>
.top-section {
  display: flex;
  flex-direction: column;
}
.title-and-formula {
  padding-top: 2em;
  padding-left: 1.5em;
}
.title-and-formula .formula {
  float: left;
  padding-left: 9em;
}
</style>
