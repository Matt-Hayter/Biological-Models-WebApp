<!--eslint-disable-->
<template>
  <div class="predator-prey-view">
    <TheNavBar 
      @showPageAlert="showSubmissionAlert"
      />
    <!--Pass props to child component and handle emitted events for configuration bar-->
    <ConfigBar
      :tabs-data="tabsData"
      :config-tab-titles="configTabTitles"
      @changeN0="updateN0"
      @changea="updatea"
      @changeb="updateb"
      @changeP0="updateN0"
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
import TheNavBar from "@/components/TheNavBar/TheNavBar.vue";
import ConfigBar from "@/components/ConfigBar.vue";
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
      //Data used for running simulations
      simData: {
        //Prey
        N0: 0,
        a: 0,
        b: 0,
        //Predator
        P0: 0,
        c: 0,
        d: 0,
      },
      //Contains data for each paramater tab
      tabsData: [
        //Tab one
        {
          data: [
            {
              label: "$N_{0}$",
              //Name of event emitted to page component to update simData upon input
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
              //Name of event emitted to page component to update simData upon input
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
      //For sign up, login or saved preset alert, to be inherited by TempAlert component
      alertMessage: "",
      alertVariant: "danger",
      showAlert: false,
      alertSecs: 4,
    };
  },
  methods: {
    //Update simulation data with emitted event data upon slider input
    updateN0(newN0) {
      this.simData.N0 = newN0;
      console.log(this.simData.N0, "N0-change");
    },
    updatea(newa) {
      this.simData.a = newa;
      console.log(this.simData.a, "a-change");
    },
    updateb(newb) {
      this.simData.b = newb;
      console.log(this.simData.b, "b-change");
    },
    updateP0(newP0) {
      this.simData.P0 = newP0;
      console.log(this.simData.P0, "P0-change");
    },
    updatec(newc) {
      this.simData.c = newc;
      console.log(this.simData.c, "c-change");
    },
    updated(newd) {
      this.simData.d = newd;
      console.log(this.simData.d, "d-change");
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
