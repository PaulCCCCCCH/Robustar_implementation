<template>
  <v-dialog v-model="dialog" width="700px" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on"> Upload New Model </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <span>Upload New Model</span>
        <v-btn icon @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-form ref="form" lazy-validation class="pa-4">
        <v-text-field
          v-model="name"
          :rules="[rules.required]"
          :loading="isSubmitting"
          label="Name"
          hint=""
          outlined
          clearable
          dense
        ></v-text-field>
        <v-textarea
          v-model="description"
          :loading="isSubmitting"
          rows="1"
          label="Description"
          hint=""
          auto-grow
          outlined
          clearable
          dense
        ></v-textarea>
        <v-checkbox v-model="usePredefined" label="use predefined" dense></v-checkbox>
        <div v-if="!usePredefined">
          <v-file-input
            v-model="weightFile"
            :loading="isSubmitting"
            prepend-icon="mdi-file-outline"
            chips
            clearable
            dense
            filled
            show-size
            label="Weight File (optional)"
            hint="choose file"
          ></v-file-input>
          <v-file-input
            v-model="codeFile"
            :rules="[rules.required]"
            :loading="isSubmitting"
            @change="handleCodeFileUpload"
            prepend-icon="mdi-file-outline"
            chips
            clearable
            dense
            filled
            show-size
            label="Code File"
            hint="choose file"
          ></v-file-input>
          <v-textarea
            v-model="code"
            :rules="[rules.required]"
            :loading="isSubmitting"
            prepend-icon="mdi-xml"
            label="Code"
            hint="The final code uploaded will be based on the content in this code editor."
            rows="5"
            filled
            clearable
            dense
            style="font-family: monospace"
          ></v-textarea>
        </div>
        <div v-else>
          <v-text-field
            v-model="numClasses"
            :loading="isSubmitting"
            label="num_classes"
            type="number"
            min="0"
            hint=""
            outlined
            clearable
            dense
          ></v-text-field>
          <v-select
            v-model="architecture"
            :items="['a', 'b', 'c']"
            :loading="isSubmitting"
            label="Model Architecture"
            hint=""
            outlined
            dense
          ></v-select>
        </div>
      </v-form>

      <v-divider></v-divider>

      <v-card-actions class="d-flex flex-column align-start py-8">
        <div>
          <v-btn :loading="isSubmitting" depressed color="primary" class="mr-4" @click="submit">
            Submit
          </v-btn>
          <v-btn :loading="isSubmitting" depressed @click="reset"> Reset </v-btn>
        </div>
        <div v-if="status">
          <div class="mb-2 mt-4">
            Status: <span class="orange--text">validating</span
            ><span class="green--text">success</span><span class="red--text">fail</span>
          </div>
          <div>Feedback</div>
          <code class="d-block overflow-auto pa-3" style="max-height: 200px"
            >print("hello world")
          </code>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ModelUploader',
  data() {
    return {
      dialog: false,
      usePredefined: false,
      isSubmitting: false,
      name: '',
      description: '',
      weightFile: null,
      codeFile: null,
      code: '',
      numClasses: 0,
      architecture: 'a',
      rules: {
        required: (value) => ((value && typeof value === 'string' && !!value.trim()) || (value && value instanceof File)) || 'Required.',
      },
      status: '',
      feedback: '',
    };
  },
  methods: {
    handleCodeFileUpload(file) {
      if (!file || !file instanceof File) {
        this.code = ''
        return
      } 
      const reader = new FileReader()
      reader.readAsText(file)
      reader.onloadstart = () => {
        this.$root.startProcessing('The file is being read. Please wait...');
      }
      reader.onload = () => {
        this.code = reader.result
        this.$root.finishProcessing();
      }
      reader.onerror = () => {
        this.$root.finishProcessing();
        this.$root.alert('error', 'Failed to read file');
      }
    },
    submit() {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true;
        setTimeout(() => {
          this.isSubmitting = false;
          // this.reset();
          this.status = 'sdfsd';
        }, 3000);
      }
    },
    reset() {
      this.$refs.form.reset();
      this.status = '';
      this.feedback = '';
      this.usePredefined = false;
      this.name = '';
      this.description = '';
      this.weightFile = null;
      this.code = '';
      this.architecture = 'a';
    },
  },
};
</script>
