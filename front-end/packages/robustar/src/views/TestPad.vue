<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Test Settings</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="start_testing('validation')">
            Start Testing on Validation Set
          </v-btn>
        </div>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="start_testing('test')">
            Start Testing on Test Set
          </v-btn>
        </div>
      </v-form>
    </v-sheet>

    <!-- api feedback -->

    <v-overlay :value="sending" opacity="0.7">
      <v-progress-circular indeterminate size="30" class="mr-4"></v-progress-circular>
      <span style="vertical-align: middle"> The test is going on. Please wait... </span>
    </v-overlay>

    <!-- testing succeeded -->
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
      <div class="white--text">Testing succeeded</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="accent" text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>

    <!-- testing failed -->
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
      <div class="white--text">Testing failed</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbarError = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { APIStartTest } from '@/apis/test';
export default {
  name: 'TestPad',
  data() {
    return {
      sending: false,
      snackbar: false,
      snackbarError: false,
    };
  },
  methods: {
    testingSuccess(res) {
      console.log(res);
      this.sending = false;
      this.snackbar = true;
    },
    testingFailed(res) {
      console.log(res);
      this.sending = false;
      this.snackbarError = true;
    },
    start_testing(split) {
      this.sending = true;
      APIStartTest(
        {
          split: split,
        },
        this.testingSuccess,
        this.testingFailed
      );
    },
  },
};
</script>
