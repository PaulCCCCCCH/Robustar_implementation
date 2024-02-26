<template>
  <div class="d-flex flex-column align-center">
    <v-sheet rounded width="800" elevation="3" class="my-8 pa-8">
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
          v-model="configs.num_workers"
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
          <v-btn
            depressed
            color="primary"
            class="mx-auto"
            @click="startTraining"
            data-test="train-pad-btn-start-training"
          >
            START TRAINING
          </v-btn>
        </div>
        <div class="d-flex flex-column align-center my-4">
          <v-btn
            depressed
            color="primary"
            class="mx-auto"
            @click="stopTraining"
            data-test="train-pad-btn-stop-training"
          >
            STOP TRAINING
          </v-btn>
        </div>
      </v-form>
    </v-sheet>
  </div>
</template>

<script>
import { APIStartTrain, APIStopTrain } from '@/services/train';
import { APIGetCurrentModel } from '@/services/model/';
import { configs } from '@/configs.js';
export default {
  name: 'TrainPad',
  data() {
    return {
      // model_options: [
      //   'resnet-18-32x32',
      //   'resnet-18',
      //   'resnet-34',
      //   'resnet-50',
      //   'resnet-101',
      //   'resnet-152',
      //   'mobilenet-v2',
      // ],
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
        model_id: 1,
        use_paired_train: true,
        mixture: 'random_pure',
        auto_save_model: true,
        batch_size: 128,
        shuffle: true,
        learn_rate: 0.1,
        paired_train_reg_coeff: 0.001,
        epoch: 20,
        num_workers: 8,
        user_edit_buffering: false,
        use_tensorboard: true,
        save_every: 5,
      },
    };
  },
  async created() {
    try {
      const res = await APIGetCurrentModel();
      const model = res?.data?.data;
      if (model) {
        this.configs.model_name = model.nickname;
        this.configs.epoch = model.epoch;
        this.configs.pretrain = model.pretrained;
      }
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    async startTraining() {
      this.$root.startProcessing('The training is starting. Please wait...');
      try {
        // TODO(Chonghan): Check whether current model is set or not, both here and from the back end
        const res = await APIStartTrain({
          configs: this.configs,
          info: 'placeholder',
        });
        this.$root.finishProcessing();
        this.$root.alert('success', 'Training started successfully');
        window.open(configs.tensorboardUrl);
      } catch (error) {
        this.$root.finishProcessing();
        this.$root.alert('error', error.response?.data?.detail || 'Training failed');
      }
    },
    async stopTraining() {
      try {
        const res = await APIStopTrain();
        this.$root.alert('success', 'Successfully stop training');
      } catch (error) {
        this.$root.alert('error', error.response?.data?.detail || 'Failed to stop training');
      }
    },
  },
};
</script>
