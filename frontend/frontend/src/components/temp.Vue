<!--eslint-disable-->
<template>
  <div class="config-bar">
    <!--Enclose config within card-->
    <b-card class="rounded-0" style="min-width: 25em; position: fixed">
      <template #header>
        <p class="mt-3" style="font-size: 1.5em">Model Parameters</p>
      </template>
      <b-card-body style="min-height: 68vh">
        <!--Display all param sliders with correct labels, depending on page-->
        <div v-for="sliderData in allSliderData" :key="sliderData.label">
          <!--Update component data for Slider to inherit-->
          <span currentSliderData="sliderData"></span>
          <!--Passes events emitted from slider up the inheritance hierachy-->
          <SliderContent v-on="$listeners"
            >{{ sliderData.label }}
          </SliderContent>
          <SliderTicks />
        </div>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import SliderContent from "@/components/common/SliderContent.vue";
import SliderTicks from "@/components/common/SliderTicks.vue";

export default {
  components: {
    SliderContent,
    SliderTicks,
  },
  props: ["allSliderData"],
  data() {
    return {
      currentSliderData: {},
    };
  },
  methods: {},
};
</script>
