<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-4">
      <div class="text-h4 text-center font-weight-medium">Training Settings</div>
      <v-divider class="mt-4 mb-8"></v-divider>
      <v-form>
        <div class="text-h5 mb-4">System settings</div>
        <!-- Shuffle training set  -->
        <v-checkbox
          v-model="configs.shuffle"
          label="shuffle the trainset"
          true-value="yes"
          false-value="no"
          :ripple="false"
        ></v-checkbox>
        <!-- Save model -->
        <v-checkbox
          v-model="configs.auto_save_model"
          label="save the model per epoch"
          true-value="yes"
          false-value="no"
          :ripple="false"
          class="mt-n2 mb-1"
        ></v-checkbox>
        <!-- Save path -->
        <v-text-field
          v-model="configs.save_dir"
          label="save model to"
          outlined
          clearable
        ></v-text-field>
        <!-- Select device -->
        <v-select
          v-model="configs.device"
          :items="[
            { text: 'cpu', value: 'cpu' },
            { text: 'cuda', value: 'cuda' },
          ]"
          label="Select training device"
          outlined
        ></v-select>
        <!-- Set num of dataloader workers -->
        <v-text-field
          v-model="configs.thread"
          label="Number of dataloader workers"
          outlined
          clearable
          type="number"
        ></v-text-field>
        <v-divider class="mt-4 mb-8"></v-divider>
        <div class="text-h5 mb-4">Hyperparameters</div>
        <!-- Set learning rate -->
        <v-text-field
          value="0.1"
          label="Learning rate"
          outlined
          clearable
          type="number"
        ></v-text-field>
        <!-- Set Epoch -->
        <v-text-field value="10" label="Epoch" outlined clearable type="number"></v-text-field>
        <!-- Set Image size -->
        <v-text-field value="32" label="Image size" outlined clearable type="number"></v-text-field>
        <!-- Set Batch size -->
        <v-text-field
          value="128"
          label="Batch size"
          outlined
          clearable
          type="number"
        ></v-text-field>
        <v-divider class="mt-4 mb-8"></v-divider>
        <div class="text-h5 mb-4">Paired Training</div>
        <!-- Use paired training ? -->
        <v-checkbox
          v-model="configs.use_paired_train"
          label="use paired training"
          true-value="yes"
          false-value="no"
          :ripple="false"
          class="mb-2"
        ></v-checkbox>
        <div v-if="configs.use_paired_train === 'yes'">
          <!-- Paired data path -->
          <v-text-field
            v-model="configs.paired_data_path"
            label="specify the path to the paired training set"
            outlined
            clearable
          ></v-text-field>
          <v-select
            v-model="configs.mixture"
            :items="mixture_methods"
            label="Paired data noise"
            outlined
          ></v-select>
          <v-text-field
            value="1e-4"
            label="Paired training strength"
            outlined
            clearable
            messages="The constant weight for the loss term calculated with paired training data. Increasing the value will result in a stronger regularization effect."
          ></v-text-field>
        </div>
        <v-divider class="my-8"></v-divider>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="startTraining">
            Start Training
          </v-btn>
        </div>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="stopTraining">
            Stop Training
          </v-btn>
        </div>
      </v-form>
    </v-sheet>

    <!-- api feedback -->

    <v-overlay :value="sending" opacity="0.7">
      <v-progress-circular indeterminate size="30" class="mr-4"></v-progress-circular>
      <span style="vertical-align: middle"> The training is going on. Please wait... </span>
    </v-overlay>

    <!-- training succeeded -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbar"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Training succeeded</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="accent" text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>

    <!-- training failed -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbarError"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Training failed</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbarError = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { APIStartTrain, APIStopTrain } from '@/apis/train';
export default {
  name: 'TrainPad',
  data() {
    return {
      sending: false,
      snackbar: false,
      snackbarError: false,

      model_options: [
        'resnet-18-32x32',
        'resnet-18',
        'resnet-34',
        'resnet-50',
        'resnet-101',
        'resnet-152',
        'mobilenet-v2',
      ],
      mixture_methods: [
        'pure_black',
        'noise',
        'noise_weak',
        'noise_minor',
        'random_pure',
        'hstrips',
        'vstrips',
        'mixture',
      ],

      // Training configs
      configs: {
        model: 'resnet-18-32x32',
        // weight: "/Robustar2/checkpoint_images",
        weight: '',
        train_path: '/Robustar2/dataset/train',
        test_path: '/Robustar2/dataset/test',
        class_path: './model/cifar-class.txt',
        port: '8000',
        save_dir: '/Robustar2/checkpoints',
        use_paired_train: 'false',
        mixture: 'random_pure',

        // Selection for the following not implemented
        paired_data_path: '/Robustar2/dataset/paired',
        device: 'cuda',
        auto_save_model: 'yes',
        batch_size: '128',
        shuffle: 'yes',
        learn_rate: 0.1,
        pgd: 'no PGD',
        paired_train_reg_coeff: 0.001,
        image_size: 32,
        epoch: 20,
        thread: 8,
        pretrain: 'no',
      },
    };
  },
  methods: {
    trainingSuccess(res) {
      console.log(res);
      this.sending = false;
      this.snackbar = true;
      window.open('http://localhost:6006');
    },
    trainingFailed(res) {
      console.log(res);
      this.sending = false;
      this.snackbarError = true;
    },
    startTraining() {
      this.sending = true;
      APIStartTrain(
        {
          configs: this.configs,
          info: 'placeholder',
        },
        this.trainingSuccess,
        this.trainingFailed
      );
    },
    stopSuccess(res){
      console.log(res);
      alert("Successfully stop training");
    },
    stopFailed(res){
      console.log(res);
      alert("Failed to stop training");
    },
    stopTraining() {
      APIStopTrain(this.stopSuccess, this.stopFailed);
    },
  },
};
</script>