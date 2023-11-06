<template>
  <div class="d-flex flex-column align-center">
    <v-card class="mt-8 mb-4 pa-2" width="1000">
      <v-card-title class="d-flex justify-space-between mb-2">
        <span>Current Model: {{ $root.currentModel }}</span>
        <v-btn depressed color="primary" @click="trainModel">Train</v-btn>
      </v-card-title>
      <v-card-text>
        <div class="d-flex justify-space-between" style="width: 700px">
          <span>
            <span class="font-weight-medium">Created time: </span>
            11/19/1999 16:00
          </span>
          <span>
            <span class="font-weight-medium">Last trained: </span>
            11/19/1999 16:00
          </span>
          <span>
            <span class="font-weight-medium">Accuracies: </span>
            50%
          </span>
          <span>
            <span class="font-weight-medium">Epoch: </span>
            100
          </span>
        </div>
        <div class="my-2">
          <span class="font-weight-medium">Description: </span>
        </div>
        <div>
          <span class="font-weight-medium">Architecture: </span>
        </div>
      </v-card-text>
    </v-card>

    <v-card class="pa-2" width="1000">
      <v-card-title class="mb-2">All Models</v-card-title>
      <v-card-text>
        <div class="d-flex justify-space-between">
          <span style="width: 400px"
            ><v-select
              v-model="viewingModel"
              :loading="isSubmitting"
              :items="modelList"
              label="Model"
              hint=""
              outlined
              dense
            ></v-select
          ></span>
          <span
            ><ModelUploader />
            <v-btn class="ml-4" depressed color="primary" @click="setCurrentModel"
              >Set As Current Model</v-btn
            ></span
          >
        </div>
        <v-divider class="mb-4"></v-divider>
        <div class="d-flex justify-space-between">
          <span>
            <span class="font-weight-medium">Created time: </span>
            {{ viewingModel.create_time }}
          </span>
          <div style="width: 200px">
            <v-text-field
              :loading="isSubmitting"
              label="Last trained"
              hint=""
              outlined
              clearable
              dense
            ></v-text-field>
          </div>
          <div style="width: 120px">
            <v-text-field
              :loading="isSubmitting"
              label="Accuracies"
              hint=""
              outlined
              clearable
              dense
            ></v-text-field>
          </div>
          <div style="width: 100px">
            <v-text-field
              v-model="viewingModel.epoch"
              :loading="isSubmitting"
              label="Epoch"
              hint=""
              outlined
              clearable
              dense
              type="number"
            ></v-text-field>
          </div>
        </div>
        <v-textarea
          v-model="viewingModel.description"
          :loading="isSubmitting"
          rows="1"
          label="Description"
          hint=""
          auto-grow
          outlined
          clearable
          dense
        ></v-textarea>
        <v-textarea
          v-model="viewingModel.architecture"
          :loading="isSubmitting"
          rows="7"
          label="Architecture"
          hint=""
          outlined
          clearable
          dense
        ></v-textarea>
        <v-divider class="mb-4"></v-divider>
        <div class="d-flex justify-end">
          <v-btn :loading="isSubmitting" depressed color="error" @click="deleteModel">Delete</v-btn>
          <v-btn
            :loading="isSubmitting"
            depressed
            color="warning"
            class="mx-4"
            @click="duplicateModel"
            >Duplicate</v-btn
          >
          <v-btn :loading="isSubmitting" depressed color="success" @click="saveModelChanges"
            >Save Changes</v-btn
          >
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import {
  APIGetCurrentModel,
  APISetCurrentModel,
  APIDeleteModel,
  APIUploadModel,
  APIGetAllModels,
} from '@/services/model/';
import ModelUploader from '@/components/ModelUploader';

export default {
  name: 'TrainModel',
  components: {
    ModelUploader,
  },
  data() {
    return {
      isSubmitting: false,
      viewingModel: {
        architecture: '',
        class_name: '',
        create_time: '',
        description: '',
        epoch: 0,
        nickname: '',
      },
      modelList: [],
      epoch: 0,
    };
  },
  async mounted() {
    try {
      // console.log(await APIGetCurrentModel());
      const response = (await APIGetAllModels())?.data?.data;
      this.modelList = response.map((item) => ({ text: item.nickname, value: item }));
      this.viewingModel = this.modelList.length ? this.modelList[0].value : null;
    } catch (error) {
      console.error('Error fetching model list:', error);
    }
  },
  methods: {
    trainModel() {
      this.$router.push({ name: 'TrainPad' });
    },
    async setCurrentModel() {
      try {
        const response = await APISetCurrentModel(this.viewingModel.nickname);
        this.$root.currentModel = this.viewingModel;
      } catch (error) {
        console.error('Error setting current model:', error);
      }
    },
    async deleteModel() {
      this.isSubmitting = true;
      try {
        await APIDeleteModel(this.viewingModel.nickname);
        this.modelList.splice(this.modelList.indexOf(this.viewingModel), 1);
        this.viewingModel = this.modelList[0] || null;
      } catch (error) {
        console.error('Error deleting model:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
    async duplicateModel() {
      this.isSubmitting = true;
      try {
        // TODO: Replace with actual API call
        this.viewingModel = this.viewingModel + '-copy';
        this.modelList.push(this.viewingModel);
      } catch (error) {
        console.error('Error duplicating model:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
    async saveModelChanges() {
      this.isSubmitting = true;
      try {
        // TODO: Replace with actual API call
      } catch (error) {
        console.error('Error saving model changes:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
