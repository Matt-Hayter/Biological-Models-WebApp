<!--eslint-disable-->
<template>
  <div class="preset-buttons" style="display: flex; flex-direction: column">
    <div class="preset-save-list">
      <b-button-group style="padding: 2em 0.5em">
        <b-button class="btn-success">
          Save <b-icon icon="box-arrow-in-down" font-scale="1.4" shift-v="1.5"></b-icon>
        </b-button>
        <b-dropdown dropright variant="info" no-caret>
          <template #button-content>
            My Presets <b-icon icon="justify" font-scale="1.5" style="margin-left: 4em"></b-icon>
          </template>
        </b-dropdown>
      </b-button-group>
    </div>
    <div class="suggestions">
      <b-button id="suggestions-button" @click="showSuggestions = !showSuggestions" style="float: right; padding-top: 2em">
        Suggestions
      </b-button>
      <b-popover target="suggestions-button" placement="right" :show.sync="showSuggestions">
        <b-list-group>
          <b-list-group-item>{{ paramSuggestions[0] }}</b-list-group-item>
          <b-list-group-item>{{ paramSuggestions[1] }}</b-list-group-item>
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
      showSuggestions: false,
    };
  },
};
</script>

