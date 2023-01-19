<!--eslint-disable-->
<template>
  <div class="account-dropdown-form">
    <b-dropdown-form style="width: 17em">
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
    <!--Mount sign up modal to button-->
    <b-dropdown-item-button v-b-modal.sign-up>
      New around here? Sign up
    </b-dropdown-item-button>
    <b-dropdown-item-button>Forgot Password?</b-dropdown-item-button>
    <!--Sign up modal-->
    <b-modal
      ref="signUpModal"
      id="sign-up"
      title="Create an Account"
      >
      <b-form @submit="onSubmitSignUp">
        <b-form-group
          label="Username:"
          label-for="form-username-input"
          >
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="signUp.username"
            required
            placeholder="Enter username">
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Email address:"
          label-for="form-email-input"
          >
          <b-form-input
            id="form-email-input"
            type="text"
            v-model="signUp.email"
            required
            placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Password:"
          label-for="form-password-input"
          >
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="signUp.password"
            required
            placeholder="Enter password">
          </b-form-input>
        </b-form-group>
        <br>
        <b-button type="submit" variant="outline-info">Submit</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios"; //For making client-side http requests

export default {
  props: {
    message: String,
  },
  data() {
    return {
      //Default sign up values
      signUp: {
        username: "",
        email: "",
        passsword: "",
      },
    };
  },
  methods: {
    async onSubmitSignUp(event) {
      try {
        event.preventDefault();
        this.$refs.signUpModal.hide(); //Hide modal following submission

        //Handle server communication
        const serverPayload = {
          username: this.username,
          email: this.email,
          password: this.password,
        };
        const path = "http://localhost:5000/";
        await axios.post(path, serverPayload); //Send payload to server

        //Handle message update
        const message = "Account created!";
        this.$emit("messageUpdate", message); //Emit event to create page alert
        //In case of axios problems
      } catch (error) {
        const message = "Error creating account, please try again";
        this.$emit("messageUpdate", message);
      }
    },
  },
};
</script>
