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
      <v-card-title>
        All models <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="modelList"
        :single-select="singleSelect"
        :search="search"
        item-key="nickname"
        show-select
        class="elevation-1"
        width="1000"
      >
        <template v-slot:top>
          <!-- <v-toolbar flat> -->
            <v-dialog v-model="dialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="text-h5">Edit item</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <div class="d-flex justify-space-between">
                      <span style="width: 400px"
                        ><v-text-field
                          v-model="viewingModel.nickname"
                          :loading="isSubmitting"
                          label="Model Name"
                          hint=""
                          outlined
                          clearable
                          dense
                        ></v-text-field
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
                      <v-btn :loading="isSubmitting" depressed color="error" @click="deleteModel"
                        >Delete</v-btn
                      >
                      <v-btn
                        :loading="isSubmitting"
                        depressed
                        color="warning"
                        class="mx-4"
                        @click="duplicateModel"
                        >Duplicate</v-btn
                      >
                      <v-btn
                        :loading="isSubmitting"
                        depressed
                        color="success"
                        @click="saveModelChanges"
                        >Save Changes</v-btn
                      >
                    </div>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
                  <v-btn color="blue darken-1" text @click="saveModelChanges"> Save </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
                  <v-btn color="blue darken-1" text @click="deleteModel(model.nickname)">
                    OK
                  </v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          <!-- </v-toolbar> -->
          <v-switch v-model="singleSelect" label="Single select" class="pa-3"></v-switch>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
          <v-icon small @click="deleteModel"> mdi-delete </v-icon>
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
      currentModel: { ...initialModel },
      isSubmitting: false,
      viewingModel: { ...initialModel },
      modelList: [],
      epoch: 0,
      selectedModelIndex: null,
      singleSelect: false,
      selected: [],
      search: '',
      editedIndex: -1,
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: 'nickname',
          align: 'start',
          sortable: false,
          value: 'nickname',
        },
        { text: 'Tag', value: 'tag' },
        { text: 'Created Time', value: 'create_time' },
        { text: 'Last Trained', value: 'last_trained' },
        { text: 'Epoch', value: 'epoch' },
        { text: 'Test Accuracy', value: 'test_accuracy' },
        { text: 'Train Accuracy', value: 'test_accuracy' },
        { text: 'Validation Accuracy', value: 'test_accuracy' },
        { text: 'Description', value: 'description' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      editedItem: {
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
      },
    };
  },
  mounted() {
    this.getCurrentModel();
    this.getModelList();
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  methods: {
    trainModel() {
      this.$router.push({ name: 'TrainPad' });
    },
    selectModel(index) {
      if (this.selectedModelIndex === index) {
        this.selectedModelIndex = null;
        this.viewingModel = { ...initialModel };
      } else {
        this.selectedModelIndex = index;
        this.viewingModel = { ...this.modelList[index] };
      }
    },
    editItem(item) {
      this.editedIndex = this.modelList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
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
        this.modelList = (await APIGetAllModels())?.data?.data;
        this.viewingModel = this.modelList.length ? { ...this.modelList[0] } : { ...initialModel };
      } catch (error) {
        console.error('Error fetching model list:', error);
      }
    },
    async setCurrentModel() {
      try {
        const response = await APISetCurrentModel(this.viewingModel.nickname);
        this.currentModel = { ...this.viewingModel };
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
        // this.dialogDelete = true;
      } catch (error) {
        console.error('Error deleting model:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
    async duplicateModel() {
      this.isSubmitting = true;
      try {
        await APIDuplicateModel(this.viewingModel.nickname);
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
        await APIUpdateModel(this.modelList[this.editedIndex].nickname, this.viewingModel);
        this.getModelList();
        this.dialog = false;
      } catch (error) {
        console.error('Error saving model changes:', error);
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
