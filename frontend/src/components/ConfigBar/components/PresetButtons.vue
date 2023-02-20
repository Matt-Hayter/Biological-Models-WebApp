<template>
  <div class="preset-buttons">
    <div class="preset-save-list">
      <b-button-group class="preset-button-bar">
        <!--Save button-->
        <b-button id="save-button" class="btn-success" @click="onClickSave">
          Save <b-icon icon="box-arrow-in-down" font-scale="1.4" shift-v="1.5"></b-icon>
        </b-button>
        <!--Presets dropdown-->
        <b-dropdown dropright :disabled="simRunning" variant="info" no-caret @show="onClickDropdown">
          <template #button-content>
            My Presets <b-icon icon="justify" font-scale="1.5" style="margin-left: 4em"></b-icon>
          </template>
          <span v-if="emptyPresetsSignedOut">
            <b-dropdown-text>No presets to show!</b-dropdown-text>
            <b-dropdown-text>Sign in, and saved presets for this model will appear here</b-dropdown-text>
          </span>
          <span v-else-if="emptyPresetsSignedIn">
            <b-dropdown-text>No saved presets - try saving one! </b-dropdown-text>
          </span>
          <!--If signed in, and have saved presets-->
          <div v-for="(preset, index) in userPresetsUpdate" :key="preset[0]">
            <b-button-toolbar style="width: max-content;">
              <b-dropdown-item-button @click="onPresetClick(index)">
                <b style="font-size: 1.2em;">{{ preset[1] }}</b>, {{ preset[2] }}
              </b-dropdown-item-button>
              <b-dropdown-item-button @click="onClickDeletePreset(index)" style="margin-top: 0.25em">
                <b-icon icon="x"></b-icon>
              </b-dropdown-item-button>
            </b-button-toolbar>
          </div>
        </b-dropdown>
      </b-button-group>
      <!--Preset naming modal-->
      <b-modal 
        ref="presetModal"
        id="preset-name-modal"
        title="Save Preset"
        hide-footer
        centered
      >
        <b-form @submit="onSubmitPresetName">
          <b-form-group
            label="Preset name:"
            label-for="preset-name-modal"
          >
            <b-form-input
              id="preset-name-input"
              type="text"
              required
              v-model="presetName"
              placeholder="Enter name"
            >
            </b-form-input>
          </b-form-group>
          <br />
          <b-button type="submit" variant="outline-success">Save</b-button>
        </b-form>
      </b-modal>
    </div>
    <div class="suggestions">
      <b-button id="suggestions-button" pill variant="outline-info" @click="onClickSuggestions">
        Parameter Suggestions
        <b-iconstack>
          <b-icon :class="bulbClass" icon="lightbulb-fill" shift-v="3.5" scale="0.9"></b-icon>
          <b-icon icon="lightbulb" shift-v="3.5" style="color: black" scale="0.9"></b-icon>
        </b-iconstack>
      </b-button>
      <b-popover 
        custom-class="custom-popover"
        variant="info"
        target="suggestions-button"
        placement="right"
        :show.sync="showSuggestions"
        :no-fade="true"
        >
        <!--Render all suggestions, depending on model-->
        <ol class="popover-list">
          <div v-for="suggestion in paramSuggestions" :key="suggestion.id">
            <li v-katex:auto>
              {{ suggestion.text }}
              <katex-element :strict="false" :expression="suggestion.maths" />
            </li>
          </div>
        </ol>
      </b-popover>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    paramSuggestions: Array,
    userPresets: Array,
  },
  data() {
    return {
      presetName: null,
      showSuggestions: false,
      bulbOn: false,
      bulbClass: "bulb-off"
    };
  },
  watch: {
    //Hide suggestions if sim is running
    simRunning: function(isSimRunning) {
      if (isSimRunning) {
        this.hideSuggestions()
      }
    }
  },
  computed: {
    activeUser() {
      return this.$store.state.activeUser;
    },
    simRunning() {
      return this.$store.state.simRunning
    },
    userPresetsUpdate() {
      return this.userPresets
    },
    emptyPresetsSignedIn() {
      return !this.userPresets.length && this.activeUser.isActive
    },
    emptyPresetsSignedOut() {
      return !this.userPresets.length && !this.activeUser.isActive
    }
  },
  methods: {
    onPresetClick(index) {
      this.$emit("selectedPreset", index)
    },
    onClickDeletePreset(index) {
      this.$emit("deletePreset", index)
    },
    onClickDropdown() {
      this.hideSuggestions()
    },
    hideSuggestions() {
      this.showSuggestions = false;
      this.bulbOn = false;
      this.bulbClass = "bulb-off";
    },
    onClickSuggestions() { //Turn bulb on and off after suggestions click
      this.bulbOn = !this.bulbOn
      if (this.bulbOn == false) {
        this.bulbClass = "bulb-off"
      } else {
        this.bulbClass = "bulb-on"
      }
    },
    onSubmitPresetName(event) {
      event.preventDefault();
      this.$emit("presetNameInput", this.presetName); //Trigger event to main route
      this.$refs.presetModal.hide(); //Hide modal following submission
      this.presetName = ""; //Reset name (whether succcessful http req. or not)
    },
    onClickSave() {
      //So button only toggles preset naming modal when signed in
      if (this.activeUser.isActive == true) {
        this.showSuggestions = false //Close suggestions popover
        this.$refs["presetModal"].toggle("#save-button")
      } else { //If not signed in, create alert on main page
        const alertPayload = {
          message: "Sign in or create an account to save model presets! Using presets makes your life easier...",
          variant: "warning"
        }
        this.$emit("showPageAlert", alertPayload)
      }
    },
  },
};
</script>

<style scoped>
.preset-buttons {
  display: flex;
  flex-direction: column;
  position: relative;
  padding-top: 2.2em;
}
.preset-button-bar {
  padding-left: 0.5em;
  padding-right: 0.5em;
}
.popover-list {
  margin-bottom: -0.2em;
}
.custom-popover {
  max-width: 500px;
  z-index: 1;
}
.bulb-on {
  color: rgb(255, 174, 0);
}
.bulb-off {
  color: rgb(255, 255, 255);
}
#suggestions-button {
  float: right;
  margin-top: 2.3em;
  margin-right: 0.5em;
}
</style>
