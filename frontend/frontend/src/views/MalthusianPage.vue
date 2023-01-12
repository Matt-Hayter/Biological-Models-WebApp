<!-- eslint-disable -->
<template>
  <div class="MalthusianPage">
    <TheNavBar />
    <ConfigBarSingleSpecies />
    <div class="main-page" style="margin-left: 25em"> 
      <div class="title-and-info">
        <h4>Malthusian Model</h4>
        <br>
        <ModelInfo>This is some information about this model asfkjad akhlzshzsl hals alilzs zslhz lr z  l hzlxf zlx rzlfnzdfl fnz</ModelInfo>
      </div>
      <div class="formula">
        <vue-mathjax formula="$$\Large\frac{dN}{dt}=rN+m$$"></vue-mathjax>
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
  data() {},
  methods: {},
};
</script>

<style>
.title-and-info {
  float: left;
  padding-top: 2em;
  padding-left: 1.5em;
  display: flex;
  flex-direction: column;
}
.formula {
  float: left;
  padding: 2em;
  padding-left: 14em;
}
</style>
