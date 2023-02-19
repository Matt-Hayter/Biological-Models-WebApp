<template>
  <div class="SIR-view">
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
      @changeI0="updateI0"
      @changeBeta="updateBeta"
      @changeRecipGamma="updateRecipGamma"
    />
    <div class="rhs-page-component" style="margin-left: 25em">
      <!--Upon sucessful sign up, sign in or preset save-->
      <TempAlert :alert-message="alertMessage" :alert-variant="alertVariant" :show-alert="showAlert" :alert-secs="alertSecs" @resetAlert="resetSubmissionAlert" />
      <div class="top-section">
        <div class="title-and-formula">
          <h4 style="float: left">SIR Model</h4>
          <div class="formula">
            <katex-element expression="\Large\dfrac{dS}{dt}=-\beta \dfrac{SI}{N}"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dI}{dt}=\beta \dfrac{SI}{N} - \gamma I"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dR}{dt}=\gamma I"/>
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            The SIR model is a simplistic, classical model describing disease spread throughout a
            population. Individuals within the population exist in, and transition between,
            one of three states:
          </b-card-text>
          <b-card-text>
            <ul>
              <li>
                Susceptible (<katex-element expression="S"/>) - Indiduals that are able to catch
                the disease
              </li>
              <li>
                Infected (<katex-element expression="I"/>) - Individuals that currently have the disease
              </li>
              <li>
                Recovered (<katex-element expression="R"/>) - Individuals that previously had the disease,
                have recovered, and are now immune
              </li>
            </ul>
          </b-card-text>
          <b-card-text>
            In these simulations, a total population of 10 million individuals is used, and deaths are 
            included within the recovered group. All infected individuals are assumed to be infectious.
          </b-card-text>
        </ModelInfo>
      </div>
      <div class="sim-visualisation-section">
        <!--Use configuration file for bar chart-->
        <SimVisualiser
          @endSim="endSim"
          :chart-config="SIRChartConfig"
          :vis-styling-class="visStylingClass"
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
import SIRChartConfig from "./SIRChartConfig.js";

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
      totalPopulation: 10000000, //Tot. sim population. Should match backend simulation
      //Params initially at slider's min values (non-zero)
      defaultParams: {
        I0: 1, 
        beta: 0.05,
        recipGamma: 1
      },
      //Dynamic parameter array, containing params in their current state (initialised to default params)
      simParamData: [],
      barPlotS0: null, //For use in reactive bar chart
      barPlotI0: null,
      barPlotR0: 0,
      simRunning: false,
      simData: null, //Array of arrays, containing all sim data when obtained
      simTimeData: null, //Array containing times corresponding to simData
      simMaxVal: null, //Max value, for upper bound of visualisation's axis when obtained
      timeUnits: "days",
      //Contains user's presets
      userPresets: [],
      //Contains data for each paramater tab
      tabsData: [
        //Tab one
        {
          data: [
            {
              label: "I_{0}",
              units: "",
              description: "Initial number of infections",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeI0",
              inputStep: 500,
              tickStep: 5000,
              min: 0,
              max: 20000
            },
            {
              label: "\\beta",
              units: "(/day)",
              description: "Rate of infection (probability of disease transmission per contact x number of contacts per unit time)",
              emitEventName: "changeBeta",
              inputStep: 0.05,
              tickStep: 0.1,
              min: 0,
              max: 1,
            },
            {
              label: "1/ \\gamma",
              units: "(days)",
              description: "Average infectious period",
              emitEventName: "changeRecipGamma",
              inputStep: 1,
              tickStep: 2,
              min: 0,
              max: 20,
            },
          ],
          isActive: true, //Only tab, so always active
        },
      ],
      configTabTitles: [null], //No tabs needed
      paramSuggestions: [
        {
          id: 1,
          text: "Low/moderate infectiousness and small/moderate infectious period.",
          maths: "I_{0}=1,\\ \\beta=0.3,\\ 1/\\gamma=4"
        },
        {
          id: 2,
          text: "High infectiousness and large infectious period.",
          maths: "I_{0}=1,\\ \\beta=1,\\ 1/\\gamma=14"
        },
        {
          id: 3,
          text: "High infectiousness and small infectious period.",
          maths: "I_{0}=1,\\ \\beta=1,\\ 1/\\gamma=2"
        },
        {
          id: 4,
          text: "Low infectiousness and large infectious period.",
          maths: "I_{0}=1,\\ \\beta=0.2,\\ 1/\\gamma=14"
        },
      ],
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: null,
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
      //For data visualisation
      SIRChartConfig,
      visStylingClass: "SIR",
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
      return [this.barPlotS0, this.barPlotI0, this.barPlotR0]
    },
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateI0(newI0) {
      if (newI0 == 0) newI0 = this.defaultParams.I0 //Non-zero params only, set to default if 0 encountered
      this.$set(this.simParamData, 0, newI0) //Inform Vue of an array element change
      this.barPlotI0 = newI0
      this.I0UpdateS0()
      console.log(this.simParamData[0], "I0-change");
    },
    updateBeta(newBeta) {
      if (newBeta == 0) newBeta = this.defaultParams.beta //Non-zero params only
      this.$set(this.simParamData, 1, newBeta) //Inform Vue of an array element change
      console.log(this.simParamData[1], "beta-change");
    },
    updateRecipGamma(newRecipGamma) {
      if (newRecipGamma == 0) newRecipGamma = this.defaultParams.recipGamma //Non-zero params only
      this.$set(this.simParamData, 2, newRecipGamma) //Inform Vue of an array element change
      console.log(this.simParamData[2], "1/gamma-change");
    },
    //Change S0 upon change of I0 (must sum to total population)
    I0UpdateS0() {
      const I0ParamIndex = 0;
      this.barPlotS0 = this.totalPopulation - this.simParamData[I0ParamIndex]
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
        const path = "http://localhost:5000/SIR/AlterPresets";
        await axios.post(path, payload);
        const successAlertPayload = {
          message: `Added ${payload.presetName} to SIR presets`,
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
        const path = "http://localhost:5000/SIR/AllPresets";
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
        const path = `http://localhost:5000/SIR/PresetParams/${presetid}`;
        const response = await axios.get(path);
        //Set sim data (and slider values) to preset data
        const presetParamsCount = 2;
        for(let i = 0; i <= presetParamsCount; i++) {
            this.simParamData[i] = Number(response.data["preset_params"][i])
        }
        //Set barplot initial value
        const I0ParamIndex = 0
        this.barPlotI0 = null //Change value for computed recalculation
        this.barPlotI0 = this.simParamData[I0ParamIndex]
        this.barPlotS0 = this.totalPopulation - this.barPlotI0
        console.log(this.barPlotS0)
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
        const path = `http://localhost:5000/SIR/AlterPresets/${presetid}`;
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
        const path = "http://localhost:5000/SIR/RunSim"
        const payload = {
          simParams: this.simParamData
        }
        const response = await axios.post(path, payload)
        this.simData = response.data["sim_data"] //Array of arrays, containing all sim data
        this.simTimeData = response.data["time_data"] //Times corresponding to sim's data
        this.simMaxVal = response.data["sim_max_val"] //Max value, for upper bound of visualisation's axis
        this.simRunning = true //Signals to start visualising simulation
        console.log("SIR simulation successfully run at server")
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
    this.simParamData.length = 3 //Number of params in this model
    this.simParamData[0] = this.defaultParams.I0
    this.simParamData[1] = this.defaultParams.beta
    this.simParamData[2] = this.defaultParams.recipGamma
    //Set initial bar plot values, calling initialConditions computed property to be inherited by plot
    this.barPlotI0 = this.defaultParams.I0
    this.barPlotS0 = this.totalPopulation - this.barPlotI0
  },
};
</script>

<style scoped>
.SIR-view {
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
  padding-left: 21em;
}
.run-button {
  position: fixed;
  margin-right: 1em;
  margin-bottom: 1em;
  bottom: 0;
  right: 0;
  color: rgb(rgb(255, 225, 0), green, blue)
}
</style>
