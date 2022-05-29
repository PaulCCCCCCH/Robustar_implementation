<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Auto Annotation</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form>
        <!-- <v-select
          v-model="configs.split"
          :items="[
            { text: 'train', value: 'train' },
            { text: 'test', value: 'test' },
            { text: 'validation', value: 'validation' },
          ]"
          label="Which dataset do we annotate?"
          outlined
        ></v-select>
        -->
        <v-text-field
          v-model="configs.num_to_gen"
          label="Number of samples to annotate"
          outlined
          clearable
          type="number"
          hint="0 means generate for all samples"
          data-test="auto-annotate-input-sample-per-class"
        ></v-text-field>

        <div class="d-flex flex-column align-center my-4">
          <v-btn
            depressed
            color="primary"
            class="mx-auto"
            @click="startAutoAnnotate()"
            data-test="auto-annotate-pad-start-auto-annotation"
          >
            START AUTO ANNOTATION
          </v-btn>
          <div style="">Warning: This will overwrite previous annotations!</div>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APIStartAutoAnnotate } from '@/services/edit';
export default {
  name: 'AutoAnnotatePad',
  data() {
    return {
      configs: {
        num_to_gen: 0,
        split: 'train',
      },
    };
  },
  methods: {
    annotateSuccess(res) {
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('success', 'Auto annotation started');
    },
    annotateFailed(res) {
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('error', 'Auto annotation failed to start');
    },
    startAutoAnnotate() {
      this.$root.startProcessing('Starting annotation... Please wait');
      APIStartAutoAnnotate(
        this.configs.split,
        this.configs,
        this.annotateSuccess,
        this.annotateFailed
      );
    },
  },
};
</script>
