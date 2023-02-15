<template>
  <div class="sim-visualiser">
    <RacerBarChart 
      ref="racerBarChart"
      :chart-config="chartConfig"
      :initial-conditions="initialConditions"
      :sim-data="simData"
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
  </div>
</template>

<script>
import RacerBarChart from "@/components/SimVisualiser/components/RacerBarChart.vue";

export default {
  props: {
    chartConfig: Object,
    initialConditions: Array, //Listed in the order displayed sequentially in chart
    simRunning: Boolean,
    simData: Array,
    simTimeData: Array,
    simMaxVal: Number,
    timeUnits: String,
  },
  components: {
    RacerBarChart,
  },
  data() {
    return {
      currentSimTime: "0",
    };
  },
  watch: {
    simRunning: async function(isSimRunning) {
      //Visualise simulation if simRunning turns to true
      if (isSimRunning) {
        this.$refs.racerBarChart.setUpChart(this.simMaxVal) //Setup for bar chart
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
          }
          if (step + 1 == this.simData[0].length) { //Check if visualisation is completed 
            clearInterval(visualisationInterval)
            resolve()
          }
          this.currentSimTime = Number(Math.round(this.simTimeData[step]+"e1")+"e-1") //Update displayed time
          this.$refs.racerBarChart.chartSimStep(step)
          step ++ //Progress to next step
        }, 10)
      })
    }
  },
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