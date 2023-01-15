<!-- eslint-disable-->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Population Models Visualiser</a>
      <div class="collapse navbar-collapse" id="navbarColor02">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <!--Bind single-species hover prop to variant attribute-->
            <!--Listen to events @mousover and @mousleave directly from DOM using .native (Vue dropdown component doesn't emit these events)-->
            <b-dropdown
              class="nav-link dropdown-link"
              href="#"
              right
              text="Single Species Models"
              v-bind:variant="singleSpecHover"
              @mouseover.native="singleSpecHover = 'light'"
              @mouseleave.native="singleSpecHover = 'dark'"
            >
              <b-dropdown-item>Malthusian Model</b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item>Logistic Model</b-dropdown-item>
            </b-dropdown>
          </li>
          <li class="nav-item">
            <!--Bind multiple-species hover prop to variant attribute-->
            <b-dropdown
              class="nav-link"
              right
              text="Multiple Species Models"
              :variant="multSpecHover"
              @mouseover.native="multSpecHover = 'light'"
              @mouseleave.native="multSpecHover = 'dark'"
            >
              <b-dropdown-item>Predator-Prey</b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item>Competing Species</b-dropdown-item>
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
      singleSpecHover: "dark",
      multSpecHover: "dark",
    };
  },
  methods: {},
};
</script>

<style scoped>
.navbar-brand:hover {
  color: rgb(204, 204, 204);
}
</style>
