//Contains configuration for racer bar chart
let chartData = {
  labels: ['Susceptible', 'Exposed', 'Infectious', 'Dead', 'Recovered'],
  datasets: [{
    label: 'Disease spread: SEIDR',
    data: [0, 0, 0, 0, 0],
    backgroundColor: [
      'rgba(238, 255, 0, 0.2)',
      'rgba(5, 118, 248, 0.2)',
      'rgba(145, 0, 0, 0.2)',
      'rgba(0, 0, 0, 0.2)',
      'rgba(0, 170, 17, 0.2)',
    ],
    borderColor: [
      'rgba(238, 255, 0, 1)',
      'rgba(5, 118, 248, 1)',
      'rgba(145, 0, 0, 1)',
      'rgba(0, 0, 0, 1)',
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
        max: 200
      },
      y: {
        grid: {
            color: "rgba(0, 0, 0, 0)",
        }
      }
    },
    aspectRatio: 6
  }
};
