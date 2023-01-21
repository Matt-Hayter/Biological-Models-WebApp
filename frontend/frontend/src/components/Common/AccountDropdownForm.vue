<!--eslint-disable-->
<template>
  <div class="account-dropdown-form">
    <b-dropdown-form style="width: 20em">
      <b-form-group
        label="Sign in to save model presets!"
      >
      </b-form-group>
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
      <br>
      <b-button variant="primary" size="sm" @click="onClick"
        >Sign In
      </b-button>
    </b-dropdown-form>
    <b-dropdown-divider></b-dropdown-divider>
    <!--Mount sign up modal to button-->
    <b-dropdown-item-button v-b-modal.sign-up>
      New around here? <b>Sign up</b>
    </b-dropdown-item-button>
    <!--Sign up modal-->
    <b-modal
      ref="signUpModal"
      id="sign-up"
      title="Create an Account"
      hide-footer
      >
      <b-form @submit="onSubmitSignUp">
        <b-form-group
          label="Username:"
          label-for="form-username-input"
          description="Usernames are converted to lower case"
          >
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="signUp.formUsername"
            :state="usernameState"
            required
            placeholder="Enter username"
            aria-describedby="feedback-invalid-username"
          >
          </b-form-input>
          <!--Feedback for if previous input is invalid (in the false state)-->
          <b-form-invalid-feedback id="feedback-invalid-username">
            Enter at least 4 characters
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="Email address:"
          label-for="form-email-input"
          >
          <b-form-input
            id="form-email-input"
            type="email"
            v-model="signUp.formEmail"
            required
            placeholder="Enter email"
            >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Password:"
          label-for="form-password-input"
          >
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="signUp.formPassword"
            :state="passwdState"
            required
            placeholder="Enter password"
            aria-describedby="feedback-invalid-passwd"
          >
          </b-form-input>
          <b-form-invalid-feedback id="feedback-invalid-passwd">
            Enter at least 6 characters
          </b-form-invalid-feedback>
        </b-form-group>
        <TempAlert :alert-message="usernameAlertMessage" :alert-variant="usernameAlertVariant" :show-alert="showUsernameAlert" :alert-secs="alertSecs" @resetAlert="resetUsernameAlert" />
        <TempAlert :alert-message="emailAlertMessage" :alert-variant="emailAlertVariant" :show-alert="showEmailAlert" :alert-secs="alertSecs" @resetAlert="resetEmailAlert" />
        <br>
        <b-button type="submit" variant="outline-info">Submit</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import TempAlert from "@/components/common/TempAlert.vue";
import axios from "axios"; //For making client-side http requests

export default {
  components: {
    TempAlert,
  },
  data() {
    return {
      //Default sign up values
      signUp: {
        formUsername: "",
        formEmail: "",
        formPassword: "",
      },
      alertSecs: 8,
      //For non-unique username alert
      showUsernameAlert: false,
      usernameAlertMessage: "",
      usernameAlertVariant: "warning",
      //For non-unique email alert
      showEmailAlert: false,
      emailAlertMessage: "",
      emailAlertVariant: "warning",
    };
  },
  computed: {
    //Update form input state for password (valid or not), depending on current input length
    usernameState() {
      return this.signUp.formUsername.length >= 4 ? true : false;
    },
    passwdState() {
      return this.signUp.formPassword.length >= 6 ? true : false;
    },
  },
  methods: {
    onSubmitSignUp(event) {
      event.preventDefault();
      //Don't process sign up if fields are not adequate
      if (this.usernameState == false || this.passwdState == false) {
        return;
      }
      //Handle server communication
      const payload = {
        username: this.signUp.formUsername,
        email: this.signUp.formEmail,
        password: this.signUp.formPassword,
      };
      this.addUser(payload);
    },
    //Add and validate user sign up data against database
    async addUser(payload) {
      const path = "http://localhost:5000/Account";
      try {
        let input_valid = true;
        const response = await axios.post(path, payload); //Send payload to server and async await response
        if (response.data["username_error"] == true) {
          this.showUsernameAlert = true;
          this.usernameAlertMessage =
            "That username is already in use, please choose another";
          input_valid = false;
          console.log("non-unique username error");
        }
        if (response.data["email_error"] == true) {
          this.showEmailAlert = true;
          this.emailAlertMessage =
            "That email is already registered with an account, please use another";
          input_valid = false;
          console.log("non-unique email error");
        }
        //If server response says username or email is not unique
        if (input_valid == false) {
          return;
        }
        //Handle success message alert
        this.$refs.signUpModal.hide(); //Hide modal following submission
        const alert_obj = {
          message: "Account created and signed in!",
          variant: "success",
        };
        this.$emit("showPageAlert", alert_obj); //Emit event to create success alert on main page
        this.$emit("activateUsername", payload.username); //Emit event to set current user's unique username on client side
        console.log(response.data);
        //In case of axios problems, give error alert
      } catch (error) {
        this.$refs.signUpModal.hide(); //Hide modal following submission
        const alert_obj = {
          message: "Error creating account, failed connecting to server",
          variant: "danger",
        };
        this.$emit("showPageAlert", alert_obj); //Emit event to create failure alert on main page
      }
    },
    resetUsernameAlert() {
      this.showUsernameAlert = false;
    },
    resetEmailAlert() {
      this.showEmailAlert = false;
    },
  },
};
</script>
