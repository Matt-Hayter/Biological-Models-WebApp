//Contains configuration for racer bar chart
let chartData = {
  labels: ['Susceptible', 'Infectious', 'Recovered'],
  datasets: [{
    label: 'Disease spread: SIR',
    data: [0, 0, 0],
    backgroundColor: [
      'rgba(255, 255, 0, 0.3)',
      'rgba(255, 0, 0, 0.2)',
      'rgba(0, 170, 17, 0.2)',
    ],
    borderColor: [
      'rgba(255, 255, 0, 1)',
      'rgba(255, 0, 0, 1)',
      'rgba(0, 170, 17, 1)',
    ],
    borderWidth: 1,
    barPercentage: 0.9,
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
        beginAtZero: true,
        max: 10000000
      },
      y: {
        grid: {
            color: "rgba(0, 0, 0, 0)",
        }
      }
    },
    aspectRatio: 5
  }
};
