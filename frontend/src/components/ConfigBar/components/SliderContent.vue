<template>
  <div class="slider-content">
    <label
      for="slider-range"
      class="form-label d-flex"
      style="float: left; margin-bottom: 0"
    >
      <katex-element style="font-size: 1.4em" :expression="sliderData.label" />
      <span style="font-size: 1.2em; margin-left: 10px; margin-top: 3px">{{
        sliderData.units
      }}</span>
      <div :id="sliderData.label" class="info-hit-box">
        <b-icon
          icon="info-circle"
          scale="1.1"
          shift-v="-7em"
          variant="info"
          style="margin-left: 0.5em"
        />
      </div>
      <b-popover
        custom-class="custom-popover"
        :target="sliderData.label"
        variant="info"
        triggers="hover click"
        :show.sync="showParamInfo"
        placement="right"
        :no-fade="true"
      >
        {{ sliderData.description }}
      </b-popover>
    </label>
    <div class="current-param-value-box">
      {{ currentSimParamData }}
    </div>
    <!--Bind inherited slider data to required range attributes-->
    <input
      type="range"
      class="form-range h-70"
      id="slider-range"
      :min="sliderData.min"
      :value="currentSimParamData"
      :max="sliderData.max"
      :step="sliderData.inputStep"
      @input="$emit(sliderData.emitEventName, Number($event.target.value))"
      :disabled="simRunning"
    />
  </div>
</template>

<script>
export default {
  props: {
    //Slider's contents are inherited
    sliderData: Object,
    currentSimParamData: Number,
  },
  data() {
    return {
      isRunning: true,
      showParamInfo: false,
    };
  },
  computed: {
    simRunning() {
      return this.$store.state.simRunning;
    },
  },
  watch: {
    //Hide suggestions if sim is running
    simRunning: function (isSimRunning) {
      if (isSimRunning) {
        this.showParamInfo = false;
      }
    },
  },
  methods: {
    tabClick() {
      this.showParamInfo = false; //Close parameter description on tab click
    },
  },
};
</script>

<style scoped>
.current-param-value-box {
  border-radius: 4px;
  border-color: rgb(146, 146, 146);
  background-color: rgba(171, 171, 171, 0.05);
  text-align: left;
  padding-left: 7px;
  padding-top: 1.5px;
  font-size: 0.9em;
  margin-top: 10px;
  width: 60px;
  height: 25px;
  border-style: outset;
  border-width: 1px;
  float: right;
}
.custom-popover {
  z-index: 1;
  max-width: 550px;
}
.info-hit-box {
  width: 35px;
  height: 30px;
}
</style>
