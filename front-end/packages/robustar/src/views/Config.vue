<template>
  <div class="d-flex flex-column align-center">
    <table border="1" cellspacing="2" cellpadding="0">
      <tr v-for="(value, key) of configs">
        <th class="key">{{key}}</th>
        <td class="value">{{value}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { APIGetConfig } from '@/apis/config';
export default {
  name: 'Config',
  data() {
    return {
      configs:null,
    };
  },
  methods: {
    getConfigSuccess(res){
        console.log(res);
        this.configs = res.data.data;
    },
    getConfigFailed(res){
        console.log(res);
        this.configs = undefined;
    },
    startGettingConfig() {
      APIGetConfig(
        this.getConfigSuccess,
        this.getConfigFailed
      );
    },
  },
  beforeMount(){
      this.startGettingConfig();
  }
};
</script>