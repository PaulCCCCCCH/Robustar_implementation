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

      <div class="pa-4">
        <v-text-field label="Name" hint="" outlined clearable required dense></v-text-field>
        <v-textarea
          label="Description"
          hint=""
          auto-grow
          outlined
          clearable
          required
          dense
        ></v-textarea>
        <v-checkbox v-model="usePredefined" label="use predefined"></v-checkbox>
        <div v-if="!usePredefined">
          <div class="mb-4">
            Weight File (optional) <v-btn class="ml-4" depressed outlined small>choose file</v-btn>
          </div>
          <v-textarea label="Code" hint="" rows="5" filled clearable required dense></v-textarea>
        </div>
        <div v-else>
          <v-text-field
            label="num_classes"
            type="number"
            min="0"
            hint=""
            outlined
            clearable
            required
            dense
          ></v-text-field>
          <v-select
            :items="['a', 'b', 'c']"
            label="Model Architecture"
            hint=""
            outlined
            dense
          ></v-select>
        </div>
      </div>

      <v-divider></v-divider>

      <v-card-actions class="d-flex flex-column align-start py-8">
        <div class="mb-4">
          <v-btn depressed color="primary" class="mr-8"> Submit </v-btn>
          <span>Status:</span>
        </div>
        <div>
          <div>Feedback</div>
          <code>print("hello world")</code>
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
    };
  },
};
</script>
