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
                <b-dropdown-item>Predator-Prey</b-dropdown-item>
                <b-dropdown-item>Competing Species</b-dropdown-item>
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
              <b-dropdown-item>SEIR Model</b-dropdown-item>
              <b-dropdown-item>SEI$^{3}$D Model $($COVID$)$</b-dropdown-item>
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
          <b-dropdown-form>
            <b-form-group
              label="Email"
              label-for="dropdown-form-email"
              @submit.stop.prevent
            >
              <b-form-input
                id="dropdown-form-email"
                size="sm"
                placeholder="email@example.com"
              ></b-form-input>
            </b-form-group>

            <b-form-group label="Password" label-for="dropdown-form-password">
              <b-form-input
                id="dropdown-form-password"
                type="password"
                size="sm"
                placeholder="Password"
              ></b-form-input>
            </b-form-group>

            <b-form-checkbox class="mb-3">Remember me</b-form-checkbox>
            <b-button variant="primary" size="sm" @click="onClick"
              >Sign In
            </b-button>
          </b-dropdown-form>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item-button>
            New around here? Sign up
          </b-dropdown-item-button>
          <b-dropdown-item-button>Forgot Password?</b-dropdown-item-button>
        </b-dropdown>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
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
  },
};
</script>

<style scoped>
.navbar-brand:hover {
  color: rgb(204, 204, 204);
}
</style>
