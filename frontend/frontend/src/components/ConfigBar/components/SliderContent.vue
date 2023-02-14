<template>
  <div class="slider-content" style="padding: 0 1.5em">
    <label
      for="slider-range"
      class="form-label d-flex"
      style="font-size: 1.4em; float: left; margin-bottom: 0"
    >
      <katex-element :expression="sliderData.label"/>
      <b-icon
        icon="info-circle"
        scale="0.75"
        shift-v="-5em"
        variant="info"
        style="margin-left: 0.5em"
      />
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
    simRunning: Boolean,
  },
  data() {
    return {
      isRunning: true
    };
  },
};
</script>

<style scoped>
.current-param-value-box {
  border-radius: 4px;
  border-color: rgb(146, 146, 146);
  background-color: rgba(171, 171, 171, 0.05);
  text-align: left;
  padding-left: 10px;
  padding-top: 1.5px;
  font-size: 0.9em;
  margin-top: 10px;
  width: 50px;
  height: 25px;
  border-style: outset;
  border-width: 1px;
  float: right;
}
</style>
