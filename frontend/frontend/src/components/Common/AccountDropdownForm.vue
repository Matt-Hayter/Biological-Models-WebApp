<!--eslint-disable-->
<template>
  <div class="account-dropdown-form">
    <b-dropdown-form @submit="onSubmitSignIn" style="width: 20em">
      <b-form-group label="Sign in to save model presets!" />
      <b-form-group label="Email" label-for="signin-email-input">
        <b-form-input
          id="signin-email-input"
          v-model="signIn.email"
          required
          size="sm"
          type="email"
          placeholder="email@example.com"
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Password" label-for="signin-passwd-input">
        <b-form-input
          id="signin-passwd-input"
          v-model="signIn.formPassword"
          type="password"
          size="sm"
          required
          placeholder="Password"
          :state="signInPasswdState"
          aria-describedby="feedback-invalid-signin-passwd"
        ></b-form-input>
        <!--Feedback for if input is invalid (in the false state)-->
        <b-form-invalid-feedback id="feedback-invalid-signin-passwd">
            Enter at least 6 characters
          </b-form-invalid-feedback>
      </b-form-group>
      <TempAlert 
        :alert-message="invalidSignInAlert.alertMessage"
        :alert-variant="invalidSignInAlert.alertVariant"
        :show-alert="invalidSignInAlert.showAlert"
        :alert-secs="invalidSignInAlert.alertSecs"
        @resetAlert="resetInvalidSignInAlert"
      />
      <br />
      <b-button type="submit" variant="outline-dark" size="sm">Sign In</b-button>
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
          label-for="signup-username-input"
          description="Usernames are converted to lower case"
        >
          <b-form-input
            id="signup-username-input"
            type="text"
            v-model="signUp.formUsername"
            :state="signUpUsernameState"
            required
            placeholder="Enter username"
            aria-describedby="feedback-invalid-username"
          >
          </b-form-input>
          <!--Feedback for if input is invalid (in the false state)-->
          <b-form-invalid-feedback id="feedback-invalid-username">
            Enter at least 4 characters
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group label="Email address:" label-for="signup-email-input">
          <b-form-input
            id="signup-email-input"
            type="email"
            v-model="signUp.formEmail"
            required
            placeholder="Enter email"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group label="Password:" label-for="signup-password-input">
          <b-form-input
            id="signup-password-input"
            type="password"
            v-model="signUp.formPassword"
            :state="signUpPasswdState"
            required
            placeholder="Enter password"
            aria-describedby="feedback-invalid-passwd"
          >
          </b-form-input>
          <b-form-invalid-feedback id="feedback-invalid-passwd">
            Enter at least 6 characters
          </b-form-invalid-feedback>
        </b-form-group>
        <TempAlert
          :alert-message="invalidSignUpAlert.usernameAlertMessage"
          :alert-variant="invalidSignUpAlert.usernameAlertVariant"
          :show-alert="invalidSignUpAlert.showUsernameAlert"
          :alert-secs="invalidSignUpAlert.alertSecs"
          @resetAlert="resetInvalidUsernameAlert"
        />
        <TempAlert
          :alert-message="invalidSignUpAlert.emailAlertMessage"
          :alert-variant="invalidSignUpAlert.emailAlertVariant"
          :show-alert="invalidSignUpAlert.showEmailAlert"
          :alert-secs="invalidSignUpAlert.alertSecs"
          @resetAlert="resetInvalidEmailAlert"
        />
        <br />
        <b-button type="submit" variant="outline-dark">Submit</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
/*eslint-disable*/
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
      signIn: {
        formEmail: "",
        formPassword: "",
      },
      //If alert is displayed within current component (if unsuccessful)
      invalidSignUpAlert: {
        alertSecs: 8,
        alertVariant: "warning",
        //For non-unique username alert
        showUsernameAlert: false,
        usernameAlertMessage:
          "That username is registered with another account, please choose another",
        //For non-unique email alert
        showEmailAlert: false,
        emailAlertMessage:
          "That email is registered with another account, please use another",
      },
      //If alert is displayed within current component (if unsuccessful)
      invalidSignInAlert: {
        alertSecs: 4,
        alertVariant: "warning",
        showAlert: false,
        alertMessage: "",
      },
    };
  },
  computed: {
    //Update form input state for password (valid or not), depending on current input length
    signUpUsernameState() {
      const usernameLength = this.signUp.formUsername.length;
      //Don't show as invalid if not yet typed
      if (usernameLength == 0) {
        return null;
      }
      //Needs to be longer than 5 characters
      return usernameLength >= 4 ? null : false;
    },
    signUpPasswdState() {
      const pswdLength = this.signUp.formPassword.length;
      //Don't show as invalid if not yet typed
      if (pswdLength == 0) {
        return null;
      }
      //Needs to be longer than 5 characters
      return pswdLength >= 6 ? null : false;
    },
    signInPasswdState() {
      const pswdLength = this.signIn.formPassword.length
      //Don't show as invalid if not yet typed
      if (pswdLength == 0) {
        return null;
      }
      //Needs to be longer than 5 characters
      return pswdLength >= 6 ? null : false;
    },
  },
  methods: {
    onSubmitSignUp(event) {
      event.preventDefault();
      //Don't process sign up if fields are not adequate
      if (
        this.signUpUsernameState == false ||
        this.signUpPasswdState == false
      ) {
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
    onSubmitSignIn(event) {
      event.preventDefault();
      //If password is too short to be valid
      if (this.signInPasswdState == false) {
        return;
      }
      //Handle server communication
      const payload = {
        email: this.signIn.formEmail,
        password: this.signIn.formPassword,
      };
      this.signInUser(payload);
    },
    //Add and validate user sign up data against database
    async addUser(payload) {
      const path = "http://localhost:5000/Account";
      try {
        const response = await axios.post(path, payload); //Send payload to server and async await response
        let input_valid = true;
        if (response.data["username_error"] == true) {
          this.invalidSignUpAlert.showUsernameAlert = true;
          input_valid = false;
          console.log("non-unique username error");
        }
        if (response.data["email_error"] == true) {
          this.invalidSignUpAlert.showEmailAlert = true;
          input_valid = false;
          console.log("non-unique email error");
        }
        //If server response says username or email is not unique
        if (input_valid == false) {
          return;
        }
        //Handle success message alert
        this.$refs.signUpModal.hide(); //Hide modal following submission
        const success_alert_obj = {
          message: "Account created and signed in!",
          variant: "success",
        };
        this.$emit("showPageAlert", success_alert_obj); //Emit event to create success alert on main page
        this.$emit("activateUsername", payload.username); //Emit event to set current user's unique username on client side
        console.log("Account created");
        //In case of axios problems, give error alert
      } catch (error) {
        this.$refs.signUpModal.hide(); //Hide modal following submission
        const alert_obj = {
          message: "Error creating account, failed connecting to server",
          variant: "danger",
        };
        this.$emit("showPageAlert", alert_obj); //Emit event to create failure alert on main page
        console.log("No account created, server problem");
      }
    },
    //Add and validate user sign up data against database
    async signInUser(payload) {
      const path = "http://localhost:5000/Account";
      try {
        const response = await axios.get(path, payload); //Send payload to server and async await response
        //If email/password comb not found, show alert on form
        if (
          response.data["username_error"] == true ||
          response.data["email_error"] == true
        ) {
          this.invalidSignInAlert.showAlert = true;
          console.log("No sign in, invalid sign in details");
          return;
        }
        //Handle success message alert (emit for main page alert)
        this.$emit("hideDropdown"); //Emit event to Navbar, hiding sign in form following submission
        const success_alert_obj = {
          message: `Signed in as ${response.data.username}`,
          variant: "success",
        };
        this.$emit("showPageAlert", success_alert_obj); //Emit event to create success alert on main page
        this.$emit("activateUsername", response.data.username); //Emit event to set current user's unique username on client side
        console.log("Signed in");
        //In case of axios problems, give error alert
      } catch (error) {
        this.$emit("hideDropdown"); //Emit event to Navbar, hiding sign in form following submission
        const unsucc_alert_obj = {
          message: "Error signing in, failed connecting to server",
          variant: "danger",
        };
        this.$emit("showPageAlert", unsucc_alert_obj); //Emit event to create failure alert on main page
        console.log("No sign in, server problem");
      }
    },
    resetInvalidUsernameAlert() {
      this.invalidSignUpAlert.showUsernameAlert = false;
    },
    resetInvalidEmailAlert() {
      this.invalidSignUpAlert.showEmailAlert = false;
    },
    resetInvalidSignInAlert() {
      this.invalidSignInAlert.showAlert = false;
    },
  },
};
</script>
