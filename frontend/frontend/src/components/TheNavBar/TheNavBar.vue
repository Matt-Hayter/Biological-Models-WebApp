<!-- eslint-disable-->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Biological Models Visualiser</a>
      <div class="collapse navbar-collapse" id="navbarColor02">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
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
          </li>
          <li class="nav-item">
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
                <b-dropdown-item @click="onSEIRClick">SEIR Model</b-dropdown-item>
              </b-dropdown-group>
              <br>
              <b-dropdown-group header="Extended">
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item class="tex2jax_ignore" @click="onSEI3RDClick">
                  <template id="#text">
                    SEI<sup>3</sup>RD Model (COVID)
                  </template>
                </b-dropdown-item>
              </b-dropdown-group>
            </b-dropdown>
          </li>
        </ul>
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
      this.$router.push("/PredatorPrey");
      this.VueMathjax.typeset();
    },
    onCompSpecClick() {
      this.$router.push("/CompetingSpecies");
      this.VueMathjax.typeset();
    },
    onSEIRClick() {
      this.$router.push("/SEIR");
    },
    onSEI3RDClick() {
      this.$router.push("/SEI3RD");
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
