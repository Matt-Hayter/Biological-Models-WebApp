<!--eslint-disable-->
<template>
  <div class="config-bar">
    <!--Enclose config within card-->
    <b-card class="rounded-0" style="min-width: 25em; position: fixed" no-body>
      <b-card-header header-tag="nav">
        <b-nav card-header tabs fill style="display: flex; flex-direction: column">
          <p class="mt-3" style="font-size: 1.5em">Model Parameters</p>
          <div tabs style="margin-top:-1em">
            <b-nav-item style="float: left" :active="tabOneActive" @click="onTabOneClick()" >
              {{ configTabTitles[0] }}
            </b-nav-item>
            <b-nav-item style="float: left" :active="tabTwoActive" @click="onTabTwoClick()">
              {{ configTabTitles[1] }}
            </b-nav-item>
          </div>
        </b-nav>
      </b-card-header>
      <b-card-body style="min-height: 68vh">
        <!--Display all param sliders with correct labels, depending on page-->
        <div v-for="sliderData in currentTabData" :key="sliderData.label">
          <!--Passes events emitted from slider up the inheritance hierachy-->
          <SliderContent 
            :slider-data="sliderData"
            v-on="$listeners"
            >
          </SliderContent>
          <SliderTicks :slider-data="sliderData"/>
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
    tabOneData: Array,
    tabTwoData: Array,
    configTabTitles: Array
  },
  components: {
    SliderContent,
    SliderTicks,
  },
  data() {
    return {
      //Default confnig bar status
      currentTabData: this.tabOneData,
      tabOneActive: true,
      tabTwoActive: false,
    };
  },
  methods: {
    onTabOneClick() {
      this.currentTabData = this.tabOneData;
      this.tabOneActive = true;
      this.tabTwoActive = false;
    },
    onTabTwoClick() {
      this.currentTabData = this.tabTwoData;
      this.tabTwoActive = true;
      this.tabOneActive = false;
    },
  }
};
</script>
