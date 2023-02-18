<template>
  <div class="tick-group">
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
        i += this.sliderData.tickStep
      ) {
        tickArray.push(Number(Math.round(i+"e2")+"e-2"));
      }
      return tickArray;
    },
  },
};
</script>

<style scoped>
.tick-group {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: -7px;
  margin-right: -7px;
}
.tick {
  display: flex;
  flex-direction: column;
  width: 29px;
  margin-top: -0.5em;
  font-size: 0.8em;
}
.tick-line {
  width: 0.8px;
  background-color: rgb(127, 127, 127);
  height: 5px;
  margin: auto;
}
.tick-content {
  margin: auto
}
</style>
