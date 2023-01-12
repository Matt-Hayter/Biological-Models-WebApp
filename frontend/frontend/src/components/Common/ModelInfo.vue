<!-- eslint-disable-->
<template>
  <div class="model-info-button">
    <!--Mount collapse bar to button-->
    <b-button v-b-toggle.collapse-bar variant="outline-info" size="sm" style="padding: 0.3em">
      About this model
      <b-icon icon="chevron-down" font-scale="1"></b-icon>
    </b-button>
    <b-collapse id="collapse-bar">
      <b-card>
        <!--Model-specific buttom content goes here-->
        <slot></slot>
      </b-card>
    </b-collapse>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>
