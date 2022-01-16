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
  },
  beforeMount() {
    this.startGettingConfig();
  },
};
</script>

<style>
table {
  width: 60%;
  margin: 0 auto;
  padding-top: 10px;
  font-family: "Trebuchet MS", sans-serif;
  font-size: 16px;
  font-weight: bold;
  line-height: 1.4em;
  font-style: normal;
  border-collapse:separate;
}

.key {
    color:#fff;
    width: 40%;
    text-shadow:1px 1px 1px #2E7FD1;
    background-color:#74A2CF;
    border:1px solid #4E88C2;
    border-right:3px solid #74A2CF;
    padding:0px 10px;
    background: linear-gradient(to right, #74A2CF , #2E7FD1);
    -moz-border-radius:5px 0px 0px 5px;
    -webkit-border-top-left-radius:5px;
    -webkit-border-bottom-left-radius:5px;
    border-top-left-radius:5px;
    border-bottom-left-radius:5px;
}
.value {
    padding:10px;
    width: 60%;
    text-align:center;
    background-color:#E5F2FF;
    border: 2px solid #E9EFF5;
    -moz-border-radius:2px;
    -webkit-border-radius:2px;
    border-radius:2px;
    color:#666;
    text-shadow:1px 1px 1px #fff;
}
</style>
