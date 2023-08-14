<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="mt-8 pa-4">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col class="d-flex justify-start align-center">
              <v-card-title class="mb-0">Current model: ResNet</v-card-title>
            </v-col>
            <v-col class="d-flex justify-end align-center" cols="2">
              <v-btn block>Train</v-btn>
            </v-col>
          </v-row>
          <v-row justify="space-between">
            <v-col cols="2">Created time:</v-col>
            <v-col cols="2">Trained:</v-col>
            <v-col cols="2">Accuracies:</v-col>
            <v-col cols="2">Epoch:</v-col>
          </v-row>
          <v-card-text>Description:</v-card-text>
          <v-card-text>Architecture:</v-card-text>
        </v-col>
      </v-row>
    </v-sheet>

    <v-sheet rounded width="800" elevation="3" class="mt-4 pa-4">
      <v-row class="d-flex flex-column align-center">
        <v-col cols="12">
          <v-card-title>All models</v-card-title>

          <v-row class="d-flex" row-gap="2">
            <v-col>
              <v-select :items="['a', 'b', 'c']" label="Model" hint="" outlined dense></v-select>
            </v-col>
            <v-col>
              <ModelUploader />
            </v-col>
            <v-col>
              <v-btn block>Set as current model</v-btn>
            </v-col>
          </v-row>

          <v-divider class="mt-4 mb-8"></v-divider>
          <v-row justify="space-between">
            <v-col cols="3">Created time:</v-col>
            <v-col cols="3">Last trained:</v-col>
            <v-col cols="3">Accuracies:</v-col>
            <v-col cols="3">Epoch:</v-col>
          </v-row>
          <v-card-text>Description:</v-card-text>
          <v-card-text>Architecture:</v-card-text>
          <v-row class="row" row-gap="2">
            <v-col><v-btn block>Delete</v-btn></v-col>
            <v-col><v-btn block>Duplicate</v-btn></v-col>
            <v-col><v-btn block>Save changes</v-btn></v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-sheet>
  </div>
</template>

<script>
import ModelUploader from '@/components/ModelUploader';

export default {
  name: 'TrainModel',
  components: {
    ModelUploader,
  },
};
</script>
