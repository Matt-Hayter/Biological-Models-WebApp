<template>
  <!--Change dropdown contents depending on sign-in status-->
  <div v-if="!user.isActive" class="signed-out-dropdown">
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
        :alert-message="invalidSignInAlert.message"
        :alert-variant="invalidSignInAlert.variant"
        :show-alert="invalidSignInAlert.show"
        :alert-secs="invalidSignInAlert.secs"
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
          :alert-message="invalidSignUpAlert.usernameMessage"
          :alert-variant="invalidSignUpAlert.usernameVariant"
          :show-alert="invalidSignUpAlert.showUsernameAlert"
          :alert-secs="invalidSignUpAlert.secs"
          @resetAlert="resetInvalidUsernameAlert"
        />
        <TempAlert
          :alert-message="invalidSignUpAlert.emailMessage"
          :alert-variant="invalidSignUpAlert.emailVariant"
          :show-alert="invalidSignUpAlert.showEmailAlert"
          :alert-secs="invalidSignUpAlert.secs"
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
        <b-form-text style="font-size: 1.1em">
            <span style="padding-top: 0.24em; float: left">User:</span>
            <span class="username-text">
              {{ user.username }}
            </span>
        </b-form-text>
      </b-form-group>
      <b-dropdown-divider></b-dropdown-divider>
      <div style="margin-left: -10px;">
        <b-dropdown-item-button v-b-modal.manage-account-modal>
          <b>Manage account</b>
        </b-dropdown-item-button>
        <b-dropdown-item-button @click="onClickSignOut">
          <b>Sign out</b>
        </b-dropdown-item-button>
      </div>
    </b-dropdown-form>
    <!--Manage account modal-->
    <b-modal
      ref="manageAccountModal"
      id="manage-account-modal"
      title="Manage Account"
      hide-footer
      centered
      >
      <b-form-text class="account-info-text">
        <div class="first-row">
          <div style="padding-top: 0.24em; float: left">Username:</div>
          <!--Username display, with editable username-->
          <div v-if="!editingUsername">
            <div class="username-text">
              {{ user.username }}
            </div>
            <b-button class="edit-username-button" @click="onClickEditUsername">
              <b-icon icon="pencil" shift-v="10" shift-h="-9" />
            </b-button>
          </div>
          <!--Edit username form display-->
          <div v-else-if="editingUsername" class="edit-username-section">
            <b-input-group>
              <b-form-input 
                id="manage-account-username-input"
                type="text"
                v-model="newUsername"
                :state="newUsernameState"
                placeholder="New username"
                aria-describedby="feedback-invalid-username"
              />
              <b-input-group-append>
                <b-button-group>
                  <b-button variant="outline-success" @click="onClickSubmitNewUsername">Save</b-button>
                  <b-button variant="outline-primary" @click="onClickCancelEditUsername"><b-icon icon="x"></b-icon></b-button>
                </b-button-group>
              </b-input-group-append>
              <!--Feedback for if input is invalid (in the false state)-->
              <b-form-invalid-feedback id="feedback-invalid-username">
                Please enter at least 4 characters
              </b-form-invalid-feedback>
            </b-input-group>
            <TempAlert
              :alert-message="newUsernameAlert.message"
              :alert-variant="newUsernameAlert.variant"
              :show-alert="newUsernameAlert.show"
              :alert-secs="newUsernameAlert.secs"
              @resetAlert="resetNewUsernameAlert"
            />
          </div>
        </div>
        <div class="second-row" style="padding-top: 0.24em">
          <div style="float: left">Email:</div>
          <div class="email-text">
            {{ user.email }}
          </div>
        </div>
      </b-form-text>
      <br />
      <b-button v-b-modal.delete-account style="float: right;" @click="onClickDeleteAccountModal">
        <b-form-text>
          Delete Account
        </b-form-text>
      </b-button>
    </b-modal>
    <b-modal
      ref="deleteAccountModal"
      id="delete-account"
      hide-footer
      centered
      >
      <template #modal-title>
        Account deletion <b-icon icon="exclamation-triangle" variant="danger" scale="1.2" shift-v="1" />
      </template>
      <b>Removing your account will permanently delete all of your associated data,
        including all saved presets</b>
      <b-button style="margin-top: 30px;" variant="outline-danger">
        Delete Account
      </b-button>
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
      //Default sign up and sign in values
      signUp: {
        formUsername: "",
        formEmail: "",
        formPassword: "",
      },
      signIn: {
        formEmail: "",
        formPassword: "",
      },
      //Account management data
      editingUsername: false,
      newUsername: "",
      //Alert displayed within current component (if unsuccessful)
      invalidSignUpAlert: {
        secs: 8,
        variant: "warning",
        //For non-unique username alert
        showUsernameAlert: false,
        usernameMessage:
          "That username is registered with another account, please choose another",
        //For non-unique email alert
        showEmailAlert: false,
        emailMessage:
          "That email is registered with another account, please use another",
      },
      //Alert displayed within current component (if unsuccessful)
      invalidSignInAlert: {
        secs: 4,
        variant: "warning",
        show: false,
        message:
          "Account not found, please check email and password or create an account",
      },
      //alert displayed within current component (successful or unsuccessful)
      newUsernameAlert: {
        secs: 8,
        variant: null, //Variable
        show: false,
        message: null, //Variable
      },
    };
  },
  computed: {
    //Access Vuex store containing active user info
    user() {
      return this.$store.state.user;
    },
    //Update form input states (valid or not), depending on current input lengths
    newUsernameState() {
      const usernameLength = this.newUsername.length;
      //Needs to be longer than 5 characters. Don't accept 0 characters
      return usernameLength >= 4 ? null : false;
    },
    signUpUsernameState() {
      const usernameLength = this.signUp.formUsername.length;
      return this.usernameStatus(usernameLength)
    },
    signUpPasswdState() {
      const pswdLength = this.signUp.formPassword.length;
      return this.passwdStatus(pswdLength)
    },
    signInPasswdState() {
      const pswdLength = this.signIn.formPassword.length;
      return this.passwdStatus(pswdLength)
    },
  },
  methods: {
    usernameStatus(usernameLength) {
      //Don't show as invalid if not yet typed
      if (usernameLength == 0) {
        return null;
      }
      //Needs to be longer than 5 characters
      return usernameLength >= 4 ? null : false;
    },
    passwdStatus(pswdLength) {
      //Don't show as invalid if not yet typed
      if (pswdLength == 0) {
        return null;
      }
      //Needs to be longer than 7 characters
      return pswdLength >= 8 ? null : false;
    },
    onSubmitSignUp(event) {
      event.preventDefault();
      //Don't process sign up if fields are not adequate
      if (this.signUpUsernameState == false || this.signUpPasswdState == false) {
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
      if (this.signInPasswdState == false) {return}
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
    onClickEditUsername() {
      this.editingUsername = true
    },
    onClickCancelEditUsername() {
      this.editingUsername = false
      this.newUsername = ""
    },
    onClickSubmitNewUsername() {
      //If username is not valid
      if (this.newUsernameState == false) {return}
      const payload = {
        newUsername: this.newUsername,
        email: this.user.email //To identify user
      }
      this.changeUsername(payload)
    },
    onClickDeleteAccountModal() {
      this.$refs.manageAccountModal.hide()
    },
    //Add and validate user sign up data against database
    async addUser(payload) {
      const path = "http://localhost:5000/Account/SignUp";
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
      const path = "http://localhost:5000/Account/SignIn";
      try {
        const response = await axios.post(path, payload); //Send payload to server and async await response
        //If email/password comb not found, show alert on form
        if (response.data["username"] == null) {
          this.invalidSignInAlert.show = true;
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
    async changeUsername() {
      const path = "http://localhost:5000/Account/ChangeUsername";
      try {
        const response = await axios.put(path, payload); //Send payload to server
        console.log("here")
        if (response.data["username_error"]) { //If server response says username is not unique
          //Failure alert on modal
          this.newUsernameAlert.message = 
            "Username already in use, please select another. Entries are converted to lower case."
          this.newUsernameAlert.variant = "warning"
          this.newUsernameAlert.show = true;
          console.log("non-unique username error");
          return
        }
        //If successful:
        //Show success alert on modal
        this.newUsernameAlert.message = "Username updated successfully"
        this.newUsernameAlert.variant = "success"
        this.newUsernameAlert.show = true;
        this.$store.commit("usernameUpdate", response.data["username"]); //Update vuex state
        console.log("Username updated");
        //Reset input params for username change
        this.newUsername = ""
        this.editingUsername = false
        //In case of axios problems, give error alert
      } catch (error) {
        this.$refs.manageAccountModal.hide()
        this.newUsername = ""
        this.editingUsername = false
        const alert_obj = {
          message: "Error changing username, failed response from server",
          variant: "danger",
        };
        this.$emit("showPageAlert", alert_obj); //Emit event to create failure alert on main page
        console.log("No username change, server problem");
      }
    },
    resetInvalidUsernameAlert() {
      this.invalidSignUpAlert.showUsernameAlert = false;
    },
    resetInvalidEmailAlert() {
      this.invalidSignUpAlert.showEmailAlert = false;
    },
    resetInvalidSignInAlert() {
      this.invalidSignInAlert.show = false;
    },
    resetNewUsernameAlert() {
      this.newUsernameAlert.show = false;
      this.newUsernameAlert.message = null; //Variable params
      this.newUsernameAlert.variant = null;
    },
    initSignInForm() {
      this.signIn.formEmail = "";
      this.signIn.formPassword = "";
    },
    initSignUpForm() {
      this.signUp.formUsername = "";
      this.signUp.formEmail = "";
      this.signUp.formPassword = "";
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
.first-row {
  display: flex;
  flex-direction: row;
}
.account-info-text {
  font-size: 1.1em;
  display: flex;
  flex-direction: column;
}
.username-text {
  float: left;
  padding-left: 0.4em;
  color: rgb(49, 49, 49);
  font-size: 1.3em;
}
.email-text {
  float: left;
  padding-left: 0.4em;
  color: rgb(49, 49, 49);
}
.edit-username-button {
  margin-left: 8px;
  max-width: 20px;
  height: 36px;
  padding: 15px;
}
.edit-username-section {
  font-size: 0.9em;
  margin-left: 8px;
  margin-top: -8px;
}
</style>
