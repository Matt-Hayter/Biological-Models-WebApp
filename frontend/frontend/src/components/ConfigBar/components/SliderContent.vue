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
    <!--Bind inherited slider data to required range attributes-->
    <input
      type="range"
      class="form-range h-70"
      id="slider-range"
      :min="sliderData.min"
      :value="currentSimParamData"
      :max="sliderData.max"
      :step="sliderData.step"
      @input="$emit(sliderData.emitEventName, Number($event.target.value))"
    />
  </div>
</template>

<script>
export default {
  props: {
    //Slider's contents are inherited
    sliderData: Object,
    currentSimParamData: Number
  },
  data() {
    return {};
  },
};
</script>
