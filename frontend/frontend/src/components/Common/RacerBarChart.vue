<template>
  <div class="bar-chart">
      <div class="chart-container">
        <canvas id="racer-bar-chart"></canvas>
      </div>
  </div>
</template>

<script>
import { Chart as ChartJS, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(BarController, BarElement, CategoryScale, LinearScale)

export default {
  props: {
    chartConfig: Object,
    initialConditions: Array, //Given in the order displayed in chart
  },
  data() {
    return {
      racerChart: null
    };
  },
  watch: {
    initialConditions: function(value) { //Update initial bar lengths upon user param change
      for(let i = 0; i < value.length; i++) {
        this.chartConfig.data.datasets[0].data[i] = this.initialConditions[i]
      }
      this.racerChart.update();
    },
    // displaySimulation() {
    //   // setInterval(() => {
    //   //   //this.chartConfig.data.datasets[0].data[0] += 0.01
    //   //   racerChart.update();
    //   // }, 100)
    // }
  },
  mounted() {
    //Created chart.js bar plot, using inherited configuration
    this.racerChart = new ChartJS(document.getElementById('racer-bar-chart'), this.chartConfig);
  }
};
</script>

<style scoped>
.chart-container {
  padding: 20px;
  background: white;
  position: relative;
  height: 50vh;
  width: 67vw;
}
</style>