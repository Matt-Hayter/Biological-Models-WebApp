<template>
  <div class="slider-content" style="padding: 0 0.5em">
    <label
      for="slider-range"
      class="form-label d-flex"
      style="font-size: 1.5em; float: left; margin-bottom: 0"
      >{{ sliderData.label }}
      <b-icon
        icon="info-circle"
        scale="0.7"
        shift-v="-4em"
        variant="info"
        style="margin-left: 0.5em"
      />
    </label>
    <!--Bind inherited slider data to required range attributes-->
    <input
      type="range"
      class="form-range"
      id="slider-range"
      :min="sliderData.min"
      :max="sliderData.max"
      :step="sliderData.step"
      @input="$emit(sliderData.emitEventName, $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  props: {
    //Slider's contents are inherited
    sliderData: Object,
  },
  data() {
    return {};
  },
};
</script>
