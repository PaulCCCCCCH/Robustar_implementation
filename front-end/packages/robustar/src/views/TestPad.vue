<template>
  <div class="container">
    <el-card class="box-card form-group">
      <div slot="header" class="clearfix text-center">
        <h1>Test Settings</h1>
      </div>
      <div>
        <button type="button" class="btn btn-primary" @click="start_testing('validation')">
          Start Testing on Validation Set
        </button>
        <button type="button" class="btn btn-primary" @click="start_testing('test')">
          Start Testing on Test Set
        </button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { APIStartTest } from '@/apis/test';
export default {
  name: 'TestPad',
  data() {
    return {
    };
  },
  methods: {
    start_testing(split) {
      const success = (response) => {
        // TODO: deal with RResponse.fail
        console.log(response);
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APIStartTest(
        {
          split: split,
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
