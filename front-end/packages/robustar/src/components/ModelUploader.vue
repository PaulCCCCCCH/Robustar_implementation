<template>
  <v-dialog v-model="dialog" width="700px" persistent>
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on" outlined color="primary"> Upload New Model </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex justify-space-between">
        <span>Upload New Model</span>
        <v-btn icon @click="dialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-form ref="form" lazy-validation class="pa-4">
        <div class="d-flex justify-space-between">
          <v-text-field v-model="nickname" :rules="[rules.required]" :loading="isSubmitting" label="Nickname" hint=""
            outlined clearable dense class="mr-4" data-test="model-upload-nickname"></v-text-field>
          <v-select v-if="predefined" v-model="className" :rules="[rules.required]" :loading="isSubmitting"
            :items="modelClasses" label="Class Name" hint="" outlined @change="addModelClassAsTag"></v-select>
          <v-text-field v-else v-model="className" :rules="[rules.required]" :loading="isSubmitting" label="Class Name"
            hint="" outlined clearable dense data-test="model-upload-classname"></v-text-field>
        </div>
        <v-combobox v-model="tags" :loading="isSubmitting" label="Tags" multiple chips clearable dense small-chips
          outlined></v-combobox>
        <v-textarea v-model="description" :loading="isSubmitting" rows="1" label="Description" hint="" auto-grow outlined
          clearable dense></v-textarea>
        <v-checkbox v-model="predefined" label="use predefined" dense class="d-inline-block mr-8"></v-checkbox>
        <v-checkbox v-if="predefined" v-model="pretrained" label="is model pretrained" dense
          class="d-inline-block"></v-checkbox>
        <div v-if="!predefined">
          <v-file-input v-model="weightFile" :loading="isSubmitting" prepend-icon="mdi-file-outline" chips clearable dense
            filled show-size label="Weight File (optional)" hint="choose file"></v-file-input>
          <v-file-input v-model="codeFile" :rules="[rules.required]" :loading="isSubmitting"
            @change="handleCodeFileUpload" prepend-icon="mdi-file-outline" chips clearable dense filled show-size
            label="Code File" hint="choose file" data-test="model-upload-codefile"></v-file-input>
          <v-textarea v-model="code" :rules="[rules.required]" :loading="isSubmitting" prepend-icon="mdi-xml" label="Code"
            hint="The final code uploaded will be based on the content in this code editor." rows="5" filled clearable
            dense style="font-family: monospace"></v-textarea>
        </div>
      </v-form>

      <v-divider></v-divider>

      <v-card-actions class="d-flex flex-column align-start py-8">
        <div>
          <v-btn :loading="isSubmitting" depressed color="primary" class="mr-4" @click="submit"
            data-test="model-upload-submit-button">
            Submit
          </v-btn>
          <v-btn :loading="isSubmitting" depressed @click="reset"> Reset </v-btn>
        </div>
        <div v-if="status">
          <div class="mb-2 mt-4">
            Status: <span class="orange--text">validating</span><span class="green--text">success</span><span
              class="red--text">fail</span>
          </div>
          <div>Feedback</div>
          <code class="d-block overflow-auto pa-3" style="max-height: 200px">print("hello world")
                  </code>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { APIUploadModel, APIGetPredefinedModels } from '@/services/model';

export default {
  name: 'ModelUploader',
  data() {
    return {
      dialog: false,
      predefined: false,
      pretrained: false,
      isSubmitting: false,
      nickname: '',
      className: '',
      modelClasses: [
        'resnet-18',
        'resnet-34',
        'resnet-50',
        'resnet-101',
        'resnet-152',
        'mobilenet-v2',
        'resnet-18-32x32',
        'alexnet',
      ],
      tags: [],
      description: '',
      weightFile: null,
      codeFile: null,
      code: '',
      rules: {
        required: (value) =>
          (value && typeof value === 'string' && !!value.trim()) ||
          (value && value instanceof File) ||
          'Required.',
      },
      status: '',
      feedback: '',
    };
  },
  async mounted() {
    try {
      this.modelClasses = (await APIGetPredefinedModels())?.data?.data ?? [];
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    handleCodeFileUpload(file) {
      if (!file || !file instanceof File) {
        this.code = '';
        return;
      }
      const reader = new FileReader();
      reader.readAsText(file);
      reader.onloadstart = () => {
        this.$root.startProcessing('The file is being read. Please wait...');
      };
      reader.onload = () => {
        this.code = reader.result;
        this.$root.finishProcessing();
      };
      reader.onerror = () => {
        this.$root.finishProcessing();
        this.$root.alert('error', 'Failed to read file');
      };
    },
    addModelClassAsTag() {
      if (this.predefined && this.className && !this.tags.includes(this.className)) {
        this.tags.push("predefined-"+this.className);
      }
    },
    async submit() {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true;
        try {
          await APIUploadModel(
            {
              class_name: this.className,
              nickname: this.nickname,
              description: this.description,
              tags: this.tags,
              predefined: this.predefined ? '1' : '0',
              pretrained: this.pretrained ? '1' : '0',
            },
            this.code,
            this.weightFile
          );
          this.reset();
          this.$root.alert('success', 'Model uploading succeeded');
          this.$emit('upload');
          this.dialog = false;
        } catch (error) {
          this.$root.alert('error', error.response?.data?.detail || 'Server error. Check console.');
        } finally {
          this.isSubmitting = false;
        }
      }
    },
    reset() {
      this.$refs.form.reset();
      this.status = '';
      this.feedback = '';
      this.predefined = false;
      this.pretrained = false;
      this.nickname = '';
      this.className = '';
      this.tags.length = 0;
      this.description = '';
      this.weightFile = null;
      this.code = '';
    },
  },
};
</script>
