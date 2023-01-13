<template>
  <div class="ConfigBarMalthusian">
    <!--Enclose config within card-->
    <b-card class="rounded-0" style="min-width: 25em; position: fixed">
      <template #header>
        <p class="mt-2" style="font-size: 1.5em">Model Parameters</p>
      </template>
      <b-card-body style="min-height: 68vh">
        <label
          for="initialPopRange"
          class="form-label d-flex justify-content-center"
          style="font-size: 1.5em"
          >$N_{0}$
          <b-icon
            icon="info-circle"
            scale="0.7"
            shift-v="-6em"
            variant="info"
            style="margin-left: 0.5em"
          />
        </label>
        <input
          type="range"
          class="form-range"
          min="0"
          max="5"
          step="0.5"
          id="initialPopRange"
          @input="$emit('changeInitialPopulation', $event.target.value)"
        />
        <label
          for="rateRange"
          class="form-label d-flex justify-content-center"
          style="font-size: 1.5em"
          >$r$
          <b-icon
            icon="info-circle"
            scale="0.7"
            shift-v="-6em"
            variant="info"
            style="margin-left: 0.5em"
          />
        </label>
        <input
          type="range"
          class="form-range"
          min="0"
          max="5"
          step="0.5"
          id="rateRange"
          @input="$emit('changeRate', $event.target.value)"
        />
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
export default {
  props: ["rate", "initialPopulation"],
  data() {
    return {};
  },
  methods: {},
};
</script>
