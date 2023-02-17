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
      :simRunning="simRunning"
      @showPageAlert="showSubmissionAlert"
      @presetNameInput="handlePresetName"
      @selectedPreset="getPresetParams"
      @deletePreset="deletePreset"
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
          <h4 style="float: left">Predator-Prey (Lotka-Volterra) Model</h4>
          <div class="formula">
            <katex-element expression="\Large\dfrac{dN}{dt}=N(a-bP)"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dP}{dt}=P(cN-d)"/>
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            The Lotka-Volterra model is a simple model describing variation in the populations of a
            prey species (<katex-element expression="N"/>) hunted by a predator species (<katex-element expression="P"/>).
            Solutions are oscillatory in nature,
            with an increase in prey population not only driving more prey reproduction, but also
            increasing predation.
          </b-card-text>
          <b-card-text>
            This model assumes that prey populations can always bounce back,
            even from extremely low populations. This, as we know, isn't usually the case, and
            prey can infact be hunted to extinction. Other assumptions include that there is no
            shortage of food for the prey, and that the environment is constant.
          </b-card-text>
        </ModelInfo>
      </div>
      <div class="sim-visualisation-section">
        <!--Use configuration file for bar chart-->
        <SimVisualiser
          @endSim="endSim"
          :chart-config="predPreyChartConfig"
          :initial-conditions="initialConditions"
          :sim-running="simRunning"
          :sim-data="simData"
          :sim-time-data="simTimeData"
          :sim-max-val="simMaxVal"
          :time-units="timeUnits"
        />
      </div>
    </div>
    <b-button class="run-button" :variant="runVariant" pill @click="onClickRun">
      {{ runText }} <b-icon :icon="runIcon" scale="1.5" shift-v="1"></b-icon>
    </b-button>
  </div>
</template>

<script>
import axios from "axios"; //For making client-side http requests
import TheNavBar from "@/components/TheNavBar/TheNavBar.vue";
import ConfigBar from "@/components/ConfigBar/ConfigBar.vue";
import ModelInfo from "@/components/common/ModelInfo.vue";
import TempAlert from "@/components/common/TempAlert.vue";
import SimVisualiser from "@/components/SimVisualiser/SimVisualiser.vue";
import predPreyChartConfig from "./PredPreyChartConfig.js";

export default {
  components: {
    TheNavBar,
    ConfigBar,
    ModelInfo,
    TempAlert,
    SimVisualiser,
  },
  data() {
    return {
      //Params initially at slider's min values (non-zero)
      defaultParams: {
        //Prey
        N0: 0.5,
        a: 0.1,
        b: 0.1,
        //Predator
        P0: 0.5,
        c: 0.05,
        d: 0.1
      },
      //Dynamic parameter array, containing params in their current state (initialised to default params)
      simParamData: [],
      barPlotN0: null, //For use in reactive bar chart.
      barPlotP0: null,
      simRunning: false,
      simData: null, //Array of arrays, containing all sim data when obtained
      simTimeData: null, //Array containing times corresponding to simData
      simMaxVal: null, //Max value, for upper bound of visualisation's axis when obtained
      timeUnits: "years",
      //Contains user's presets
      userPresets: [],
      //Contains data for each paramater tab
      tabsData: [
        //Tab one
        {
          data: [
            {
              label: "N_{0}",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeN0",
              inputStep: 0.5,
              tickStep: 1,
              min: 0,
              max: 10,
            },
            {
              label: "a",
              emitEventName: "changea",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
            {
              label: "b",
              emitEventName: "changeb",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
          ],
          isActive: true,
        },
        //Tab two
        {
          data: [
            {
              label: "P_{0}",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeP0",
              inputStep: 0.5,
              tickStep: 1,
              min: 0,
              max: 10,
            },
            {
              label: "c",
              emitEventName: "changec",
              inputStep: 0.05,
              tickStep: 0.1,
              min: 0,
              max: 1,
            },
            {
              label: "d",
              emitEventName: "changed",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
          ],
          isActive: false,
        },
      ],
      configTabTitles: ["Prey", "Predator"],
      paramSuggestions: [
        {
          id: 1,
          text: "Steady variations between predator and prey populations",
          maths: "N_{0}=2,\\ a=1.2,\\ b=1,\\ P_{0}=1,\\ c=0.6,\\ d=1"
        },
        {
          id: 2,
          text: "Lots of natural prey births and predator deaths, minimal effects from predation.",
          maths: "N_{0}=1,\\ a=2,\\ b=0.1,\\ P_{0}=1,\\ c=0.05,\\ d=2",
        },
        {
          id: 3,
          text: "Heavy predation effects, little natural prey births and predator deaths.",
          maths: "N_{0}=10,\\ a=0.4,\\ b=2,\\ P_{0}=1,\\ c=1,\\ d=0.4",
        },
      ],
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: null,
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
      //For data visualisation
      predPreyChartConfig,
      //Default run simulation button config
      runIcon: "play",
      runVariant: "success",
      runText: "Run Simulation",
    };
  },
  computed: {
    //Access Vuex store containing active user info
    activeUser() {
      return this.$store.state.activeUser;
    },
    initialConditions() { //Array inherited by bar chart for reactive display
      return [this.barPlotN0, this.barPlotP0]
    }
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateN0(newN0) {
      if (newN0 == 0) newN0 = this.defaultParams.N0 //Non-zero params only, set to default if 0 encountered
      this.$set(this.simParamData, 0, newN0) //Inform Vue of an array element change
      this.barPlotN0 = newN0;
      console.log(this.simParamData[0], "N0-change");
    },
    updatea(newa) {
      if (newa == 0) newa = this.defaultParams.a //Non-zero params only
      this.$set(this.simParamData, 1, newa) //Inform Vue of an array element change
      console.log(this.simParamData[1], "a-change");
    },
    updateb(newb) {
      if (newb == 0) newb = this.defaultParams.b //Non-zero params only
      this.$set(this.simParamData, 2, newb) //Inform Vue of an array element change
      console.log(this.simParamData[2], "b-change");
    },
    updateP0(newP0) {
      if (newP0 == 0) newP0 = this.defaultParams.P0 //Non-zero params only
      this.$set(this.simParamData, 3, newP0) //Inform Vue of an array element change
      this.barPlotP0 = newP0;
      console.log(this.simParamData[3], "P0-change");
    },
    updatec(newc) {
      if (newc == 0) newc = this.defaultParams.c //Non-zero params only
      this.$set(this.simParamData, 4, newc) //Inform Vue of an array element change
      console.log(this.simParamData[4], "c-change");
    },
    updated(newd) {
      if (newd == 0) newd = this.defaultParams.d //Non-zero params only
      this.$set(this.simParamData, 5, newd) //Inform Vue of an array element change
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
    async handlePresetName(presetName) {
      const presetPayload = {
        //Active user's email for database identification
        userEmail: this.$store.state.activeUser.email,
        presetName: presetName,
        presetData: this.simParamData,
      };
      await this.addPreset(presetPayload);
      this.getAllPresets(); //Update presets list
    },
    async addPreset(payload) {
      try {
        const path = "http://localhost:5000/PredPrey/AlterPresets";
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
    //Upon selecting a preset, get params from server
    async getPresetParams(presetIndex) {
      try {
        const presetid = this.userPresets[presetIndex][0] //Identify preset
        const path = `http://localhost:5000/PredPrey/PresetParams/${presetid}`;
        const response = await axios.get(path);
        //Set sim data (and slider values) to preset data
        const presetParamsCount = 5;
        for(let i = 0; i <= presetParamsCount; i++) {
            this.simParamData[i] = Number(response.data["preset_params"][i])
        }
        //Set barplot initial value
        const N0Index = 0
        const P0Index = 3
        this.barPlotN0 = this.simParamData[N0Index]
        this.barPlotP0 = this.simParamData[P0Index]
        const successAlertPayload = {
          message: `Loaded ${this.userPresets[presetIndex][1]} preset`,
          variant: "success",
        };
        this.showSubmissionAlert(successAlertPayload);
        console.log("Preset loaded");
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
    },
    async deletePreset(presetIndex) {
      try {
        const presetid = this.userPresets[presetIndex][0] //Identify preset (non-sensitive -> use key)
        const path = `http://localhost:5000/PredPrey/AlterPresets/${presetid}`;
        await axios.delete(path);
        const deletedAlertPayload = {
          message: `Deleted ${this.userPresets[presetIndex][0]} preset`,
          variant: "dark",
        };
        this.getAllPresets();
        this.showSubmissionAlert(deletedAlertPayload);
        console.log("Preset deleted");
      } catch (error) {
        const failureAlertPayload = {
          message: "Unable to delete preset, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Preset not loaded, server problem");
      }
    },
    onClickRun() { //Run/stop simulation button pressed
      if (this.simRunning == false) {
        this.runIcon = "stop"
        this.runVariant = "danger"
        this.runText = "Stop"
        this.runSim()
      } else {
        this.endSim()
      }
    },
    async runSim() {
      try {
        const path = "http://localhost:5000/PredPrey/RunSim"
        const payload = {
          simParams: this.simParamData
        }
        const response = await axios.post(path, payload)
        this.simData = response.data["sim_data"] //Array of arrays, containing all sim data
        this.simTimeData = response.data["time_data"] //Times corresponding to sim's data
        this.simMaxVal = response.data["sim_max_val"] //Max value, for upper bound of visualisation's axis
        this.simRunning = true //Signals to start visualising simulation
        console.log("Pred Prey simulation successfully run at server")
      } catch (error) {
        this.endSim() //Reset button
        const failureAlertPayload = {
          message: "Unable to run simulation, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Simulation error, server problem");
      }
    },
    endSim() {
      this.simRunning = false
      this.runIcon = "play"
      this.runVariant = "success"
      this.runText = "Run Simulation"
    }
  },
  mounted() {
    if (this.$store.state.activeUser.isActive) { //Don't load presets if no one is logged in
      this.getAllPresets()
    }
    //Set simulation params to default values
    this.simParamData.length = 6 //Number of params in this model
    this.simParamData[0] = this.defaultParams.N0
    this.simParamData[1] = this.defaultParams.a
    this.simParamData[2] = this.defaultParams.b
    this.simParamData[3] = this.defaultParams.P0
    this.simParamData[4] = this.defaultParams.c
    this.simParamData[5] = this.defaultParams.d
    //Set initial bar plot values, calling initialConditions computed property to be inherited by plot
    this.barPlotN0 = this.defaultParams.N0
    this.barPlotP0 = this.defaultParams.P0
  },
};
</script>

<style scoped>
.predator-prey-view {
  min-width: 1024px;
}
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
.run-button {
  position: fixed;
  margin-right: 1em;
  margin-bottom: 1em;
  bottom: 0;
  right: 0;
  z-index: 2;
}
</style>
