<template>
  <div class="bar-chart">
    <div class="chart-container" :class="stylingClass">
      <canvas id="racer-bar-chart"></canvas>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip,
} from "chart.js";
ChartJS.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
);

export default {
  props: {
    chartConfig: Object,
    initialConditions: Array, //Listed in the order displayed sequentially in chart
    simData: Array,
    stylingClass: String,
  },
  data() {
    return {
      racerChart: null,
    };
  },
  watch: {
    initialConditions: function (newICs) {
      //Update initial bar lengths upon user param change
      this.setInitialConditions(newICs);
    },
  },
  methods: {
    setUpChart(graphBounds) {
      this.chartConfig.options.scales.x.max = graphBounds["data"]; //Resize bar plot to fit sim
      this.setInitialConditions(this.initialConditions); //Update chart with initial conditions
    },
    setInitialConditions(newICs) {
      //Set chart to initial values
      for (let i = 0; i < newICs.length; i++) {
        this.chartConfig.data.datasets[0].data[i] = newICs[i];
      }
      this.racerChart.update();
    },
    chartSimStep(step) {
      //Set each chart data index to it's corresponding simulation data index, on each iteration
      for (let i = 0; i < this.simData.length; i++) {
        this.chartConfig.data.datasets[0].data[i] =
          this.simData[i][step]["data"];
      }
      this.racerChart.update("none"); //Update chart with current iteration's simulation data
    },
  },
  mounted() {
    //Created chart.js bar plot, using inherited configuration
    this.racerChart = new ChartJS(
      document.getElementById("racer-bar-chart"),
      this.chartConfig
    );
  },
};
</script>

<style scoped>
.chart-container {
  padding: 20px;
  background: white;
  position: relative;
  width: 95%;
}
.pred-prey {
  min-height: 16vw;
}
.comp-spec {
  min-height: 16vw;
}
.SIR {
  min-height: 20vw;
}
.SEIDR {
  min-height: 25vw;
}
</style>
