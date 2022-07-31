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
          :true-value="true"
          :false-value="false"
          :ripple="false"
        ></v-checkbox>
        <!-- Model Name -->
        <v-text-field
          v-model="configs.model_name"
          label="Model name"
          outlined
          clearable
        ></v-text-field>
        <!-- Save model -->
        <v-checkbox
          v-model="configs.auto_save_model"
          label="Save the model per epoch"
          :true-value="true"
          :false-value="false"
          :ripple="false"
          class="mt-n2 mb-1"
        ></v-checkbox>
        <div v-if="configs.auto_save_model">
          <!-- Save path -->
          <v-text-field
            v-model="configs.save_dir"
            label="The directory to save model to"
            outlined
            clearable
          ></v-text-field>
          <!-- Save every-->
          <v-text-field
            value="10"
            v-model="configs.save_every"
            label="Save every n epochs"
            outlined
            clearable
            type="number"
          ></v-text-field>
        </div>

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
          v-model="configs.learn_rate"
          value="0.1"
          label="Learning rate"
          outlined
          clearable
          type="number"
        ></v-text-field>
        <!-- Set Epoch -->
        <v-text-field
          value="10"
          v-model="configs.epoch"
          label="Epoch"
          outlined
          clearable
          type="number"
        ></v-text-field>
        <!-- Set Batch size -->
        <v-text-field
          v-model="configs.batch_size"
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
          :true-value="true"
          :false-value="false"
          :ripple="false"
          class="mb-2"
        ></v-checkbox>
        <div v-if="configs.use_paired_train">
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
            v-model="configs.paired_train_reg_coeff"
            value="1e-3"
            label="Paired training strength"
            outlined
            clearable
            messages="The constant weight for the loss term calculated with paired training data. Increasing the value will result in a stronger regularization effect."
          ></v-text-field>
          <v-checkbox
            v-model="configs.user_edit_buffering"
            label="Store annotation data in RAM when training"
            messages="This speeds up training but may increase RAM usage"
            :true-value="true"
            :false-value="false"
            :ripple="false"
          ></v-checkbox>
        </div>
        <v-divider class="my-8"></v-divider>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="startTraining">
            START TRAINING
          </v-btn>
        </div>
        <div class="d-flex flex-column align-center my-4">
          <v-btn depressed color="primary" class="mx-auto" @click="stopTraining">
            STOP TRAINING
          </v-btn>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APIStartTrain, APIStopTrain } from '@/services/train';
export default {
  name: 'TrainPad',
  data() {
    return {
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
        model_name: 'my-test-model',
        // weight: "/Robustar2/checkpoint_images",
        weight: '',
        train_path: '/Robustar2/dataset/train',
        test_path: '/Robustar2/dataset/test',
        class_path: './model/cifar-class.txt',
        port: '8000',
        save_dir: '/Robustar2/checkpoints',
        use_paired_train: false,
        mixture: 'random_pure',
        user_edit_buffering: false,

        // Selection for the following not implemented
        paired_data_path: '/Robustar2/dataset/paired',
        device: 'cuda',
        auto_save_model: true,
        save_every: 5,
        batch_size: '128',
        shuffle: true,
        learn_rate: 0.1,
        pgd: false,
        paired_train_reg_coeff: 0.001,
        image_size: 32,
        epoch: 20,
        thread: 8,
        pretrain: false,
      },
    };
  },
  methods: {
    trainingSuccess(res) {
      const getPort = async () => {
        const config = await fetch("serverUrls.json");
        return await config.json();
      }
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('success', 'Training started successfully');
      getPort.then(port => {
        window.open('http://localhost:'+port.tensorboardPort)
      });
    },
    trainingFailed(res) {
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('error', 'Training failed');
    },
    startTraining() {
      this.$root.startProcessing('The training is starting. Please wait...');
      APIStartTrain(
        {
          configs: this.configs,
          info: 'placeholder',
        },
        this.trainingSuccess,
        this.trainingFailed
      );
    },
    stopSuccess(res) {
      console.log(res);
      alert('Successfully stop training');
    },
    stopFailed(res) {
      console.log(res);
      alert('Failed to stop training');
    },
    stopTraining() {
      APIStopTrain(this.stopSuccess, this.stopFailed);
    },
  },
};
</script>
