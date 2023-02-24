//Contains configuration for racer bar chart
let chartData = {
  datasets: [{
    label: 'Susceptible',
    backgroundColor: 'rgba(255, 220, 0, 1)',
    borderColor: 'rgba(255, 220, 0, 1)',
    borderWidth: 3,
    cubicInterpolationMode: 'monotone',
    data: [{"data": 0, "t": 0}], //Default. Externally set as simulation is run
  },
  {
    label: 'Exposed',
    borderColor: 'rgba(5, 118, 248, 1)',
    backgroundColor: 'rgba(5, 118, 248, 1)',
    borderWidth: 3,
    cubicInterpolationMode: 'monotone',
    data: [{"data": 0, "t": 0}], //Default. Externally set as simulation is run
  },
  {
    label: 'Infectious',
    borderColor: 'rgba(255, 0, 0, 1)',
    backgroundColor: 'rgba(255, 0, 0, 1)',
    borderWidth: 3,
    cubicInterpolationMode: 'monotone',
    data: [{"data": 0, "t": 0}], //Default. Externally set as simulation is run
  },
  {
    label: 'Dead',
    borderColor: 'rgba(0, 0, 0, 1)',
    backgroundColor: 'rgba(0, 0, 0, 1)',
    borderWidth: 3,
    cubicInterpolationMode: 'monotone',
    data: [{"data": 0, "t": 0}], //Default. Externally set as simulation is run
  },
  {
    label: 'Recovered',
    borderColor:'rgba(0, 170, 17, 1)',
    backgroundColor: 'rgba(0, 170, 17, 1)',
    borderWidth: 3,
    cubicInterpolationMode: 'monotone',
    data: [{"data": 0, "t": 0}], //Default. Externally set as simulation is run
  }]
};
//Insert data into config 
export default { 
  type: 'line',
  data: chartData,
  options: {
    animation: false, //No animation
    parsing: {
      xAxisKey: "t",
      yAxisKey: "data"
    },
    aspectRatio: 2,
    scales: {
      x: {
        beginAtZero: true,
        type: 'linear',
        max: 10,
        title: {
          display: true,
          text: "Time (days)",
          font: {
            size: 15,
          }
        },
        ticks: {
          minRotaion: 0, //Slightly reduce render time
          maxRotation: 0
        }
      },
      y: {
        beginAtZero: true,
        type: 'linear',
        max: 10,
        title: {
          display: true,
          text: "Population",
          font: {
            size: 15,
          }
        },
        ticks: {
          minRotaion: 0, //Slightly reduce render time
          maxRotation: 0
        }
      },
    },
    spanGaps: true, //Slightly reduce render time
    elements: {
      point: {
        radius: 0 //Slightly reduce render time
      }
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          font: {
            size: 13
          }
        }
      },
      tooltip: {
        enabled: true
      }
    },
    interaction: {
      intersect: false
    },
  }
};
