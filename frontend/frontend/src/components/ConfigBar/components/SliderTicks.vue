<template>
  <div
    class="tick-group d-flex justify-content-between"
    style="padding: 0 1.5em"
  >
    <!--Assign correct number of ticks and values to slider, depending on implementation-->
    <div v-for="label in createTickLabels" :key="label">
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
  computed: {
    //Create array of tick labels, given max, min and step{
    createTickLabels() {
      const tickArray = []
      for (
        let i = this.sliderData.min;
        i <= this.sliderData.max;
        i += this.sliderData.step
      ) {
        tickArray.push(i);
      }
      return tickArray;
    },
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
  height: 5px;
  margin: auto;
}
</style>
