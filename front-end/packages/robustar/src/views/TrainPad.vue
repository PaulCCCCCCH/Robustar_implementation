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
          <v-btn depressed color="primary" class="mx-auto" @click="start_training">
            Start Training
          </v-btn>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APIStartTrain } from '@/apis/train';
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
    print_config() {
      console.log(this.configs);
    },
    start_training() {
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
        window.location.replace('http://localhost:6006');
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APIStartTrain(
        {
          configs: this.configs,
          info: 'placeholder',
        },
        success,
        failed
      );
    },
  },
};
</script>

<style type="text/css">
/* body {
  margin-top: 20px;
  color: #1a202c;
  text-align: left;
  background-color: #e2e8f0;
}

.main-body {
  padding: 15px;
}

.nav-link {
  color: #4a5568;
}

.card {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm > .col,
.gutters-sm > [class*='col-'] {
  padding-right: 8px;
  padding-left: 8px;
}

.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}

.h-100 {
  height: 100% !important;
}

.shadow-none {
  box-shadow: none !important;
} */
</style>
