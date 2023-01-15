<template>
  <div class="malthusian-page">
    <TheNavBar />
    <!--Pass props to child component and handle emitted events for configuration bar-->
    <ConfigBar
      :all-slider-data="allSliderData"
      @changeInitialPopulation="updateInitialPopulation"
      @changeRate="updateRate"
    />
    <div class="rhs-page-component" style="margin-left: 25em">
      <div class="top-section">
        <div class="title-and-formula">
          <h4 style="float: left">Malthusian Model</h4>
          <div class="formula">
            <vue-mathjax formula="$$\Large\frac{dN}{dt}=rN-m$$"></vue-mathjax>
          </div>
        </div>
        <ModelInfo style="padding-left: 1.5em; padding-right: 1.5em">
          <b-card-text>
            The Malthusian model is a simplistic description of population
            dynamics for a single species. The population will continue to grow
            in number regardless of it's size, meaning that there are no
            external constraints which may limit population growth.
          </b-card-text>
          <b-card-text>
            The model can be extended to account for population migration,
            meaning that members are either migrating into or out of the
            population. This can be explored using the $m$ parameter.
          </b-card-text>
        </ModelInfo>
      </div>
    </div>
  </div>
</template>

<script>
import TheNavBar from "@/components/TheNavBar.vue";
import ConfigBar from "@/components/ConfigBar/ConfigBar.vue";
import ModelInfo from "@/components/common/ModelInfo.vue";

export default {
  components: {
    TheNavBar,
    ConfigBar,
    ModelInfo,
  },
  data() {
    return {
      //Data used for running simulations
      simData: {
        rate: 0,
        initialPopulation: 0,
      },
      //Create array containing data for each parameter slider on page
      allSliderData: [
        {
          label: "$N_{0}$",
          //Name of event emitted to page component to update simData upon input
          emitEventName: "changeInitialPopulation",
          min: 10,
          max: 50,
          step: 10,
        },
        {
          label: "$r$",
          emitEventName: "changeRate",
          min: 1,
          max: 5,
          step: 1,
        },
      ],
    };
  },
  methods: {
    //Update simulation data with emitted event data upon input
    updateInitialPopulation(newInitialPop) {
      this.simData.initialPopulation = newInitialPop;
      console.log(this.simData.initialPopulation, "Pop");
    },
    updateRate(newRate) {
      this.simData.rate = newRate;
      console.log(this.simData.rate, "rate");
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
  padding-left: 14em;
}
</style>
