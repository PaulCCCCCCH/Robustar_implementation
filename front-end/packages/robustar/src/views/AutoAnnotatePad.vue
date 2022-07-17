<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Auto Annotation</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form v-model="valid" ref="form" lazy-validation>
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
          v-model="configs.start_idx_to_gen"
          :rules="startIdxRules"
          class="mb-4"
          label="Start index of samples to annotate"
          outlined
          clearable
          type="number"
          min="0"
          hint="A value of 0 means the beginning of all samples"
          required
        ></v-text-field>

        <v-text-field
          v-model="configs.end_idx_to_gen"
          :rules="endIdxRules"
          label="End index of samples to annotate"
          outlined
          clearable
          type="number"
          min="-1"
          hint="A value of -1 means the end of all samples"
          required
        ></v-text-field>

        <div class="d-flex flex-column align-center my-4">
          <v-btn
            depressed
            color="primary"
            class="mb-4"
            @click="startAutoAnnotate"
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
      valid: false, // is input valid or not
      startIdxRules: [
        (v) => (!v && v !== 0 ? 'Start index is required' : true),
        (v) => v >= 0 || 'start index should be a non-negative value',
      ],
      endIdxRules: [
        (v) => (!v && v !== 0 ? 'End index is required' : true),
        (v) => v >= -1 || 'end index should be greater than or equal to -1',
        (v) =>
          v >= Number(this.configs.start_idx_to_gen) ||
          Number(v) === -1 ||
          'end index should be greater than start index or equal to -1',
      ],
      configs: {
        start_idx_to_gen: 0,
        end_idx_to_gen: -1,
        split: 'train',
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      const { startIdx, endIdx } = vm.$route.params;
      if (startIdx) {
        vm.configs.start_idx_to_gen = startIdx;
      }
      if (endIdx) {
        vm.configs.end_idx_to_gen = endIdx;
      }
    });
  },
  methods: {
    async startAutoAnnotate() {
      if (!this.$refs.form.validate()) {
        return;
      }
      this.$root.startProcessing('Starting annotation... Please wait');
      try {
        const res = await APIStartAutoAnnotate(this.configs.split, this.configs);
        console.log(res);
        this.$root.finishProcessing();
        this.$root.alert('success', 'Auto annotation started');
      } catch (error) {
        console.log(error);
        this.$root.finishProcessing();
        this.$root.alert('error', 'Auto annotation failed to start');
      }
    },
  },
};
</script>
