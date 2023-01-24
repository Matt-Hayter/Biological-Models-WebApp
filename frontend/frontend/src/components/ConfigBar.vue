<!--eslint-disable-->
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
        <div v-for="tabData in tabsData" :key="tabData.data.label">
          <!--Only show tab data if tab is selected (isActive=true). Rendered nonetheless.-->
          <div v-show="tabData.isActive" v-for="sliderData in tabData.data" :key="sliderData.label">
            <!--Passes events emitted from slider up the inheritance hierachy-->
            <SliderContent 
              :slider-data="sliderData"
              v-on="$listeners"
              >
            </SliderContent>
            <SliderTicks :slider-data="sliderData"/>
          </div>
        </div>
        <b-button-group style="padding: 1em 0.5em">
          <b-button class="btn-success">
            Save <b-icon icon="box-arrow-in-down" font-scale="1.5"></b-icon>
          </b-button>
          <b-button  class="btn-info">
            My Presets
          </b-button>
        </b-button-group>
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
    tabsData: Array,
    configTabTitles: Array
  },
  components: {
    SliderContent,
    SliderTicks,
  },
  data() {
    return {};
  },
  methods: {
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
