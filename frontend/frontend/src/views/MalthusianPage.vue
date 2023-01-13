<template>
  <div class="MalthusianPage">
    <TheNavBar />
    <ConfigBarSingleSpecies
      @changeInitialPopulation="updateInitialPopulation"
      @changeRate="updateRate"
    />
    <div class="main-page" style="margin-left: 25em">
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
import TheNavBar from "@/components/common/TheNavBar.vue";
import ConfigBarSingleSpecies from "@/components/ConfigBar/components/ConfigBarMalthusian.vue";
import ModelInfo from "@/components/common/ModelInfo.vue";

export default {
  components: {
    TheNavBar,
    ConfigBarSingleSpecies,
    ModelInfo,
  },
  data() {
    return {
      rate: 0,
      initialPopulation: 0,
    };
  },
  methods: {
    updateInitialPopulation(newInitialPop) {
      this.initialPopulation = newInitialPop;
      console.log(this.initialPopulation);
    },
    updateRate(newRate) {
      this.rate = newRate;
      console.log(this.rate);
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
