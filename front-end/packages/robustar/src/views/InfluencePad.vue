<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Influence Calculation</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form>
        <div class="text-h5 mb-4">settings</div>
        <!-- Set num of test samples per class for which we calculate influence-->
        <v-text-field
          v-model="configs.test_sample_num"
          label="Number of test samples for which we calculate influence (integer).
          This number will be multiplied with the number of classes in the dataset"
          outlined
          clearable
          type="number"
          hint="A value of -1 means calculating influence for the entire test set"
        ></v-text-field>

        <br />
        <!-- Set r_averaging -->
        <v-text-field
          v-model="configs.r_averaging"
          label="r_averaging (integer)"
          outlined
          clearable
          type="number"
          hint="Number of iterations of which to take the avg.
            of the h_estimate calculation; recursion_depth = len(train_data) / r."
        ></v-text-field>

        <v-divider class="my-8"></v-divider>
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
      // influence calculation settings
      configs: {
        test_sample_num: 10,
        r_averaging: 1,
      },
    };
  },
  methods: {
    start_calculation() {
      this.$root.startProcessing('The influence is being calculated. Please wait...');
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
        this.$root.finishProcessing();
        this.$root.alert('success', 'Influence calculation succeeded');
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
        this.$root.finishProcessing();
        this.$root.alert('error', 'Influence calculation failed');
      };
      APICalculateInfluence(
        {
          configs: this.configs,
        },
        success,
        failed
      );
    },
  },
};
</script>
