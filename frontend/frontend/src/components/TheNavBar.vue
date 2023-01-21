<!-- eslint-disable-->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Biological Models Visualiser</a>
      <div class="collapse navbar-collapse" id="navbarColor02">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <!--Bind single-species hover prop to variant attribute-->
            <!--Listen to events @mousover and @mousleave directly from DOM using .native (Vue dropdown component doesn't emit these events)-->
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
            class="nav-link"
            right
            variant="dark"
            text="Account"
          >
            <!--Use icon within dropdown button-->
            <template #button-content>
              Account
              <b-icon icon="person-lines-fill" font-scale="1.6"></b-icon>
            </template>
            <!--Pass form submission events up the inheritance hierachy-->
            <AccountDropdownForm v-on="$listeners"/>
          </b-dropdown>
      </div>
    </div>
  </nav>
</template>

<script>
import AccountDropdownForm from "@/components/common/AccountDropdownForm.vue";

export default {
  components: {
    AccountDropdownForm,
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
