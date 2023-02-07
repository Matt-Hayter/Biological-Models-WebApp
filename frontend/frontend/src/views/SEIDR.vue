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
      <!--Upon sucessful sign up, sign in or preset save-->
      <TempAlert :alert-message="alertMessage" :alert-variant="alertVariant" :show-alert="showAlert" :alert-secs="alertSecs" @resetAlert="resetSubmissionAlert" />
      <div class="top-section">
        <div class="title-and-formula">
          <h4 class="tex2jax_ignore" style="float: left">SEIDR Model</h4>
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
        //Rates
        10, //alpha
        10, //beta
        1, //1/gamma
        10, //1/epsilon
        //Initial conditions
        10, //E0
        1, //I0
      ],
      //Contains user's presets
      userPresets: [],
      //Contains data for each paramater tab
      tabsData: [
        //Tab one
        {
          data: [
            {
              label: "\\alpha",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeAlpha",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "\\beta",
              emitEventName: "changeBeta",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "1/ \\gamma",
              emitEventName: "changeRecipGamma",
              min: 1,
              max: 10,
              step: 1,
            },
            {
              label: "1/ \\epsilon",
              //Name of event emitted to page component to update simParamData upon input
              emitEventName: "changeRecipEpsilon",
              min: 10,
              max: 50,
              step: 5,
            },
          ],
          isActive: true,
        },
        //Tab two
        {
          data: [
            {
              label: "E_{0}",
              emitEventName: "changeE0",
              min: 10,
              max: 50,
              step: 5,
            },
            {
              label: "I_{0}",
              emitEventName: "changeI0",
              min: 1,
              max: 10,
              step: 1,
            },
          ],
          isActive: false,
        },
      ],
      configTabTitles: ["Rates", "Initial Conditions"],
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
    updateAlpha(newAlpha) {
      this.simParamData[0] = newAlpha;
      console.log(this.simParamData[0], "alpha-change");
    },
    updateBeta(newBeta) {
      this.simParamData[1] = newBeta;
      console.log(this.simParamData[1], "beta-change");
    },
    updateRecipGamma(newRecipGamma) {
      this.simParamData[2] = newRecipGamma;
      console.log(this.simParamData[2], "1/gamma-change");
    },
    updateRecipEpsilon(newRecipEpsilon) {
      this.simParamData[3] = newRecipEpsilon;
      console.log(this.simParamData[3], "1/epsilon-change");
    },
    updateE0(newE0) {
      this.simParamData[4] = newE0;
      console.log(this.simParamData[4], "E0-change");
    },
    updateI0(newI0) {
      this.simParamData[5] = newI0;
      console.log(this.simParamData[5], "I0-change");
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
          userEmail: this.$store.state.activeUser.email
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
        this.simParamData[0] = Number(response.data["preset_params"][0]); //alpha
        this.simParamData[1] = Number(response.data["preset_params"][1]); //beta
        this.simParamData[2] = Number(response.data["preset_params"][2]); //1/gamma
        this.simParamData[3] = Number(response.data["preset_params"][3]); //1/epsilon
        this.simParamData[4] = Number(response.data["preset_params"][4]); //E0
        this.simParamData[5] = Number(response.data["preset_params"][5]); //I0
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
  },
  mounted() {
    if (this.$store.state.activeUser.isActive) { //Don't load presets if no one is logged in
      this.getAllPresets()
    }
  },
};
</script>

<style scoped>
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
  padding-left: 20em;
}
</style>

