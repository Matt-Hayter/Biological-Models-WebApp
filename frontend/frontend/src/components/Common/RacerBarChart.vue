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
    initialConditions: function(newICs) { //Update initial bar lengths upon user param change
      this.setInitialConditions(newICs)
    },
    simRunning: function(isSimRunning) {
      //Visualise simulation if simRunning turns to true
      if (isSimRunning) {
        this.chartConfig.options.scales.x.max = this.simMaxVal //Resize bar plot to fit sim
        this.setInitialConditions(this.initialConitions) //Update chart with initial conditions
        this.racerChart.update();
        //Give chart time to update with inital values before displaying sim
        setTimeout(this.visualiseChartSim(), 1000)
      }
    }
  },
  methods: {
    setInitialConditions(newICs) { //Set chart to initial values
      for(let i = 0; i < newICs.length; i++) {
        this.chartConfig.data.datasets[0].data[i] = newICs[i]
      }
      this.racerChart.update();
    },
    visualiseChartSim() {
      let step = 0 //For all simulation time steps
      //Iterate through dataset with a time delay between iterations
      const visualisationInterval = setInterval(() => {
        //Set each chart data index to it's corresponding simulation data index, on each iteration
        for (let i = 0; i < this.simData.length; i++) {
            this.chartConfig.data.datasets[0].data[i] = this.simData[i][step]
        }
        this.racerChart.update(); //Update chart with current iteration's simulation data
        step ++ //Progress to next step
        if (!this.simRunning) {
          clearInterval(visualisationInterval)
        }
      }, 100)
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
  width: 100%;
}
</style>