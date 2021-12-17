<template>
  <div class="container">
    <el-card class="box-card form-group">
      <div slot="header" class="clearfix text-center">
        <h1>Test Settings</h1>
      </div>
      <div>
        <button type="button" class="btn btn-primary" @click="start_training">
          Start Testing
        </button>
      </div>

      <!-- <button class="btn btn-info" type="button">Save configs</button> -->
    </el-card>
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
body {
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
}
</style>
