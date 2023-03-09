<template>
  <div class="temp-alert">
    <b-alert
      :show="alertCountDown"
      :variant="alertVariant"
      fade
      @dismissed="alertCountDown = 0"
      @dismiss-count-down="countDownChanged"
    >
      <p>{{ alertMessage }}</p>
      <!--Progress alert timer-->
      <b-progress
        :max="alertSecs"
        :value="alertCountDown"
        height="3px"
      ></b-progress>
    </b-alert>
  </div>
</template>

<script>
export default {
  props: {
    showAlert: Boolean,
    alertMessage: String,
    alertVariant: String,
    alertSecs: Number,
  },
  data() {
    return {
      alertCountDown: 0,
    };
  },
  watch: {
    //If alertMessage prop changes, there is a new alert
    showAlert() {
      if (this.showAlert == true) {
        //Show alert and start timer (b-alert's show attribute enables an automatic countdown of binded data)
        this.alertCountDown = this.alertSecs;

        console.log("Showing alert");
        this.$emit("resetAlert"); //Set showAlert back to false before next alert
      }
    },
  },
  methods: {
    //Update timer upon alert's "dismiss-count-down" event (every sec)
    countDownChanged(timeLeft) {
      this.alertCountDown = timeLeft;
    },
  },
};
</script>
