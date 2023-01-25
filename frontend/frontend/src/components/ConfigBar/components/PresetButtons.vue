<!--eslint-disable-->
<template>
  <div class="preset-buttons" style="display: flex; flex-direction: column">
    <div class="preset-save-list">
      <b-button-group style="padding: 2em 0.5em">
        <b-button class="btn-success" v-b-modal.preset-name-modal @click="showPresetModal=true">
          Save <b-icon icon="box-arrow-in-down" font-scale="1.4" shift-v="1.5"></b-icon>
        </b-button>
        <b-dropdown dropright variant="info" no-caret @show="onClickDropdown">
          <template #button-content>
            My Presets <b-icon icon="justify" font-scale="1.5" style="margin-left: 4em"></b-icon>
          </template>
          <div>
            
          </div>
        </b-dropdown>
      </b-button-group>
      <!--Preset naming modal-->
      <b-modal 
        ref="presetModal"
        id="preset-name-modal"
        title="Save Preset"
        hide-footer
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
      <b-button id="suggestions-button" style="float: right; padding-top: 2em" @click="onClickSuggestions">
        Suggestions <b-icon :icon="bulbIcon" shift-v="1.5"></b-icon>
      </b-button>
      <b-popover target="suggestions-button" placement="right" :show.sync="showSuggestions">
        <!--Render all suggestions, depending on model-->
        <b-list-group v-for="suggestion in paramSuggestions" :key="suggestion.id" flush>
          <b-list-group-item>{{ suggestion.content }}</b-list-group-item>
        </b-list-group>
      </b-popover>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  props: {
    paramSuggestions: Array,
  },
  data() {
    return {
      presetName: "",
      showPresetModal: true,
      showSuggestions: false,
      bulbOn: false,
      bulbIcon: "lightbulb-fill",
    };
  },
  methods: {
    onClickDropdown() {
      this.showSuggestions = false;
      this.bulbOn = false;
      this.bulbIcon = "lightbulb-fill";
    },
    onClickSuggestions() { //Turn bulb on and off after suggestions click
      this.bulbOn = !this.bulbOn
      if (this.bulbOn == false) {
        this.bulbIcon = "lightbulb-fill";
      } else {
        this.bulbIcon = "lightbulb";
      }
    },
    onSubmitPresetName(event) {
      event.preventDefault();
      this.$emit("presetNameInput", this.presetName); //Trigger event to main route
      this.$refs.presetModal.hide(); //Hide modal following submission
      this.presetName = ""; //Reset name (whether succcessful http req. or not)
    },
  },
};
</script>

