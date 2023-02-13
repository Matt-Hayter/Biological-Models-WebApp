<template>
  <div class="config-bar">
    <!--Enclose config within card-->
    <b-card class="rounded-0" style="width:25em; position: relative; float: left;" no-body>
      <!--If tabs are required-->
      <div v-if="configTabTitles.length == 2">
        <b-card-header header-tag="nav">
          <b-nav card-header tabs fill style="display: flex; flex-direction: column">
            <p style="font-size: 1.5em; margin-bottom: -0.07em;">Model Parameters</p>
            <div tabs>
              <b-nav-item style="float: left" :active="tabsData[0].isActive" @click="onTabOneClick()" >
                {{ configTabTitles[0] }}
              </b-nav-item>
              <b-nav-item style="float: left" :active="tabsData[1].isActive" @click="onTabTwoClick()">
                {{ configTabTitles[1] }}
              </b-nav-item>
            </div>
          </b-nav>
        </b-card-header>
      </div>
      <!--If no tabs required-->
      <div v-else-if="configTabTitles.length == 1">
        <b-card-header>
          <p style="font-size: 1.5em; margin-top: 0.6em;">Model Parameters</p>
        </b-card-header>
      </div>
      <b-card-body style="min-height: 71.4vh">
        <!--Render all param sliders with correct labels, for each tab-->
        <div class="param-sliders" v-for="(tabData, index1) in tabsData" :key="tabData.data.label">
          <!--Only show tab data if tab is selected (isActive=true). Rendered nonetheless.-->
          <div v-show="tabData.isActive" v-for="(sliderData, index2) in tabData.data" :key="sliderData.label">
            <!--Pass each slider's data individually to slider component-->
            <SliderContent 
              :slider-data="sliderData"
              :current-sim-param-data="simParamData[currentSliderIndex(index1,index2)]"
              :sim-running="simRunning"
              v-on="$listeners"
              >
            </SliderContent>
            <SliderTicks :slider-data="sliderData"/>
          </div>
        </div>
        <PresetButtons
          v-on="$listeners"
          :param-suggestions="paramSuggestions"
          :user-presets="userPresets"
          :sim-running="simRunning"
        />
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
    simParamData: Array,
    simRunning: Boolean,
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
      return i1*this.tabsData[0].data.length + i2
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

<style scoped>
.param-sliders {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
