//Contains configuration for racer bar chart
let chartData = {
  labels: ['Species 1', 'Species 2'],
  datasets: [{
    label: 'Two Competing Species',
    data: [0, 0],
    backgroundColor: [
      'rgba(255, 170, 0, 0.2)',
      'rgb(0, 255, 255, 0.2)',
    ],
    borderColor: [
      'rgba(255, 170, 0, 1)',
      'rgb(0, 255, 255, 1)',
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
    aspectRatio: 5,
    scales: {
      x: {
        beginAtZero: true,
        max: 1000,
        title: {
          display: true,
          text: "Population Density",
          font: {
            size: 15,
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