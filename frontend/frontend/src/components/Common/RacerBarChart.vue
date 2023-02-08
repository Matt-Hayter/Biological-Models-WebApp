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
    initialConditions: Array, //Listed in the order displayed sequentially in chart
    simRunning: Boolean,
    simData: Array,
    simMaxVal: Number
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
    simRunning: function(value) {
      console.log(this.simData)
      this.chartConfig.options.scales.x.max = this.simMaxVal //Resize bar plot to fit sim
      this.racerChart.update();
      //Visualise simulation if simRunning turns to true
      if (value) {
        let step = 0 //For all simulation time steps
        setInterval(() => {
          //Set each chart data element to it's corresponding simulation data index, on each iteration
          for (let i = 0; i < this.simData.length; i++) {
              this.chartConfig.data.datasets[0].data[i] = this.simData[i][step]
          }
          this.racerChart.update();
        }, 10)
      }
    }
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