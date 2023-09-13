//Contains configuration for racer bar chart
let chartData = {
  datasets: [
    {
      label: "Prey",
      backgroundColor: "rgba(54, 162, 255, 1)",
      borderColor: "rgba(54, 162, 255, 1)",
      borderWidth: 3,
      cubicInterpolationMode: "monotone",
      data: [{ data: 0, t: 0 }], //Default. Externally set as simulation is run
    },
    {
      label: "Predator",
      borderColor: "rgba(255, 26, 104, 1)",
      backgroundColor: "rgba(255, 26, 104, 1)",
      borderWidth: 3,
      cubicInterpolationMode: "monotone",
      data: [{ data: 0, t: 0 }], //Default. Externally set as simulation is run
    },
  ],
};
//Insert data into config
export default {
  type: "line",
  data: chartData,
  options: {
    animation: false, //No animation
    parsing: {
      xAxisKey: "t",
      yAxisKey: "data",
    },
    aspectRatio: 3,
    scales: {
      x: {
        beginAtZero: true,
        type: "linear",
        max: 10,
        title: {
          display: true,
          text: "Time (years)",
          font: {
            size: 15,
          },
        },
        ticks: {
          minRotaion: 0, //Slightly reduce render time
          maxRotation: 0,
        },
      },
      y: {
        beginAtZero: true,
        type: "linear",
        max: 10,
        title: {
          display: true,
          text: "Population Density (/area)",
          font: {
            size: 15,
          },
        },
        ticks: {
          minRotaion: 0, //Slightly reduce render time
          maxRotation: 0,
        },
      },
    },
    spanGaps: true, //Slightly reduce render time
    elements: {
      point: {
        radius: 0, //Slightly reduce render time
      },
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          font: {
            size: 13,
          },
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    interaction: {
      intersect: false,
    },
  },
};
