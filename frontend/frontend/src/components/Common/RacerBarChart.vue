<template>
  <div class="bar-chart" style="display: flex; justify-content: center">
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
  },
  data() {
    return {
    };
  },
  mounted() {
    const ctx = document.getElementById('racer-bar-chart');
    new ChartJS(ctx, this.chartConfig);
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  aspect-ratio: 1.9;
  padding: 20px;
  background: white;
}
</style>