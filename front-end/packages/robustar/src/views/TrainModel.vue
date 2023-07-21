<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-8">
      <!-- <v-container> -->
      <v-row class="d-flex flex-column align-center">
        <v-col cols="8">
          <v-card-title class="text-h4 text-center font-weight-medium text--primary"
            >current model: ResNet</v-card-title
          >
          <v-divider class="mt-4 mb-8"></v-divider>
          <v-card-subtitle class="text-h5 mb-4">Current model: ResNet</v-card-subtitle>
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
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-8">
      <v-row class="d-flex flex-column align-center">
        <v-col cols="8">
          <v-card-title>All models</v-card-title>
          <v-row justify="space-between" align="center">
            <v-col cols="4"
              ><v-select :items="model_options" v-model="$root.imageClass" clearable></v-select
            ></v-col>
            <v-col cols="2"
              ><v-btn :true-value="true" :false-value="false" class="mt-n2 mb-1"
                >Upload New Model</v-btn
              ></v-col
            >
          </v-row>
          <v-divider class="mt-4 mb-8"></v-divider>
          <v-card-text>{{ $root.imageClass }}</v-card-text>
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
      <!-- </v-container> -->
    </v-sheet>
  </div>
</template>
