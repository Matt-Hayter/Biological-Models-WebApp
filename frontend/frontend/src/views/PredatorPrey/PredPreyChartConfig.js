//Contains configuration for racer bar chart
const chartData = {
  labels: ['Prey', 'Predator'],
  datasets: [{
    label: 'Weekly Sales',
    data: [18, 12],
    backgroundColor: [
      'rgba(255, 26, 104, 0.2)',
      'rgba(54, 162, 235, 0.2)',
    ],
    borderColor: [
      'rgba(255, 26, 104, 1)',
      'rgba(54, 162, 235, 1)',
    ],
    borderWidth: 1,
    barThickness: 100
  }]
};
//Insert data into config 
export default {
  type: 'bar',
  data: chartData,
  options: {
    indexAxis: "y",
    scales: {
      x: {
        beginAtZero: true
      },
    }
  }
};
