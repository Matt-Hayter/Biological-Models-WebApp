<!-- eslint-disable -->
<template>
  <div class="MalthusianPage">
    <TheNavBar />
    <ConfigBarSingleSpecies style="float: left;" />
    <div class="model-text-main" style="float: left; padding: 1em; padding-left: 1em;">
      <h5>Malthusian Model</h5>
    </div>
  </div>
</template>

<script>
import TheNavBar from "@/components/Common/TheNavBar.vue";
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
