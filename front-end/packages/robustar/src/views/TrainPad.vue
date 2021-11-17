<template>
  <div id="training-settings-page" class="container">
    <el-card class="box-card form-group">
      <div slot="header" class="clearfix text-center">
        <h1>Training Settings</h1>
      </div>
      <div>
        <h3>System settings</h3>

        <!-- Shuffle training set  -->
        <input
          type="checkbox"
          checked=""
          v-model="configs.shuffle"
          true-value="yes"
          false-value="no"
        />
        <label class="custom-control-label" for="shuffle-trainset">shuffle the trainset</label>

        <br />
        <!-- Save model -->
        <input
          type="checkbox"
          class="custom-control-input"
          id="epoch-save"
          checked=""
          v-model="configs.auto_save_model"
          true-value="yes"
          false-value="no"
        />
        <label class="custom-control-label" for="epoch-save">save the model per epoch</label>

        <!-- Save path -->
        <div class="form-group">
          <label>Save model to</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            v-model="configs.save_dir"
          />
          <small class="form-text text-muted"></small>
        </div>

        <div class="form-group">
          <label>Select training device</label>
          <select
            type="text"
            class="form-control"
            v-model="configs.device"
            aria-describedby="fullNameHelp"
          >
            <option value="cpu">cpu</option>
            <option value="cuda">cuda</option>
          </select>
        </div>

        <div class="form-group">
          <label>Number of dataloader workers</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            v-model="configs.thread"
            value="8"
          />
          <small class="form-text text-muted"></small>
        </div>

        <hr />

        <!-- <button type="button" @click="update_server" class="btn btn-primary">Update Server</button> -->
        <!-- <button type="reset" class="btn btn-light" onclick="location.replace('http://home.0cdl.com:6006')">Start Training</button> -->

        <h3>Hyperparameters</h3>
        <div class="form-group">
          <label>learning rate</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            value="0.1"
          />
          <small class="form-text text-muted"></small>
        </div>

        <div class="form-group">
          <label>Epoch</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            value="0.1"
          />
          <small class="form-text text-muted"></small>
        </div>

        <div class="form-group">
          <label>image size</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            value="32"
          />
          <small class="form-text text-muted"></small>
        </div>

        <div class="form-group">
          <label>batch size</label>
          <input
            type="text"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            value="64"
          />
          <small class="form-text text-muted"></small>
        </div>

        <hr />

        <h3>Paired Training</h3>
        <!-- Use paired training ? -->
        <div class="custom-control custom-checkbox">
          <input
            type="checkbox"
            id="use-pretrained"
            class="custom-control-input"
            v-model="configs.use_paired_train"
            true-value="yes"
            false-value="no"
          />
          <label class="custom-control-label" for="use-pretrained">Use paired training</label>
        </div>

        <!-- Options for paired training only -->
        <div v-if="configs.use_paired_train === 'yes'">
          <!-- Paired data path-->
          <div class="form-group">
            <label>Specify the path to the paired training set</label>
            <input
              type="text"
              class="form-control"
              v-model="configs.paired_data_path"
              aria-describedby="fullNameHelp"
              placeholder="Enter a value"
              value="/Robustar2/dataset/paired"
            />
            <small class="form-text text-muted"></small>
          </div>

          <!-- Mixture methods -->
          <div class="form-group">
            <label>Paired data noise</label>
            <select
              type="text"
              class="form-control"
              v-model="configs.mixture"
              aria-describedby="fullNameHelp"
              placeholder="Enter a value"
            >
              <option v-for="method in mixture_methods" :value="method" :key="method">
                {{ method }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Paired training strength</label>
            <input
              type="text"
              class="form-control"
              aria-describedby="fullNameHelp"
              placeholder="Enter a value"
              value="1e-4"
            />
            <small class="form-text text-muted">
              The constant weight for the loss term calculated with paired training data. Increasing
              the value will result in a stronger regularization effect.
            </small>
          </div>
        </div>

        <hr />
        <button type="button" class="btn btn-primary" @click="start_training">
          Start Training
        </button>
      </div>

      <!-- <button class="btn btn-info" type="button">Save configs</button> -->
    </el-card>
  </div>
</template>

<script>
import { APIStartTrain } from '@/apis/train';
import { APIGeneratePairedDataset } from '@/apis/generate';
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

      // Data generation configs
      generate_configs: {
        mirrored_data_path: '/Robustar2/dataset/train',
        user_edit_path: '/Robustar2/user-edit.json',
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
    generate_paired_data() {
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
        alert(response.data.msg);
      };

      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APIGeneratePairedDataset(
        this.generate_configs.mirrored_data_path,
        this.generate_configs.user_edit_path,
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
