<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Influence Calculation</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form v-model="valid" ref="form" lazy-validation>
        <div class="text-h5 mb-8">settings</div>
        <!-- Set start index of test samples per class for which we calculate influence-->
        <v-text-field
          v-model="configs.test_sample_start_idx"
          :rules="startIdxRules"
          class="mb-4"
          label="Start index of test samples"
          outlined
          clearable
          type="number"
          min="0"
          hint="A value of 0 means the beginning of test samples"
          required
        ></v-text-field>
        <!-- Set end index of test samples per class for which we calculate influence-->
        <v-text-field
          v-model="configs.test_sample_end_idx"
          :rules="endIdxRules"
          class="mb-4"
          label="End index of test samples"
          outlined
          clearable
          type="number"
          min="-1"
          hint="A value of -1 means the end of test samples"
          required
        ></v-text-field>
        <!-- Set r_averaging -->
        <v-text-field
          v-model="configs.r_averaging"
          label="r_averaging (integer)"
          outlined
          clearable
          type="number"
          hint="Number of iterations of which to take the avg.
            of the h_estimate calculation; recursion_depth = len(train_data) / r."
          required
        ></v-text-field>

        <v-divider class="mt-4 mb-8"></v-divider>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="start_calculation">
            START CALCULATION
          </v-btn>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APICalculateInfluence } from '@/services/predict';
export default {
  name: 'InfluencePad',
  data() {
    return {
      valid: false, // is input valid or not
      startIdxRules: [
        (v) => (!v && v !== 0 ? 'Start index is required' : true),
        (v) => v >= 0 || 'start index should be a non-negative value',
      ],
      endIdxRules: [
        (v) => (!v && v !== 0 ? 'End index is required' : true),
        (v) => v >= -1 || 'end index should be greater than or equal to -1',
        (v) =>
          v >= Number(this.configs.test_sample_start_idx) ||
          Number(v) === -1 ||
          'end index should be greater than start index or equal to -1',
      ],
      // influence calculation settings
      configs: {
        test_sample_start_idx: 0,
        test_sample_end_idx: 9,
        r_averaging: 1,
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      const { startIdx, endIdx } = vm.$route.params;
      if (startIdx) {
        vm.configs.test_sample_start_idx = startIdx;
      }
      if (endIdx) {
        vm.configs.test_sample_end_idx = endIdx;
      }
    });
  },
  methods: {
    async start_calculation() {
      if (!this.$refs.form.validate()) {
        return;
      }
      this.$root.startProcessing('The influence is being calculated. Please wait...');
      try {
        const res = await APICalculateInfluence({
          configs: this.configs,
        });
        console.log(res);
        this.$root.finishProcessing();
        this.$root.alert('success', 'Influence calculation succeeded');
      } catch (error) {
        console.log(error);
        alert('Server error. Check console.');
        this.$root.finishProcessing();
        this.$root.alert('error', 'Influence calculation failed');
      }
    },
  },
};
</script>
