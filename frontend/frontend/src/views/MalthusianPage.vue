<!-- eslint-disable -->
<template>
  <div class="MalthusianPage">
    <TheNavBar />
    <ConfigBarSingleSpecies style="float: left;" />
    <div class="model-title">
      <h4>Malthusian Model</h4>
    </div>
    <div class="formula">
      <vue-mathjax formula="$$\Large\frac{dN}{dt}=\left(b-d\right)N=rN$$"></vue-mathjax>
    </div>
  </div>
</template>

<script>
import TheNavBar from "@/components/common/TheNavBar.vue";
import ConfigBarSingleSpecies from "@/components/ConfigBar/components/ConfigBarSingleSpecies.vue";

export default {
  components: {
    TheNavBar,
    ConfigBarSingleSpecies,
  },
  data() {},
  methods: {},
};
</script>

<style>
.model-title {
  float: left;
  padding: 1.5em;
  padding-left: 1.5em;
}
.formula {
  float: left;
  padding: 1.5em;
  padding-left: 8em;
}
</style>
