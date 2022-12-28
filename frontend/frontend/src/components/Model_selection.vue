<template>
  <div class="Model_selection">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootswatch@5.2.3/dist/simplex/bootstrap.min.css"
    />
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Population Models Visualiser</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarColor02"
          aria-controls="navbarColor02"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarColor02">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <b-dropdown
                class="nav-link"
                href="#"
                right
                text="Single Species Models"
                variant="dark"
              >
                <b-dropdown-item>Malthusian Model</b-dropdown-item>
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item>Logistic Model</b-dropdown-item>
              </b-dropdown>
            </li>
            <li class="nav-item">
              <b-dropdown
                class="nav-link"
                right
                text="Multiple Species Models"
                variant="dark"
              >
                <b-dropdown-item>Predator-Prey</b-dropdown-item>
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item>Competing Species</b-dropdown-item>
              </b-dropdown>
            </li>
            <li>
              <b-dropdown
                class="nav-link text-white"
                text="Account"
                variant="dark"
              >
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

                  <b-form-group
                    label="Password"
                    label-for="dropdown-form-password"
                  >
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
                <b-dropdown-item-button>
                  Forgot Password?
                </b-dropdown-item-button>
              </b-dropdown>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {};
</script>
