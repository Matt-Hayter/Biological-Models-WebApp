<template>
  <div class="sim-visualiser">
    <RacerBarChart 
      ref="racerBarChart"
      :chart-config="barChartConfig"
      :initial-conditions="initialConditions"
      :sim-data="simData"
      :styling-class="visStylingClass"
    />
    <div>
      <div class="time-display">
        <span class="sim-time">
          Time elapsed ({{ timeUnits }}):
        </span>
        <div class="sim-time-box">
          {{ currentSimTime }}
        </div>
      </div>
    </div>
    <LineChart
      ref="lineChart"
      :chart-config="lineChartConfig"
      :initial-conditions="initialConditions"
      :sim-data="simData"
      :styling-class="visStylingClass"
    />
  </div>
</template>

<script>
import RacerBarChart from "./components/RacerBarChart.vue";
import LineChart from "./components/LineChart.vue";

export default {
  props: {
    barChartConfig: Object,
    lineChartConfig: Object,
    initialConditions: Array, //Listed in the order displayed sequentially in chart
    simData: Array,
    simMaxVal: Number,
    timeUnits: String,
    visStylingClass: String,
  },
  components: {
    RacerBarChart,
    LineChart
  },
  data() {
    return {
      currentSimTime: "0",
    };
  },
  computed: {
    simRunning() {
      return this.$store.state.simRunning
    },
  },
  watch: {
    simRunning: async function(isSimRunning) {
      //Visualise simulation if simRunning turns to true
      if (isSimRunning) {
        console.log(this.simData[0])
        const endTime = this.simData[0][this.simData[0].length - 1]["t"]
        this.$refs.racerBarChart.setUpChart(this.simMaxVal) //Setup for bar chart
        this.$refs.lineChart.setUpChart(this.simMaxVal, endTime) //Setup for line chart
        this.currentSimTime = 0
        //Delay to update inital values and x-scales before displaying simulation
        await new Promise((resolve) => setTimeout(resolve, 1000))
        await this.visualiseSim() //Begin racer chart animation
        this.$emit("endSim")
      }
    }
  },
  methods: {
    async visualiseSim() {
      let step = 0 //For all simulation time steps
      //Iterate through dataset with a time delay between iterations
      return new Promise((resolve) => {
        const visualisationInterval = setInterval(() => {
          if (!this.simRunning) { //Check if visualisation is running
            clearInterval(visualisationInterval)
            resolve()
            return
          }
          if (step + 1 == this.simData[0].length) { //Check if visualisation is completed 
            clearInterval(visualisationInterval)
            resolve()
            return
          }
          this.currentSimTime = Number(Math.round(this.simData[0][step]["t"]+"e1")+"e-1") //Update displayed time
          this.$refs.racerBarChart.chartSimStep(step)
          this.$refs.lineChart.chartSimStep(step)
          step ++ //Progress to next step
        }, 20)
      })
    }
  }
};
</script>

<style scoped>
.sim-visualiser {
  display: flex;
  flex-direction: column;
  justify-content: top;
}
.time-display {
  float: right;
  margin-right: 115px;
}
.time-display .sim-time-box {
  border-radius: 4px;
  border-color: rgb(146, 146, 146);
  background-color: rgba(171, 171, 171, 0.151);
  text-align: left;
  padding: 0em 1em;
  padding-top: 1.5px;
  width: 90px;
  height: 30px;
  border-style: outset;
  border-width: 2px;
  float: right;
  margin-left: 8px;
}
</style>