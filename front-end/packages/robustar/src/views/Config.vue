<template>
  <div>
    <table class="table">
      <tr v-for="(value, key) of configs">
        <th class="key">{{ key }}</th>
        <td class="value">{{ value }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { APIGetConfig } from '@/services/config';
export default {
  name: 'Config',
  data() {
    return {
      configs: null,
      name: null,
    };
  },
  methods: {
    getConfigSuccess(res) {
      console.log(res);
      this.configs = res.data.data;
    },
    getConfigFailed(res) {
      console.log(res);
      this.configs = undefined;
    },
    startGettingConfig() {
      APIGetConfig(this.getConfigSuccess, this.getConfigFailed);
    },
    changeName() {
      if (configs.key == batch_size) {
        name = 'Batch Size';
        configs.key = name;
      }
    },
  },
  beforeMount() {
    this.startGettingConfig();
    this.changeName();
  },
};
</script>

<style>
.table {
  margin: auto;
  border-top: 1px solid #e6eaee;
  border-left: 1px solid #e6eaee;
}
.key {
  width: 200px;
  background-color: #eff3f6;
  color: #393c3e;
  border-bottom: 1px solid #e6eaee;
  border-right: 1px solid #e6eaee;
}
.value {
  width: 250px;
  height: 35px;
  line-height: 35px;
  box-sizing: border-box;
  padding: 0 10px;
  border-bottom: 1px solid #e6eaee;
  border-right: 1px solid #e6eaee;
}
</style>
