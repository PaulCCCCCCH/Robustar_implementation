<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-8">
      <div class="text-h4 text-center font-weight-medium">Influence Calculation</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form v-model="valid" ref="form" lazy-validation>
        <div class="text-h5 mb-8"> Image Index Range </div>
        <!-- Set start index of test samples per class for which we calculate influence-->
        <v-text-field
          v-model="configs.test_start_index"
          :rules="startIdxRules"
          class="mb-4"
          label="Start index of test samples"
          outlined
          clearable
          type="number"
          min="0"
          hint="A value of 0 means the beginning of test samples"
          required
          data-test="influence-pad-start-index-field"
        ></v-text-field>
        <!-- Set end index of test samples per class for which we calculate influence-->
        <v-text-field
          v-model="configs.test_end_index"
          :rules="endIdxRules"
          class="mb-4"
          label="End index of test samples"
          outlined
          clearable
          type="number"
          min="-1"
          hint="A value of -1 means the end of test samples"
          required
          data-test="influence-pad-end-index-field"
        ></v-text-field>

        <v-divider class="mt-4 mb-8"></v-divider>
        <div class="text-h5 mb-8"> Algorithm Parameters </div>
        <!-- Set r_averaging -->
        <v-text-field
          v-model="configs.r_averaging"
          label="r_averaging (integer)"
          outlined
          clearable
          type="number"
          hint="Run the algorithm r times and take the average. Increasing this 
          results in better accuracy and longer training time."
          required
        ></v-text-field>
        <v-text-field
          v-model="configs.recursion_depth"
          label="recursion_depth (integer)"
          outlined
          clearable
          type="number"
          hint="Number of batches we sample from the training data; 
          Increasing this results in better accuracy and longer training time.
          It is recommended to have recursion_depth * r = size of training data"
          required
        ></v-text-field>
        <v-text-field
          v-model="configs.scale"
          label="scale"
          outlined
          clearable
          type="number"
          hint="The scale of the influence value. Tune this number for the dataset
          and model you use if you see NaN values in the results."
          required
        ></v-text-field>

        <v-divider class="mt-4 mb-8"></v-divider>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="startCalculation">
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
          v >= Number(this.configs.test_start_index) ||
          Number(v) === -1 ||
          'end index should be greater than start index or equal to -1',
      ],
      // influence calculation settings
      configs: {
        test_start_index: 0,
        test_end_index: 9,
        r_averaging: 1,
        recursion_depth: 1,
        scale: 5000,
        damp: 0.001,
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      const { startIdx, endIdx } = vm.$route.params;
      if (startIdx) {
        vm.configs.test_start_index = startIdx;
      }
      if (endIdx) {
        vm.configs.test_end_index = endIdx;
      }
    });
  },
  methods: {
    async startCalculation() {
      if (!this.$refs.form.validate()) {
        return;
      }
      this.$root.startProcessing('The influence is being calculated. Please wait...');
      try {
        const res = await APICalculateInfluence({
          configs: this.configs,
        });
        this.$root.finishProcessing();
        this.$root.alert('success', 'Influence calculation succeeded');
      } catch (error) {
        this.$root.finishProcessing();
        console.log(error);
        this.$root.alert('error', error.response?.data?.detail || 'Server error. Check console.');
      }
    },
  },
};
</script>
