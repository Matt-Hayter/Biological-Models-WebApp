//Contains configuration for racer bar chart
let chartData = {
  labels: ['Susceptible', 'Infected', 'Recovered'],
  datasets: [{
    label: 'Disease spread: SIR',
    data: [0, 0, 0],
    backgroundColor: [
      'rgba(255, 220, 0, 0.3)',
      'rgba(255, 0, 0, 0.2)',
      'rgba(0, 170, 17, 0.2)',
    ],
    borderColor: [
      'rgba(255, 220, 0, 1)',
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
    aspectRatio: 4,
    scales: {
      x: {
        beginAtZero: true,
        max: 10000000,
        title: {
          display: true,
          text: "Population",
          font: {
            size: 16,
          }
        }
      },
      y: {
        grid: {
            color: "rgba(0, 0, 0, 0)",
        },
        ticks: {
          font: {
            size: 13
          }
        }
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: true
      }
    },
  }
};
