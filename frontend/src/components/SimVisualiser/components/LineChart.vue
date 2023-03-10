<template>
  <div class="line-chart">
    <div class="chart-container" :class="stylingClass">
      <canvas id="dynamic-line-chart"></canvas>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  LinearScale,
  LineController,
  PointElement,
  LineElement,
  Legend,
  Tooltip,
} from "chart.js";
ChartJS.register(
  LinearScale,
  LineController,
  PointElement,
  LineElement,
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
      lineChart: null,
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
      this.chartConfig.options.scales.y.max = graphBounds["data"]; //Resize y data to fit sim
      this.chartConfig.options.scales.x.max = graphBounds["t"]; //Resize x data to fit sim
      this.setInitialConditions(this.initialConditions); //Update chart with initial conditions
    },
    setInitialConditions(newICs) {
      //Set chart to initial values
      for (let i = 0; i < newICs.length; i++) {
        this.chartConfig.data.datasets[i].data = [{ data: newICs[i], t: 0 }];
      }
      this.lineChart.update();
    },
    chartSimStep(step) {
      //Set each chart data index to it's corresponding simulation data index, on each iteration
      for (let i = 0; i < this.simData.length; i++) {
        this.chartConfig.data.datasets[i].data.push(this.simData[i][step]);
      }
      if (step % 3 == 0) {
        this.lineChart.update("none"); //Update chart with current iteration's simulation data
      }
    },
  },
  mounted() {
    //Create chart.js bar plot, using inherited configuration
    this.lineChart = new ChartJS(
      document.getElementById("dynamic-line-chart").getContext("2d"),
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
  min-height: 29vw;
}
.comp-spec {
  min-height: 29vw;
}
.SIR {
  min-height: 33vw;
}
.SEIDR {
  min-height: 33vw;
}
</style>
