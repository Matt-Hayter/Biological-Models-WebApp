<template>
  <div class="config-bar">
    <!--Enclose config within card-->
    <b-card class="config-bar-card rounded-0" no-body>
      <!--If tabs are required-->
      <div v-if="configTabTitles.length == 2">
        <b-card-header header-tag="nav">
          <b-nav
            card-header
            tabs
            fill
            style="display: flex; flex-direction: column"
          >
            <p style="font-size: 1.5em; margin-bottom: -0.07em">
              Model Parameters
            </p>
            <div tabs>
              <b-nav-item
                style="float: left"
                :active="tabsData[0].isActive"
                @click="onTabOneClick()"
              >
                {{ configTabTitles[0] }}
              </b-nav-item>
              <b-nav-item
                style="float: left"
                :active="tabsData[1].isActive"
                @click="onTabTwoClick()"
              >
                {{ configTabTitles[1] }}
              </b-nav-item>
            </div>
          </b-nav>
        </b-card-header>
      </div>
      <!--If no tabs required-->
      <div v-else-if="configTabTitles.length == 1">
        <b-card-header>
          <p style="font-size: 1.5em; margin-top: 0.6em">Model Parameters</p>
        </b-card-header>
      </div>
      <b-card-body style="min-height: 71.4vh">
        <!--Render all param sliders with correct labels, for each tab-->
        <div v-for="(tabData, index1) in tabsData" :key="tabData.data.label">
          <!--Only show tab data if tab is selected (isActive=true). Rendered nonetheless.-->
          <div
            class="ticks"
            v-show="tabData.isActive"
            v-for="(sliderData, index2) in tabData.data"
            :key="sliderData.label"
          >
            <!--Pass each slider's data individually to slider component-->
            <SliderContent
              ref="sliders"
              :slider-data="sliderData"
              :current-sim-param-data="
                simParamData[currentSliderIndex(index1, index2)]
              "
              v-on="$listeners"
            >
            </SliderContent>
            <SliderTicks :slider-data="sliderData" />
          </div>
        </div>
        <PresetButtons
          class="preset-buttons"
          v-on="$listeners"
          :param-suggestions="paramSuggestions"
          :user-presets="userPresets"
        />
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import SliderContent from "@/components/config-bar/components/SliderContent.vue";
import SliderTicks from "@/components/config-bar/components/SliderTicks.vue";
import PresetButtons from "@/components/config-bar/components/PresetButtons.vue";

export default {
  props: {
    tabsData: Array,
    configTabTitles: Array,
    paramSuggestions: Array,
    userPresets: Array,
    simParamData: Array,
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
      return i1 * this.tabsData[0].data.length + i2;
    },
    onTabOneClick() {
      //Close all parameter descriptions for current tab
      this.$refs.sliders.forEach((slider) => {
        slider.tabClick();
      });
      //Update tabsData[i].isActive props if tab changes (delay allows for param description closure)
      setTimeout(() => this.$emit("tabOneActive"), 15);
    },
    onTabTwoClick() {
      this.$refs.sliders.forEach((slider) => {
        slider.tabClick();
      });
      setTimeout(() => this.$emit("tabTwoActive"), 15);
    },
  },
};
</script>

<style scoped>
.ticks {
  padding: 0 1.2em;
}
.param-sliders {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.config-bar-card {
  width: 25em;
  position: relative;
  float: left;
  height: 100vh;
}
.preset-buttons {
  position: absolute;
  bottom: 130px;
}
</style>
