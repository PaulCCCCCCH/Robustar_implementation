<template>
  <div class="d-flex flex-column align-center">
    <v-card class="mt-8 mb-4 pa-2" width="1300">
      <v-card-title class="d-flex justify-space-between mb-2">
        <span>Current Model: {{ currentModel.nickname }}</span>
        <v-btn outlined color="primary" @click="trainModel">Train</v-btn>
      </v-card-title>
      <v-card-text>
        <div>
          <span>
            <span class="font-weight-medium">Tag: </span>
            {{ currentModel.tag }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Epoch: </span>
            {{ currentModel.epoch }}
          </span>
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
        <div class="my-2">
          <span class="mr-8">
            <span class="font-weight-medium">Created time: </span>
            {{ currentModel.create_time }}
          </span>
          <span class="mx-8">
            <span class="font-weight-medium">Last trained: </span>
            {{ currentModel.last_trained }}
          </span>
        </div>
        <div class="my-2 mb-4">
          <span class="font-weight-medium">Description: </span>{{ currentModel.description }}
        </div>
        <v-textarea
          v-model="currentModel.architecture"
          rows="3"
          label="Architecture"
          hint=""
          outlined
          clearable
          dense
          disabled
        ></v-textarea>
      </v-card-text>
    </v-card>
    <v-card class="pa-2 mb-4" width="1300">
      <v-card-title>
        All models <v-spacer></v-spacer>
        <v-text-field
          v-model="searchText"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
          dense
          class="mr-8"
        ></v-text-field>
        <ModelUploader @upload="getModelList" />
      </v-card-title>
      <v-data-table
        v-model="selectedModels"
        :headers="headers"
        :items="modelList"
        :search="searchText"
        :loading="isLoading"
        loading-text="Loading... Please wait"
        item-key="nickname"
        :item-class="(item) => (item.nickname === currentModel.nickname ? 'blue lighten-5' : '')"
        show-select
        width="1000"
      >
        <template v-slot:top>
          <!-- <v-toolbar flat> -->
          <v-dialog v-model="dialogEdit" max-width="800px" persistent>
            <v-card>
              <v-card-title>
                <span class="text-h5">Edit model</span>
              </v-card-title>
              <v-card-text>
                <div class="d-flex justify-space-between">
                  <span style="width: 400px"
                    ><v-text-field
                      v-model="editingModel.nickname"
                      :loading="isSubmitting"
                      label="Model Name"
                      hint=""
                      outlined
                      clearable
                      dense
                    ></v-text-field
                  ></span>
                  <span>
                    <v-btn class="ml-4" outlined color="primary" @click="setCurrentModel"
                      >Set As Current Model</v-btn
                    ></span
                  >
                </div>
                <v-divider class="mb-4"></v-divider>
                <div>
                  <div style="width: 100px; display: inline-block">
                    <v-text-field
                      v-model="editingModel.tag"
                      :loading="isSubmitting"
                      label="Tag"
                      hint=""
                      outlined
                      clearable
                      dense
                    ></v-text-field>
                  </div>
                  <span class="mx-8">
                    <span class="font-weight-medium">Epoch: </span>
                    {{ editingModel.epoch }}
                  </span>
                  <span>
                    <span class="font-weight-medium">Test Accuracy: </span>
                    {{ editingModel.test_accuracy }}
                  </span>
                  <span class="mx-8">
                    <span class="font-weight-medium">Train Accuracy: </span>
                    {{ editingModel.train_accuracy }}
                  </span>
                  <span>
                    <span class="font-weight-medium">Validation Accuracy: </span>
                    {{ editingModel.val_accuracy }}
                  </span>
                </div>
                <div class="mb-8">
                  <span class="mr-8">
                    <span class="font-weight-medium">Created time: </span>
                    {{ editingModel.create_time }}
                  </span>
                  <span>
                    <span class="font-weight-medium">Last trained: </span>
                    {{ editingModel.last_trained }}
                  </span>
                </div>
                <v-textarea
                  v-model="editingModel.description"
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
                  v-model="editingModel.architecture"
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
                  <v-btn
                    :loading="isSubmitting"
                    depressed
                    color="warning"
                    @click="dialogEdit = false"
                    class="mr-4"
                  >
                    Cancel
                  </v-btn>
                  <v-btn :loading="isSubmitting" depressed color="success" @click="saveModelChanges"
                    >Save Changes</v-btn
                  >
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Delete model</span>
              </v-card-title>
              <v-card-text
                >Are you sure you want to delete the model {{ deletingModelName }}?</v-card-text
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="dialogDelete = false"> Cancel </v-btn>
                <v-btn color="error darken-1" text @click="deleteModel"> Confirm </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- </v-toolbar> -->
        </template>
        <template v-slot:item.actions="{ item }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon small @click="setCurrentModel(item)" class="mr-2" v-bind="attrs" v-on="on">
                mdi-check-circle-outline
              </v-icon>
            </template>
            <span>Set as current model</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                small
                @click="
                  editingModel = { ...item };
                  dialogEdit = true;
                "
                class="mr-2"
                v-bind="attrs"
                v-on="on"
              >
                mdi-pencil
              </v-icon>
            </template>
            <span>Edit model</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon small class="mr-2" @click="duplicateModel(item)" v-bind="attrs" v-on="on">
                mdi-content-copy
              </v-icon>
            </template>
            <span>Duplicate model</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                small
                @click="
                  deletingModelName = item.nickname;
                  dialogDelete = true;
                "
                v-bind="attrs"
                v-on="on"
              >
                mdi-delete
              </v-icon>
            </template>
            <span>Delete model</span>
          </v-tooltip>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import {
  APIGetCurrentModel,
  APISetCurrentModel,
  APIDeleteModel,
  APIGetAllModels,
  APIDuplicateModel,
  APIUpdateModel,
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
      isSubmitting: false,
      isLoading: false,
      currentModel: { ...initialModel },
      editingModel: { ...initialModel },
      deletingModelName: '',
      modelList: [],
      selectedModels: [],
      searchText: '',
      dialogEdit: false,
      dialogDelete: false,
      headers: [
        {
          text: 'nickname',
          value: 'nickname',
        },
        { text: 'Tag', value: 'tag' },
        { text: 'Created Time', value: 'create_time' },
        { text: 'Last Trained', value: 'last_trained' },
        { text: 'Epoch', value: 'epoch', filterable: false },
        { text: 'Test Accuracy', value: 'test_accuracy', filterable: false },
        { text: 'Train Accuracy', value: 'train_accuracy', filterable: false },
        { text: 'Validation Accuracy', value: 'validation_accuracy', filterable: false },
        { text: 'Description', value: 'description' },
        { text: 'Actions', value: 'actions', sortable: false, filterable: false },
      ],
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
    async setCurrentModel(model) {
      try {
        const response = await APISetCurrentModel(
          model ? model.nickname : this.editingModel.nickname
        );
        this.currentModel = model ? { ...model } : { ...this.editingModel };
        this.$root.$emit('sync-current-model')
      } catch (error) {
        console.error('Error setting current model:', error);
      }
    },
    async getModelList() {
      try {
        this.isLoading = true;
        this.modelList = (await APIGetAllModels())?.data?.data;
      } catch (error) {
        console.error('Error fetching model list:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async deleteModel() {
      this.isSubmitting = true;
      try {
        await APIDeleteModel(this.deletingModelName);
        this.getCurrentModel();
        this.getModelList();
        this.dialogDelete = false;
      } catch (error) {
        console.error('Error deleting model:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
    async duplicateModel(item) {
      this.isSubmitting = true;
      try {
        await APIDuplicateModel(item.nickname);
        this.getModelList();
      } catch (error) {
        console.error('Error duplicating model:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
    async saveModelChanges() {
      this.isSubmitting = true;
      try {
        await APIUpdateModel(this.editingModel.nickname, this.editingModel);
        this.getModelList();
        this.dialogEdit = false;
      } catch (error) {
        console.error('Error saving model changes:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
