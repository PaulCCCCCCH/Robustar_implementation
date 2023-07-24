<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="1000" elevation="3" class="mt-8 pa-4">
      <v-row class="d-flex flex-column align-center">
        <v-col cols="12">
          <v-card-title>Current model: ResNet</v-card-title>
          <v-row justify="space-between">
            <v-col cols="2">Created time:</v-col>
            <v-col cols="2">Last trained:</v-col>
            <v-col cols="2">Accuracies:</v-col>
            <v-col cols="2">Epoch:</v-col>
          </v-row>
          <v-card-text>Description:</v-card-text>
          <v-card-text>Architecture:</v-card-text>
        </v-col>
      </v-row>
    </v-sheet>
    <v-sheet rounded width="1000" elevation="3" class="mt-4 pa-4">
      <v-row class="d-flex flex-column align-center">
        <v-col cols="12">
          <v-card-title>All models</v-card-title>
          <div class="d-flex">
            <v-select :items="['a', 'b', 'c']" label="Model" hint="" outlined dense></v-select>
            <ModelUploader />
          </div>
          <v-divider class="mt-4 mb-8"></v-divider>
          <v-row justify="space-between">
            <v-col cols="3">Created time:</v-col>
            <v-col cols="3">Last trained:</v-col>
            <v-col cols="3">Accuracies:</v-col>
            <v-col cols="3">Epoch:</v-col>
          </v-row>
          <v-card-text>Description:</v-card-text>
          <v-card-text>Architecture:</v-card-text>
          <v-row justify="space-between">
            <v-col cols="2" color="primary"><v-btn>Delete</v-btn></v-col>
            <v-col cols="2"><v-btn>Duplicate</v-btn></v-col>
            <v-col cols="2"><v-btn>Set a current model</v-btn></v-col>
            <v-col cols="2"><v-btn>Train</v-btn></v-col>
            <v-col cols="2"><v-btn>Save changes</v-btn></v-col>
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
