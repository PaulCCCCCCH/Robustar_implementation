<template>
  <div id="training-settings-page" class="container">
    <el-card class="box-card form-group">
      <div slot="header" class="clearfix text-center">
        <h1>Influence Calculation</h1>
      </div>
      <div>
        <h3>Settings</h3>

        <!-- Select number of test samples per class-->
        <div class="form-group">
          <label>Number of test samples for which we calculate influence</label>
          <input
            type="number"
            class="form-control"
            aria-describedby="fullNameHelp"
            placeholder="Enter a value"
            v-model="configs.n_test_per_class"
            value="10"
          />
          <small class="form-text text-muted">A value of -1 means calculating influence for the entire test set</small>
        </div>

        <hr />

        <button type="button" class="btn btn-primary" @click="start_calculation">
          Start calculation
        </button>
      </div>

      <!-- <button class="btn btn-info" type="button">Save configs</button> -->
    </el-card>
  </div>
</template>

<script>
import { APICalculateInfluence } from '@/apis/predict';
export default {
  name: 'InfluencePad',
  data() {
    return {
     // Training configs
      configs: {
        n_test_per_class: 10,
      },
    };
  },
  methods: {
    start_calculation() {
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APICalculateInfluence(
        {
          configs: this.configs,
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
