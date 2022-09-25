<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Test Settings</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="start_testing('validation')">
            START TESTING ON VALIDATION SET
          </v-btn>
        </div>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="start_testing('test')">
            START TESTING ON TEST SET
          </v-btn>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APIStartTest } from '@/services/test';
export default {
  name: 'TestPad',
  data() {
    return {};
  },
  methods: {
    async start_testing(split) {
      this.$root.startProcessing('The test is going on. Please wait...');
      try {
        const res = await APIStartTest({
          split,
        });
        console.log(res);
        this.$root.finishProcessing();
        this.$root.alert('success', 'Testing succeeded');
      } catch (error) {
        console.log(error);
        this.$root.finishProcessing();
        this.$root.alert('error', 'Testing failed');
      }
    },
  },
};
</script>
