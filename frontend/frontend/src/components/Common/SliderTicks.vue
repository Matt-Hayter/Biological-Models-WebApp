<template>
  <div
    class="tick-group d-flex justify-content-between"
    style="padding: 0 0.3em"
  >
    <!--Assign correct number of ticks and values to slider, depending on implementation-->
    <div v-for="label in tickLabels" :key="label">
      <div class="tick">
        <span class="tick-line"></span>
        <span class="tick-content">{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    sliderData: Object,
  },
  data() {
    return {
      tickLabels: [],
    };
  },
  method: {
    //Create array of tick labels, given max, min and step
    createTickLabels() {
      for (
        let i = this.sliderData.min;
        i <= this.sliderData.max;
        this.sliderData.step
      ) {
        this.tickLabels.push(i);
      }
    },
  },
  created() {
    this.createTickLabels();
  },
};
</script>

<style scoped>
.tick-group {
  padding: 0 0.4em;
}
.tick {
  display: flex;
  flex-direction: column;
  margin-top: -0.5em;
  font-size: 0.8em;
}
.tick-line {
  width: 0.8px;
  background-color: rgb(127, 127, 127);
  height: 7px;
  margin: auto;
}
</style>
