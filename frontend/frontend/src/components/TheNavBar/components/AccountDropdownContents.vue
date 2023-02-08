<template>
  <!--Change dropdown contents depending on sign-in status-->
  <div v-if="!$store.state.activeUser.isActive" class="signed-out-dropdown">
    <b-dropdown-form @submit="onSubmitSignIn" style="width: 20em">
      <b-form-group label="Sign in to save model presets!" />
      <b-form-group label="Email" label-for="signin-email-input">
        <b-form-input
          id="signin-email-input"
          v-model="signIn.formEmail"
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
          Please enter a password with at least 8 characters
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
      <b-button type="submit" variant="outline-success" size="sm"
        >Sign In</b-button
      >
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
      centered
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
            Please enter at least 4 characters
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="Email address:"
          label-for="signup-email-input"
          description="Once submitted, account email address cannot be changed"
        >
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
            Please enter at least 8 characters
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
        <b-button type="submit" variant="outline-success">Submit</b-button>
      </b-form>
    </b-modal>
  </div>
  <div v-else class="signed-in-dropdown">
    <b-dropdown-form>
      <b-form-group>
        <b-form-text
          style="font-size: 1.1em; display: flex; flex-direction: column"
        >
          <div class="first-row">
            <div style="padding-top: 0.24em; float: left">User:</div>
            <div class="username-text">
              {{ $store.state.activeUser.username }}
            </div>
          </div>
          <div class="second-row" style="padding-top: 0.24em">
            <div style="float: left">Email:</div>
            <div style="padding-left: 0.4em; float: left">
              {{ $store.state.activeUser.email }}
            </div>
          </div>
        </b-form-text>
      </b-form-group>
      <b-dropdown-divider></b-dropdown-divider>
      <b-dropdown-item-button @click="onClickSignOut">
        <b>Sign out</b>
      </b-dropdown-item-button>
    </b-dropdown-form>
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
        alertMessage:
          "Account not found, please check email and password or create an account",
      },
    };
  },
  computed: {
    //Access Vuex store containing active user info
    activeUser() {
      return this.$store.state.activeUser;
    },
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
      //Needs to be longer than 7 characters
      return pswdLength >= 8 ? null : false;
    },
    signInPasswdState() {
      const pswdLength = this.signIn.formPassword.length;
      //Don't show as invalid if not yet typed
      if (pswdLength == 0) {
        return null;
      }
      //Needs to be longer than 7 characters
      return pswdLength >= 8 ? null : false;
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
    //Sign out user, and clear frontend of data
    onClickSignOut() {
      //Clear client-side user data
      const userStatePayload = {
        username: "",
        email: "",
        isActive: false,
      };
      this.$store.commit("userUpdate", userStatePayload); //call userUpdate state mutation
      this.$emit("initPresets") //Clear previous user's presets
      const alertPayload = {
        message: "Signed out, see you soon!",
        variant: "success",
      };
      this.$emit("showPageAlert", alertPayload); //Emit event to create success alert on main page
      console.log("Signed out!");
    },
    //Add and validate user sign up data against database
    async addUser(payload) {
      const path = "http://localhost:5000/SignUp";
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
        const successAlertPayload = {
          message: `Account created, welcome ${response.data["username"]}`,
          variant: "success",
        };
        this.$emit("showPageAlert", successAlertPayload); //Create successful sign in alert on main page
        this.activateUserState(response) //Update Vuex state with user's data
        console.log("Account created");
        this.$emit("loadPresets") //Load all user's presets
        this.initSignUpForm(); //Reset form
        //In case of axios problems, give error alert
      } catch (error) {
        this.$refs.signUpModal.hide(); //Hide modal following submission
        const alert_obj = {
          message: "Error creating account, failed response from server",
          variant: "danger",
        };
        this.$emit("showPageAlert", alert_obj); //Emit event to create failure alert on main page
        console.log("No account created, server problem");
      }
    },
    //Add and validate user sign up data against database
    async signInUser(payload) {
      const path = "http://localhost:5000/SignIn";
      try {
        const response = await axios.post(path, payload); //Send payload to server and async await response
        //If email/password comb not found, show alert on form
        if (response.data["username"] == null) {
          this.invalidSignInAlert.showAlert = true;
          console.log("No sign in, invalid sign in details");
          return;
        }
        //Handle success message alert (emit for main page alert)
        this.$emit("hideDropdown"); //Emit event to Navbar, hiding sign in form following submission
        const success_alert_obj = {
          message: `Welcome ${response.data["username"]}`,
          variant: "success",
        };
        this.$emit("showPageAlert", success_alert_obj); //Create success alert on main page
        this.activateUserState(response) //Update Vuex state with user's data
        console.log(
          "Signed in as ",
          response.data["username"],
          response.data["email"]
        );
        this.initSignInForm(); //Reset form
        this.$emit("loadPresets") //Load all user's presets
        //In case of axios problems, give error alert
      } catch (error) {
        this.$emit("hideDropdown"); //Emit event to Navbar, hiding sign in form following submission
        const unsucc_alert_obj = {
          message: "Error signing in, failed response from server",
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
    initSignInForm() {
      this.signIn.formEmail = null;
      this.signIn.formPassword = null;
    },
    initSignUpForm() {
      this.signUp.formUsername = null;
      this.signUp.formEmail = null;
      this.signUp.formPassword = null;
    },
    //Update Vuex store state with signed in user's data
    activateUserState(response) {
      const userStatePayload = {
        username: response.data["username"],
        email: response.data["email"],
        isActive: true,
      }
      this.$store.commit("userUpdate", userStatePayload); //call userUpdate Vuex state mutation
    },
    //Update Vuex store state with signed in user's data
    activateUserState(response) {
      const userStatePayload = {
        username: response.data["username"],
        email: response.data["email"],
        isActive: true,
      }
      this.$store.commit("userUpdate", userStatePayload); //call userUpdate Vuex state mutation
    },
    //Update Vuex store state with signed in user's data
    activateUserState(response) {
      const userStatePayload = {
        username: response.data["username"],
        email: response.data["email"],
        isActive: true,
      }
      this.$store.commit("userUpdate", userStatePayload); //call userUpdate Vuex state mutation
    },
    //Update Vuex store state with signed in user's data
    activateUserState(response) {
      const userStatePayload = {
        username: response.data["username"],
        email: response.data["email"],
        isActive: true,
      }
      this.$store.commit("userUpdate", userStatePayload); //call userUpdate Vuex state mutation
    },
  },
};
</script>

<style scoped>
.username-text {
  float: left;
  padding-left: 0.4em;
  color: rgb(49, 49, 49);
  font-size: 1.3em;
}
</style>
