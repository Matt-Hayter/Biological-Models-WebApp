<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!--Section for bran and model categories dropdown-->
      <div class="navbar-model-categories" style="display: flex; justify-content: left;">
        <a class="navbar-brand" href="#">Biological Models Visualiser</a>
        <div id="navbarColor02">
          <b-dropdown
            class="nav-link dropdown-link"
            href="#"
            right
            text="Population Models"
            v-bind:variant="popModelsHover"
            @mouseover.native="popModelsHover = 'light'"
            @mouseleave.native="popModelsHover = 'dark'"
          >
            <b-dropdown-group header="Multiple Species Models">
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item @click="onPredPreyClick">Predator-Prey</b-dropdown-item>
              <br>
              <b-dropdown-item @click="onCompSpecClick">Competing Species</b-dropdown-item>
            </b-dropdown-group>
          </b-dropdown>
        </div>
        <div id="navbarColor02">
          <!--Bind multiple-species hover prop to variant attribute-->
          <b-dropdown
            class="nav-link"
            right
            text="Disease Spread Models"
            :variant="disSpreadHover"
            @mouseover.native="disSpreadHover = 'light'"
            @mouseleave.native="disSpreadHover = 'dark'"
          >
            <b-dropdown-group header="Standard">
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item @click="onSIRClick">SIR Model</b-dropdown-item>
            </b-dropdown-group>
            <br>
            <b-dropdown-group header="Extended">
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item class="tex2jax_ignore" @click="onSEIDRClick">
                <template id="#text">
                  SEIDR Model (COVID-19)
                </template>
              </b-dropdown-item>
            </b-dropdown-group>
          </b-dropdown>
        </div>
      </div>
      <!--For account section-->
      <div id="navbarColor02" style="display: flex; justify-content: right;">
        <b-dropdown
          ref = "signInForm"
          class="nav-link"
          right
          variant="dark"
        >
          <!--Use icon within dropdown button-->
          <template #button-content>
            Account
            <b-icon icon="person-lines-fill" font-scale="1.6"></b-icon>
          </template>
          <!--Pass form submission events up the inheritance hierachy-->
          <AccountDropdownContents v-on="$listeners" @hideDropdown="hideDropdownForm" />
        </b-dropdown>
      </div>
    </div>
  </nav>
</template>

<script>
import AccountDropdownContents from "@/components/TheNavBar/components/AccountDropdownContents.vue";

export default {
  components: {
    AccountDropdownContents,
  },
  data() {
    return {
      popModelsHover: "dark",
      disSpreadHover: "dark",
    };
  },
  methods: {
    onClick() {
      console.log("Do Something");
    },
    onPredPreyClick() {
      this.$store.commit("simRunningChange", false) //End current sim before navigating to next view
      this.$router.push("/PredatorPrey");
    },
    onCompSpecClick() {
      this.$store.commit("simRunningChange", false)
      this.$router.push("/CompetingSpecies");
    },
    onSIRClick() {
      this.$store.commit("simRunningChange", false)
      this.$router.push("/SIR");
    },
    onSEIDRClick() {
      this.$store.commit("simRunningChange", false)
      this.$router.push("/SEIDR");
    },
    //Emitted from account dropdown form component
    hideDropdownForm() {
      this.$refs.signInForm.hide(); //Hide sign in form following submission
    },
  },
};
</script>

<style scoped>
.navbar-brand:hover {
  color: rgb(204, 204, 204);
}
.nav-text {
  font-size: 2em;
}
</style>
