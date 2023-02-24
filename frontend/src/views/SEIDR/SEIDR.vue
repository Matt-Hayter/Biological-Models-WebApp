<template>
  <div class="SEIDR-view">
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
      @changeAlpha="updateAlpha"
      @changeBeta="updateBeta"
      @changeRecipGamma="updateRecipGamma"
      @changeRecipEpsilon="updateRecipEpsilon"
      @changeE0="updateE0"
      @changeI0="updateI0"
      @tabOneActive="activateTabOne"
      @tabTwoActive="activateTabTwo"
    />
    <div class="rhs-page-component" style="margin-left: 25em">
      <div class="alert-section">
        <!--Upon sucessful sign up, sign in or preset save-->
        <TempAlert
          class="alert"
          :alert-message="alertMessage"
          :alert-variant="alertVariant"
          :show-alert="showAlert"
          :alert-secs="alertSecs"
          @resetAlert="resetSubmissionAlert"
        />
      </div>
      <div class="top-section">
        <div class="title-and-formula">
          <div class="title">
            <h4>SEIDR Model</h4>
            <p>(J. M. Carcione et al.)</p>
          </div>
          <div class="formula">
            <katex-element expression="\Large\dfrac{dS}{dt}=\Lambda-\mu S - \beta \dfrac{SI}{N}"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dE}{dt}=\beta \dfrac{SI}{N} - (\mu + \epsilon)E"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dI}{dt}=\epsilon E - (\gamma + \mu + \alpha)I"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dD}{dt}=\alpha I"/>
            <br>
            <br>
            <katex-element expression="\Large\dfrac{dR}{dt}=\gamma I - \mu R"/>
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            This model is an extension of the classical SIR model of disease spread. Its increased
            complexity allows for more accurate modelling of real life events, such as the spread
            of COVID-19 within a population. Individuals within the population exist in, and transition
            between, one of five states:
          </b-card-text>
          <b-card-text>
            <ul>
              <li>
                Susceptible (<katex-element expression="S"/>) - Indiduals that are able to catch
                the disease
              </li>
              <li>
                Exposed (<katex-element expression="E"/>) - Indiduals that are infected but not yet
                contagious
              </li>
              <li>
                Infectious (<katex-element expression="I"/>) - Indiduals that are infected and
                are contagious
              </li>
              <li>
                Dead (<katex-element expression="D"/>) - Indiduals that were infectious and have now died
                from the disease
              </li>
              <li>
                Recovered (<katex-element expression="R"/>) - Individuals that previously had the disease,
                have recovered, and are now immune
              </li>
            </ul>
          </b-card-text>
          <b-card-text>
            <katex-element expression="\Lambda ="/> population birth rate,
            <katex-element expression="\mu ="/> rate of natural death per indivdual. Here,
            simulations use a balanced number of births and natural deaths,
            <katex-element expression="\Lambda=\mu N"/>, hence they are not configurable.
          </b-card-text>
          <b-card-text>
            <b>Model source</b>: J. M. Carcione at al., A Simulation of a COVID-19 Epidemic Based on a
            Deterministic SEIR Model, 2020
          </b-card-text>
        </ModelInfo>
      </div>
      <div class="sim-visualisation-section">
        <!--Use configuration file for bar chart-->
        <SimVisualiser
          @endSim="endSim"
          :chart-config="SEIDRChartConfig"
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
import SEIDRChartConfig from "./SEIDRChartConfig.js";

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
      totalPopulation: 10000000, //Tot. sim population
      //Params initially at slider's min values (non-zero)
      defaultParams: {
        //Rates
        alpha: 0.001,
        beta: 0.05,
        recipGamma: 1,
        recipEpsilon: 0.5,
        //Initial conditions
        E0: 1,
        I0: 1,
      },
      //Dynamic parameter array, containing params in their current state (initialised to default params)
      simParamData: [],
      //For use in reactive bar chart
      barPlotS0: null,
      barPlotE0: null,
      barPlotI0: null,
      barPlotD0: 0,
      barPlotR0: 0,
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
              label: "\\alpha",
              units: "(/day)",
              description: "Disease induced average lethality rate",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeAlpha",
              inputStep: 0.001,
              tickStep: 0.04,
              min: 0,
              max: 0.2
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
            {
              label: "1/ \\epsilon",
              units: "(days)",
              description: "Average incubation period (period between exposure to disease and appearence of first sympotoms)",
              emitEventName: "changeRecipEpsilon",
              inputStep: 1,
              tickStep: 2,
              min: 0,
              max: 20,
            },
          ],
          isActive: true,
        },
        //Tab two
        {
          data: [
            {
              label: "E_{0}",
              units: "",
              description: "Initial exposed population",
              emitEventName: "changeE0",
              inputStep: 500,
              tickStep: 5000,
              min: 0,
              max: 20000
            },
            {
              label: "I_{0}",
              units: "",
              description: "Initial infectious population",
              emitEventName: "changeI0",
              inputStep: 500,
              tickStep: 5000,
              min: 0,
              max: 20000
            },
          ],
          isActive: false,
        },
      ],
      configTabTitles: ["Rates", "Initial Conditions"],
      paramSuggestions: [
        {
          id: 1,
          text: "COVID-19, no isolation.",
          maths: "\\alpha=0.006,\\ \\beta=0.75,\\ 1/\\gamma=8,\\ 1/\\epsilon=3,\\, \
            E_{0}=20000,\\, I_{0}=1"
        },
        {
          id: 2,
          text: "COVID-19, isolation measures in place.",
          maths: "\\alpha=0.006,\\ \\beta=0.2,\\ 1/\\gamma=8,\\ 1/\\epsilon=3,\\, \
            E_{0}=20000,\\, I_{0}=1"
        },
        {
          id: 3,
          text: "Highly lethal disease.",
          maths: "\\alpha=0.125,\\ \\beta=0.5,\\ 1/\\gamma=8,\\ 1/\\epsilon=3,\\, \
            E_{0}=20000,\\, I_{0}=1"
        },
        {
          id: 4,
          text: "Using suggestion 1 (no isolation COVID) as a base, play around with different parameters \
            and observe the effects on the spread of the disease",
          maths: ""
        },
      ],
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: null,
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
      //For data visualisation
      SEIDRChartConfig,
      visStylingClass: "SEIDR",
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
      return [this.barPlotS0, this.barPlotE0, this.barPlotI0, this.barPlotD0, this.barPlotR0]
    },
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateAlpha(newAlpha) {
      if (newAlpha == 0) newAlpha = this.defaultParams.alpha //Non-zero params only, set to default if 0 encountered
      this.$set(this.simParamData, 0, newAlpha) //Inform Vue of an array element change
      console.log(this.simParamData[0], "alpha-change");
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
    updateRecipEpsilon(newRecipEpsilon) {
      if (newRecipEpsilon == 0) newRecipEpsilon = this.defaultParams.recipGamma //Non-zero params only
      this.$set(this.simParamData, 3, newRecipEpsilon) //Inform Vue of an array element change
      console.log(this.simParamData[3], "1/epsilon-change");
    },
    updateE0(newE0) {
      if (newE0 == 0) newE0 = this.defaultParams.E0 //Non-zero params only
      this.$set(this.simParamData, 4, newE0) //Inform Vue of an array element change
      this.barPlotE0 = newE0
      this.E0I0UpdateS0()
      console.log(this.simParamData[4], "E0-change");
    },
    updateI0(newI0) {
      if (newI0 == 0) newI0 = this.defaultParams.I0 //Non-zero params only
      this.$set(this.simParamData, 5, newI0) //Inform Vue of an array element change
      this.barPlotI0 = newI0
      this.E0I0UpdateS0()
      console.log(this.simParamData[5], "I0-change");
    },
    E0I0UpdateS0() {
      const E0ParamIndex = 4;
      const I0ParamIndex = 5;
      this.barPlotS0 = this.totalPopulation - this.simParamData[E0ParamIndex]
        - this.simParamData[I0ParamIndex] //D0, R0 = 0
    },
    //Respond to emitted "change active parameter tab" events
    activateTabOne() {
      this.tabsData[0].isActive = true;
      this.tabsData[1].isActive = false;
      console.log("opened params tab");
    },
    activateTabTwo() {
      this.tabsData[1].isActive = true;
      this.tabsData[0].isActive = false;
      console.log("opened initial conditions tab");
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
        console.log(payload.presetData)
        const path = "http://localhost:5000/SEIDR/AlterPresets";
        await axios.post(path, payload);
        const successAlertPayload = {
          message: `Added ${payload.presetName} to SEIDR presets`,
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
        const path = "http://localhost:5000/SEIDR/AllPresets";
        const payload = {
          userEmail: this.activeUser.email
        };
        const response = await axios.post(path, payload) //Identify user with email
        this.userPresets = response.data["presets"] //Update frontend presets with those in database
        console.log("Loaded user's SEIDR presets")
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
        const path = `http://localhost:5000/SEIDR/PresetParams/${presetid}`;
        const response = await axios.get(path);
        //Set sim data (and slider values) to preset data
        const presetParamsCount = 5;
        for(let i = 0; i <= presetParamsCount; i++) {
            this.simParamData[i] = Number(response.data["preset_params"][i])
        }
        //Set barplot initial values
        const E0ParamIndex = 4
        const I0ParamIndex = 5
        this.barPlotE0 = null //Change value for computed recalculation
        this.barPlotE0 = this.simParamData[E0ParamIndex]
        this.barPlotI0 = this.simParamData[I0ParamIndex]
        this.barPlotS0 = this.totalPopulation - this.barPlotE0 - this.barPlotI0 //D0 and R0 = 0
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
        const path = `http://localhost:5000/SEIDR/AlterPresets/${presetid}`;
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
        const path = "http://localhost:5000/SEIDR/RunSim"
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
        console.log("SEIDR simulation successfully run at server")
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
    this.simParamData.length = 6 //Number of params in this model
    this.simParamData[0] = this.defaultParams.alpha
    this.simParamData[1] = this.defaultParams.beta
    this.simParamData[2] = this.defaultParams.recipGamma
    this.simParamData[3] = this.defaultParams.recipEpsilon
    this.simParamData[4] = this.defaultParams.E0
    this.simParamData[5] = this.defaultParams.I0
    //Set initial bar plot values, calling initialConditions computed property to be inherited by plot
    this.barPlotE0 = this.defaultParams.E0
    this.barPlotI0 = this.defaultParams.I0
    this.barPlotS0 = this.totalPopulation - this.barPlotE0 - this.barPlotI0 //D0, R0 = 0
  },
};
</script>

<style scoped>
.SEIDR-view {
  /*Slightly larger to encompass longer equations*/
  min-width: 1050px;
}
.top-section {
  display: flex;
  flex-direction: column;
}
.title-and-formula {
  padding-top: 2em;
  padding-left: 1.5em;
}
.title {
  float: left;
  display: flex;
  flex-direction: column;
}
.title-and-formula .formula {
  float: left;
  padding-left: 17em;
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
.alert-section {
  display: flex;
  justify-content: right;
}
.alert-section .alert {
  position: fixed;
  z-index: 1;
  width: 35%;
}
</style>

