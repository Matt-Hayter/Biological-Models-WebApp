<template>
  <div class="bar-chart">
    <div class="chartMenu">
      <p>WWW.CHARTJS3.COM (Chart JS 4.2.0)</p>
    </div>
    <div class="chartCard">
      <div class="chartBox">
        <canvas id="myChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // setup 
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Weekly Sales',
          data: [18, 12, 6, 9, 12, 3, 9],
          backgroundColor: [
            'rgba(255, 26, 104, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(0, 0, 0, 0.2)'
          ],
          borderColor: [
            'rgba(255, 26, 104, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(0, 0, 0, 1)'
          ],
          borderWidth: 1
        }]
      },
      // config 
      config: {
        type: 'bar',
        data: this.data,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      },
      // render init block
      myChart: new Chart(
        document.getElementById('myChart'),
        this.config
      ),
    };
  },
  methods: {},
};
</script>

<style scoped>
.chartMenu {
  width: 100vw;
  height: 40px;
  background: #1A1A1A;
  color: rgba(54, 162, 235, 1);
}
.chartMenu p {
  padding: 10px;
  font-size: 20px;
}
.chartCard {
  width: 100vw;
  height: calc(100vh - 40px);
  background: rgba(54, 162, 235, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}
.chartBox {
  width: 700px;
  padding: 20px;
  border-radius: 20px;
  border: solid 3px rgba(54, 162, 235, 1);
  background: white;
}
</style>
