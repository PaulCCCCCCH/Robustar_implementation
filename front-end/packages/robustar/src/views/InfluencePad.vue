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

        <br>
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
            Start calculation
          </v-btn>
        </div>
      </v-form>
    </v-sheet>

    <!-- api feedback -->

    <v-overlay :value="sending" opacity="0.7">
      <v-progress-circular indeterminate size="30" class="mr-4"></v-progress-circular>
      <span style="vertical-align: middle"> calculating influence. Please wait... </span>
    </v-overlay>

    <!-- training succeeded -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbar"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Influence calculation started</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="accent" text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>

    <!-- training failed -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbarError"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Influence calculation failed</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbarError = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { APICalculateInfluence } from '@/apis/predict';
export default {
  name: 'InfluencePad',
  data() {
    return {
      sending: false,
      snackbar: false,
      snackbarError: false,

      // influence calculation settings
      configs: {
        test_sample_num: 10,
        r_averaging: 1
      },
    };
  },
  methods: {
    start_calculation() {
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
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
