<template>
  <div class="d-flex flex-column align-center">
    <v-card class="mt-8 mb-4 pa-2" width="1000">
      <v-card-title class="d-flex justify-space-between mb-2">
        <span>Current Model: {{ currentModel.nickname }}</span>
        <v-btn depressed color="primary" @click="trainModel">Train</v-btn>
      </v-card-title>
      <v-card-text>
        <div>
          <span class="mr-8">
            <span class="font-weight-medium">Tag: </span>
            {{ currentModel.tag }}
          </span>
          <span>
            <span class="font-weight-medium">Created time: </span>
            {{ currentModel.create_time }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Last trained: </span>
            {{ currentModel.last_trained }}
          </span>
          <span>
            <span class="font-weight-medium">Epoch: </span>
            {{ currentModel.epoch }}
          </span>
        </div>
        <div class="my-2">
          <span>
            <span class="font-weight-medium">Test Accuracy: </span>
            {{ currentModel.test_accuracy }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Train Accuracy: </span>
            {{ currentModel.train_accuracy }}
          </span>
          <span>
            <span class="font-weight-medium">Validation Accuracy: </span>
            {{ currentModel.val_accuracy }}
          </span>
        </div>
        <div class="my-2 mb-4">
          <span class="font-weight-medium">Description: </span>{{ currentModel.description }}
        </div>
        <v-textarea
          v-model="currentModel.architecture"
          rows="7"
          label="Architecture"
          hint=""
          outlined
          clearable
          dense
          disabled
        ></v-textarea>
      </v-card-text>
    </v-card>

    <v-card class="pa-2 mb-4" width="1000">
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
        <div>
          <div style="width: 100px; display: inline-block" class="mr-8">
            <v-text-field
              v-model="viewingModel.tag"
              :loading="isSubmitting"
              label="Tag"
              hint=""
              outlined
              clearable
              dense
            ></v-text-field>
          </div>
          <span>
            <span class="font-weight-medium">Created time: </span>
            {{ viewingModel.create_time }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Last trained: </span>
            {{ viewingModel.last_trained }}
          </span>
          <span>
            <span class="font-weight-medium">Epoch: </span>
            {{ viewingModel.epoch }}
          </span>
        </div>
        <div class="mb-8">
          <span>
            <span class="font-weight-medium">Test Accuracy: </span>
            {{ viewingModel.test_accuracy }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Train Accuracy: </span>
            {{ viewingModel.train_accuracy }}
          </span>
          <span>
            <span class="font-weight-medium">Validation Accuracy: </span>
            {{ viewingModel.val_accuracy }}
          </span>
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

const initialModel = {
  architecture: '',
  class_name: '',
  create_time: '',
  last_trained: '',
  description: '',
  epoch: 0,
  nickname: '',
  test_accuracy: '',
  train_accuracy: '',
  val_accuracy: '',
  tag: '',
};

export default {
  name: 'TrainModel',
  components: {
    ModelUploader,
  },
  data() {
    return {
      currentModel: { ...initialModel },
      isSubmitting: false,
      viewingModel: { ...initialModel },
      modelList: [],
      epoch: 0,
    };
  },
  mounted() {
    this.getCurrentModel();
    this.getModelList();
  },
  methods: {
    trainModel() {
      this.$router.push({ name: 'TrainPad' });
    },
    async getCurrentModel() {
      try {
        const response = (await APIGetCurrentModel())?.data?.data;
        this.currentModel = response;
      } catch (error) {
        console.error('Error fetching current model:', error);
      }
    },
    async getModelList() {
      try {
        const response = (await APIGetAllModels())?.data?.data;
        this.modelList = response.map((item) => ({ text: item.nickname, value: item }));
        this.viewingModel = this.modelList.length ? this.modelList[0].value : { ...initialModel };
      } catch (error) {
        console.error('Error fetching model list:', error);
      }
    },
    async setCurrentModel() {
      try {
        const response = await APISetCurrentModel(this.viewingModel.nickname);
        this.currentModel = this.viewingModel;
      } catch (error) {
        console.error('Error setting current model:', error);
      }
    },
    async deleteModel() {
      this.isSubmitting = true;
      try {
        await APIDeleteModel(this.viewingModel.nickname);
        this.getCurrentModel();
        this.getModelList();
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
