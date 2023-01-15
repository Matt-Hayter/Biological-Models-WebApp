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
        <div v-for="currentSliderData in allSliderData" :key="currentSliderData.label">
          <!--Passes events emitted from slider up the inheritance hierachy-->
          <SliderContent 
            :slider-data="currentSliderData"
            v-on="$listeners"
            >{{ currentSliderData.label }}
          </SliderContent>
          <SliderTicks :slider-data="currentSliderData"/>
        </div>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
/*eslint-disable*/
import SliderContent from "@/components/common/SliderContent.vue";
import SliderTicks from "@/components/common/SliderTicks.vue";

export default {
  props: {
    allSliderData: Object
  },
  components: {
    SliderContent,
    SliderTicks,
  },
  data() {
    return {};
  },
};
</script>
