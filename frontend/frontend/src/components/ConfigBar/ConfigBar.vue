<template>
  <div class="config-bar">
    <!--Enclose config within card-->
    <b-card class="rounded-0" style="min-width: 25em; position: fixed" no-body>
      <b-card-header header-tag="nav">
        <b-nav card-header tabs fill style="display: flex; flex-direction: column">
          <p class="mt-3" style="font-size: 1.5em">Model Parameters</p>
          <div tabs style="margin-top:-1em">
            <b-nav-item style="float: left" :active="tabsData[0].isActive" @click="onTabOneClick()" >
              {{ configTabTitles[0] }}
            </b-nav-item>
            <b-nav-item style="float: left" :active="tabsData[1].isActive" @click="onTabTwoClick()">
              {{ configTabTitles[1] }}
            </b-nav-item>
          </div>
        </b-nav>
      </b-card-header>
      <b-card-body style="min-height: 68vh">
        <!--Render all param sliders with correct labels, for each tab-->
        <div v-for="(tabData, index1) in tabsData" :key="tabData.data.label">
          <!--Only show tab data if tab is selected (isActive=true). Rendered nonetheless.-->
          <div v-show="tabData.isActive" v-for="(sliderData, index2) in tabData.data" :key="sliderData.label">
            <!--Pass each slider's data individually to slider component-->
            <SliderContent 
              :slider-data="sliderData"
              :current-sim-param-data="simParamData[currentSliderIndex(index1,index2)]"
              v-on="$listeners"
              >
            </SliderContent>
            <SliderTicks :slider-data="sliderData"/>
          </div>
        </div>
        <PresetButtons v-on="$listeners" :param-suggestions="paramSuggestions" :user-presets="userPresets"/>
        </b-card-body>
    </b-card>
  </div>
</template>

<script>
import SliderContent from "@/components/ConfigBar/components/SliderContent.vue";
import SliderTicks from "@/components/ConfigBar/components/SliderTicks.vue";
import PresetButtons from "@/components/ConfigBar/components/PresetButtons.vue";

export default {
  props: {
    tabsData: Array,
    configTabTitles: Array,
    paramSuggestions: Array,
    userPresets: Array,
    simParamData: Array
  },
  components: {
    SliderContent,
    SliderTicks,
    PresetButtons,
  },
  data() {
    return {};
  },
  methods: {
    currentSliderIndex(i1, i2) {
      return i1*this.simParamData.length/2+i2
    },
    //Update tabsData[i].isActive props if tab changes
    onTabOneClick() {
      this.$emit("tabOneActive")
    },
    onTabTwoClick() {
      this.$emit("tabTwoActive")
    },
  }
};
</script>
