<template>
  <div class="competing-species-view">
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
      @selectedPreset="getPresetParams"
      @deletePreset="deletePreset"
      @changeN1_0="updateN1_0"
      @changer1="updater1"
      @changeK1="updateK1"
      @changea1="updatea1"
      @changeN2_0="updateN2_0"
      @changer2="updater2"
      @changeK2="updateK2"
      @changea2="updatea2"
      @tabOneActive="activateTabOne"
      @tabTwoActive="activateTabTwo"
    />
    <div class="rhs-page-component" style="margin-left: 25em">
      <!--Upon sucessful sign up, sign in or preset save-->
      <TempAlert :alert-message="alertMessage" :alert-variant="alertVariant" :show-alert="showAlert" :alert-secs="alertSecs" @resetAlert="resetSubmissionAlert" />
      <div class="top-section">
        <div class="title-and-formula">
          <h4 style="float: left">Two Competing Species Model</h4>
          <div class="formula">
            <katex-element expression="\Large\dfrac{dN_{1}}{dt}=r_{1}N_{1}(1-\dfrac{N_{1}+a_{1}N_{2}}{K_{1}})" />
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dN_{2}}{dt}=r_{2}N_{2}(1-\dfrac{N_{2}+a_{2}N_{1}}{K_{2}})" />
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            This model describes two species occupying the same habitat, which
            compete for shared and finite resources. Species 1 and 2 have populations
            <katex-element expression="N_{1}"/> and <katex-element expression="N_{2}"/>
            respectively. Within the habitat, each species exhibits its own carrying capacity,
            <katex-element expression="K"/>, which is the maximum species population
            that the environment's resources could sustain.
          </b-card-text>
          <b-card-text>
            The fate of each species depends on the paramaters assigned to the model. For a chosen
            configuration, try varying initial populations, <katex-element expression="N_{1, 0}"/> and
            <katex-element expression="N_{2, 0}"/>, and see how the populations evolve to their final state!
          </b-card-text>
        </ModelInfo>
      </div>
      <div class="sim-visualisation-section">
        <!--Use configuration file for bar chart-->
        <SimVisualiser
          @endSim="endSim"
          :chart-config="compSpecChartConfig"
          :vis-styling-class="visStylingClass"
          :initial-conditions="initialConditions"
          :sim-data="simData"
          :sim-time-data="simTimeData"
          :sim-max-val="simMaxVal"
          :time-units="timeUnits"
        />
      </div>
    </div>
    <div class="run-button">
      <span v-if="spinnerOn"> <b-spinner class="loadingSpinner"></b-spinner> </span>
      <b-button :variant="runVariant" pill @click="onClickRun">
        {{ runText }} <b-icon :icon="runIcon" scale="1.5" shift-v="1"></b-icon>
      </b-button>
    </div>
  </div>
</template>

<script>
import axios from "axios"; //For making client-side http requests
import TheNavBar from "@/components/TheNavBar/TheNavBar.vue";
import ConfigBar from "@/components/ConfigBar/ConfigBar.vue";
import ModelInfo from "@/components/common/ModelInfo.vue";
import TempAlert from "@/components/common/TempAlert.vue";
import SimVisualiser from "@/components/SimVisualiser/SimVisualiser.vue";
import compSpecChartConfig from "./CompetingSpeciesChartConfig.js";

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
        //Species 1
        N1_0: 20,
        r1: 0.1,
        K1: 20,
        a1: 0.1,
        //Species 2
        N2_0: 20,
        r2: 0.1,
        K2: 20,
        a2: 0.1
      },
      //Dynamic parameter array, containing params in their current state (initialised to default params)
      simParamData: [],
      barPlotN1_0: null,
      barPlotN2_0: null,
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
              label: "N_{1,0}",
              units: "",
              description: "Initial population of species 1 (time = 0)",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeN1_0",
              inputStep: 20,
              tickStep: 100,
              min: 0,
              max: 1000,
            },
            {
              label: "r_{1}",
              units: "(/yr)",
              description: "Growth rate of species 1 (birth rate - death rate)",
              emitEventName: "changer1",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
            {
              label: "K_{1}",
              units: "",
              description: "Carrying capacity of species 1 (Max population that environment could sustain)",
              emitEventName: "changeK1",
              inputStep: 20,
              tickStep: 100,
              min: 0,
              max: 1000,
            },
            {
              label: "a_{1}",
              units: "(/yr)",
              description: "Effect of species 2 on species 1",
              emitEventName: "changea1",
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
              label: "N_{2,0}",
              units: "",
              description: "Initial population of species 2 (time = 0)",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeN2_0",
              inputStep: 20,
              tickStep: 100,
              min: 0,
              max: 1000,
            },
            {
              label: "r_{2}",
              units: "(/yr)",
              description: "Growth rate of species 2 (birth rate - death rate)",
              emitEventName: "changer2",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
            {
              label: "K_{2}",
              units: "",
              description: "Carrying capacity of species 2 (Max population that environment could sustain)",
              emitEventName: "changeK2",
              inputStep: 20,
              tickStep: 100,
              min: 0,
              max: 1000,
            },
            {
              label: "a_{2}",
              units: "(/yr)",
              description: "Effect of species 1 on species 2",
              emitEventName: "changea2",
              inputStep: 0.1,
              tickStep: 0.2,
              min: 0,
              max: 2,
            },
          ],
          isActive: false,
        },
      ],
      configTabTitles: ["Species 1", "Species 2"],
      paramSuggestions: [
        {
          id: 1,
          text: "Weak competition between species (neither species goes extinct, regardless of \
            initial populations).",
          maths: "r_{1}=1.2,\\ K_{1}=500,\\ a_{1}=0.7,\\ \
            r_{2}=0.8,\\ K_{2}=500,\\ a_{2}=0.8"
        },
        {
          id: 2,
          text: "Unbalanced competition between species (species 1 always driven to extinction, \
            regardless of starting populations)",
          maths: "r_{1}=1,\\ K_{1}=700,\\ a_{1}=1.5,\\ \
            r_{2}=1,\\ K_{2}=500,\\ a_{2}=0.5"
        },
        {
          id: 3,
          text: "Strong competition between species (either species 1 or species 2 driven to \
            extinction, depending on initial populations. See for yourself by varying them!)",
          maths: "r_{1}=1,\\ K_{1}=500,\\ a_{1}=1.5,\\ \
            r_{2}=1,\\ K_{2}=500,\\ a_{2}=1.3"
        }
      ],
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: null,
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
      //For data visualisation
      compSpecChartConfig,
      visStylingClass: "comp-spec",
      //Default run simulation button config
      runIcon: "play",
      runVariant: "success",
      runText: "Run Simulation",
      spinnerOn: false
    };
  },
  computed: {
    //Access Vuex store containing active user info
    activeUser() {
      return this.$store.state.activeUser;
    },
    simRunning() {
      return this.$store.state.simRunning;
    },
    initialConditions() { //Array inherited by bar chart for reactive display
      return [this.barPlotN1_0, this.barPlotN2_0]
    },
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateN1_0(newN1_0) {
      if (newN1_0 == 0) newN1_0 = this.defaultParams.N1_0 //Non-zero params only, set to default if 0 encountered
      this.$set(this.simParamData, 0, newN1_0) //Inform Vue of an array element change
      this.barPlotN1_0 = newN1_0
      console.log(this.simParamData[0], "N1_0-change");
    },
    updater1(newr1) {
      if (newr1 == 0) newr1 = this.defaultParams.r1 //Non-zero params only
      this.$set(this.simParamData, 1, newr1) //Inform Vue of an array element change
      console.log(this.simParamData[1], "r1-change");
    },
    updateK1(newK1) {
      if (newK1 == 0) newK1 = this.defaultParams.K1 //Non-zero params only
      this.$set(this.simParamData, 2, newK1) //Inform Vue of an array element change
      console.log(this.simParamData[2], "K1-change");
    },
    updatea1(newa1) {
      if (newa1 == 0) newa1 = this.defaultParams.a1 //Non-zero params only
      this.$set(this.simParamData, 3, newa1) //Inform Vue of an array element change
      console.log(this.simParamData[3], "a1-change");
    },
    updateN2_0(newN2_0) {
      if (newN2_0 == 0) newN2_0 = this.defaultParams.N2_0 //Non-zero params only
      this.$set(this.simParamData, 4, newN2_0) //Inform Vue of an array element change
      this.barPlotN2_0 = newN2_0
      console.log(this.simParamData[4], "N2_0-change");
    },
    updater2(newr2) {
      if (newr2 == 0) newr2 = this.defaultParams.r2 //Non-zero params only
      this.$set(this.simParamData, 5, newr2) //Inform Vue of an array element change
      console.log(this.simParamData[5], "r2-change");
    },
    updateK2(newK2) {
      if (newK2 == 0) newK2 = this.defaultParams.K2 //Non-zero params only
      this.$set(this.simParamData, 6, newK2) //Inform Vue of an array element change
      console.log(this.simParamData[6], "K2-change");
    },
    updatea2(newa2) {
      if (newa2 == 0) newa2 = this.defaultParams.a2 //Non-zero params only
      this.$set(this.simParamData, 7, newa2) //Inform Vue of an array element change
      console.log(this.simParamData[7], "a2-change");
    },
    //Respond to emitted "change active parameter tab" events
    activateTabOne() {
      this.tabsData[0].isActive = true;
      this.tabsData[1].isActive = false;
      console.log("opened species 1 tab");
    },
    activateTabTwo() {
      this.tabsData[1].isActive = true;
      this.tabsData[0].isActive = false;
      console.log("opened species 2 tab");
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
    //Triggered upon a preset save
    async handlePresetName(presetName) {
      const presetPayload = {
        //Active user's email for database identification
        userEmail: this.activeUser.email,
        presetName: presetName,
        presetData: this.simParamData,
      };
      await this.addPreset(presetPayload);
      this.getAllPresets(); //Update presets list
    },
    async addPreset(payload) {
      try {
        const path = "http://localhost:5000/CompetingSpecies/AlterPresets";
        await axios.post(path, payload);
        const successAlertPayload = {
          message: `Saved ${payload.presetName} to Competing Species presets`,
          variant: "success",
        };
        this.showSubmissionAlert(successAlertPayload);
        console.log("Preset saved");
      } catch (error) {
        const failureAlertPayload = {
          message: "Unable to save preset, failed repsonse from server",
          variant: "danger",
        };
        this.showSubmissionAlert(failureAlertPayload);
        console.log("Preset not saved, server problem");
      }
    },
    //Bring user's presets to client-side
    async getAllPresets() {
      try {
        const path = "http://localhost:5000/CompetingSpecies/AllPresets";
        const payload = {
          userEmail: this.activeUser.email
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
        const path = `http://localhost:5000/CompetingSpecies/PresetParams/${presetid}`;
        const response = await axios.get(path);
        //Set sim data (and slider values) to preset data
        const presetParamsCount = 7;
        for(let i = 0; i <= presetParamsCount; i++) {
            this.simParamData[i] = Number(response.data["preset_params"][i])
        }
        //Set barplot initial value
        const N1_0Index = 0
        const N2_0Index = 4
        this.barPlotN1_0 = null //Change value for computed recalculation
        this.barPlotN1_0 = this.simParamData[N1_0Index]
        this.barPlotN2_0 = this.simParamData[N2_0Index]
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
        const path = `http://localhost:5000/CompetingSpecies/AlterPresets/${presetid}`;
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
        const path = "http://localhost:5000/CompetingSpecies/RunSim"
        const payload = {
          simParams: this.simParamData
        }
        this.spinnerOn = true
        const response = await axios.post(path, payload)
        this.simData = response.data["sim_data"] //Array of arrays, containing all sim data
        this.simTimeData = response.data["time_data"] //Times corresponding to sim's data
        this.simMaxVal = response.data["sim_max_val"] //Max value, for upper bound of visualisation's axis
        this.spinnerOn = false
        this.$store.commit("simRunningChange", true) //Signals to start visualising simulation
        console.log("Competing Species simulation successfully run at server")
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
      this.spinnerOn = false
      this.$store.commit("simRunningChange", false)
      this.runIcon = "play"
      this.runVariant = "success"
      this.runText = "Run Simulation"
    }
  },
  mounted() {
    if (this.activeUser.isActive) { //Don't load presets if no one is logged in
      this.getAllPresets()
    }
    //Set simulation params to default values
    this.simParamData.length = 8 //Number of params in this model
    this.simParamData[0] = this.defaultParams.N1_0
    this.simParamData[1] = this.defaultParams.r1
    this.simParamData[2] = this.defaultParams.K1
    this.simParamData[3] = this.defaultParams.a1
    this.simParamData[4] = this.defaultParams.N2_0
    this.simParamData[5] = this.defaultParams.r2
    this.simParamData[6] = this.defaultParams.K2
    this.simParamData[7] = this.defaultParams.a2
    //Set initial bar plot values, calling initialConditions computed property to be inherited by plot
    this.barPlotN1_0 = this.defaultParams.N1_0
    this.barPlotN2_0 = this.defaultParams.N2_0
  },
};
</script>

<style scoped>
.competing-species-view {
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
}
.loadingSpinner {
  margin-bottom: -9px;
  margin-right: 10px;
}
</style>
