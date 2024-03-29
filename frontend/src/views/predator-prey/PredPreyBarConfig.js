//Contains configuration for racer bar chart
let chartData = {
  labels: ["Prey", "Predator"],
  datasets: [
    {
      data: [0, 0],
      backgroundColor: ["rgba(54, 162, 255, 0.2)", "rgba(255, 26, 104, 0.2)"],
      borderColor: ["rgba(54, 162, 255, 1)", "rgba(255, 26, 104, 1)"],
      borderWidth: 1,
      barPercentage: 0.9,
    },
  ],
};
//Insert data into config
export default {
  type: "bar",
  data: chartData,
  options: {
    indexAxis: "y",
    aspectRatio: 5,
    scales: {
      x: {
        beginAtZero: true,
        max: 10,
        title: {
          display: true,
          text: "Population Density (/area)",
          font: {
            size: 15,
          },
        },
      },
      y: {
        grid: {
          color: "rgba(0, 0, 0, 0)",
        },
        ticks: {
          font: {
            size: 13,
          },
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: true,
      },
    },
  },
};
