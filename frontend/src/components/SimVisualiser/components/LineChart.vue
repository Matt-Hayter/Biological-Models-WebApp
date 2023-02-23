<template>
  <div class="line-chart">
      <div class="chart-container" :class="stylingClass">
        <canvas id="dynamic-line-chart"></canvas>
      </div>
  </div>
</template>

<script>
import { Chart as ChartJS, LinearScale, LineController, PointElement, LineElement } from 'chart.js'
ChartJS.register(LinearScale, LineController, PointElement, LineElement)

export default {
  props: {
    lineChartConfig: Object,
    stylingClass: String,
  },
  data() {
    return {
      lineChart: null,
      lineChartConfig: null,
    }
  },
  methods: {
    chartSimStep(step) {
      //Set each chart data index to it's corresponding simulation data index, on each iteration
      for (let i = 0; i < this.simData.length; i++) {
          this.chartConfig.data.datasets[0].data[i] = this.simData[i][step]
      }
      this.racerChart.update("none"); //Update chart with current iteration's simulation data
    }
  },
  mounted() {
    const ctx = document.getElementById("dynamic-line-chart").getContext("2d")
    //Create chart.js bar plot, using inherited configuration
    this.lineChart = new ChartJS(ctx, this.lineChartConfig);
  }
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
  min-height: 30vw;
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