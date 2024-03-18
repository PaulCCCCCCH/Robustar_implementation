<template>
  <div class="d-flex flex-column align-center">
    <v-card class="mt-8 mb-4 pa-2" width="1300">
      <v-card-title class="d-flex justify-space-between mb-2">
        <span data-test="train-model-current-model">Current Model: {{ currentModel.nickname }}</span>
        <v-btn outlined color="primary" @click="trainModel" data-test="train-model-train-model-button">Train</v-btn>
      </v-card-title>
      <v-card-text>
        <div>
          <span>
            <span class="font-weight-medium">Tag: </span>
            {{ currentModel.tag.join(', ') }}
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
            <span class="font-weight-medium" data-test="train-model-current-model-create-time">Created time: </span>
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
        <v-textarea v-model="currentModel.architecture" rows="3" label="Architecture" hint=""
          data-test="train-model-current-model-architecture" outlined clearable dense disabled></v-textarea>
      </v-card-text>
    </v-card>
    <v-card class="pa-2 mb-4" width="1300">
      <v-card-title>
        All models <v-spacer></v-spacer>
        <div v-if="selectedTags.length > 0" class="d-flex align-center mr-4">
          <v-chip v-for="tag in selectedTags" :key="tag" close @click:close="filterByTag(tag)" class="mr-2">
            {{ tag }}
          </v-chip>
          <v-btn color="primary" outlined small @click="clearSelectedTags">
            Clear Tags
          </v-btn>
        </div>
        <v-text-field v-model="searchText" append-icon="mdi-magnify" label="Search" single-line hide-details dense
          class="mr-8"></v-text-field>
        <ModelUploader @upload="getModelList" />
      </v-card-title>
      <v-data-table v-model="selectedModels" :headers="headers" :items="filteredModelList" :search="searchText"
        :loading="isLoading" loading-text="Loading... Please wait" item-key="id" show-select width="1000">
        <template v-slot:item.tag="{ item }">
          <div>
            <v-chip v-for="tag in item.tags" :key="tag" small class="mr-1 mb-1" text-color="black"
              @click="filterByTag(tag)">
              {{ tag }}
            </v-chip>
            <span v-if="!item.tags || item.tags.length === 0">-</span>
          </div>
        </template>
        <template v-slot:top>
          <!-- <v-toolbar flat> -->
          <v-dialog v-model="dialogEdit" max-width="800px" persistent>
            <v-card>
              <v-card-title>
                <span class="text-h5">Edit model</span>
              </v-card-title>
              <v-card-text>
                <div class="d-flex justify-space-between">
                  <span style="width: 400px"><v-text-field v-model="editingModel.nickname" :loading="isSubmitting"
                      label="Model Name" hint="" outlined clearable dense
                      data-test="train-model-edit-model-name"></v-text-field></span>
                  <span>
                    <v-btn class="ml-4" outlined color="primary" @click="setCurrentModel"
                      data-test="train-model-set-current-model">Set As Current Model</v-btn></span>
                </div>
                <v-divider class="mb-4"></v-divider>
                <div>
                  <div style="width: 200px; display: inline-block">
                    <v-combobox v-model="editingModel.tags" :loading="isSubmitting" label="Tags" hint="" outlined multiple
                      chips clearable dense></v-combobox>
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
                <v-textarea v-model="editingModel.description" :loading="isSubmitting" rows="1" label="Description"
                  hint="" auto-grow outlined clearable dense data-test="train-model-edit-model-description"></v-textarea>
                <v-textarea v-model="editingModel.architecture" :loading="isSubmitting" rows="7" label="Architecture"
                  hint="" outlined clearable dense></v-textarea>
                <v-divider class="mb-4"></v-divider>
                <div class="d-flex justify-end">
                  <v-btn :loading="isSubmitting" depressed color="warning" @click="dialogEdit = false" class="mr-4"
                    data-test="train-model-edit-model-cancel">
                    Cancel
                  </v-btn>
                  <v-btn :loading="isSubmitting" depressed color="success" @click="saveModelChanges"
                    data-test="train-model-edit-model-confirm">Save Changes</v-btn>
                </div>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Delete model</span>
              </v-card-title>
              <v-card-text>Are you sure you want to delete the model {{ deletingModelName }}?</v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="dialogDelete = false"> Cancel </v-btn>
                <v-btn color="error darken-1" text @click="deleteModel" data-test="train-model-delete-model-confirm">
                  Confirm </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- </v-toolbar> -->
        </template>

        <template v-slot:item.actions="{ item }">
          <v-icon small @click="
            editingModel = { ...item };
          dialogEdit = true;
          " data-test="train-model-edit-model">
            mdi-pencil
          </v-icon>
          <v-icon small class="mx-2" @click="duplicateModel(item)" data-test="train-model-duplicate-model">
            mdi-content-copy </v-icon>
          <v-icon small @click="
            deletingModelId = item.id;
          deletingModelName = item.nickname;
          dialogDelete = true;
          " data-test="train-model-delete-model">
            mdi-delete
          </v-icon>
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
  id: '',
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
  tag: [],
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
      deletingModelId: '',
      deletingModelName: '',
      modelList: [],
      selectedModels: [],
      searchText: '',
      selectedTags: [],
      dialogEdit: false,
      dialogDelete: false,
      headers: [
        { text: 'Nickname', value: 'nickname' },
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
  computed: {
    filteredModelList() {
      if (this.selectedTags.length > 0) {
        return this.modelList.filter(model =>
          model.tags && this.selectedTags.every(tag => model.tags.includes(tag))
        );
      } else {
        return this.modelList;
      }
    },
  },
  methods: {
    trainModel() {
      this.$router.push({ name: 'TrainPad' });
    },
    filterByTag(tag) {
      if (this.selectedTags.includes(tag)) {
        this.selectedTags = this.selectedTags.filter(t => t !== tag);
      } else {
        this.selectedTags.push(tag);
      }
    },
    clearSelectedTags() {
      this.selectedTags = [];
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
        this.isLoading = true;
        const response = await APIGetAllModels();
        this.modelList = response?.data?.data;
      } catch (error) {
        console.error('Error fetching model list:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async setCurrentModel() {
      try {
        const response = await APISetCurrentModel(this.editingModel.id);
        this.currentModel = { ...this.editingModel };
      } catch (error) {
        console.error('Error setting current model:', error);
      }
    },
    async deleteModel() {
      this.isSubmitting = true;
      try {
        await APIDeleteModel(this.deletingModelId);
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
        await APIDuplicateModel(item.id);
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
        await APIUpdateModel(this.editingModel.id, this.editingModel);
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
