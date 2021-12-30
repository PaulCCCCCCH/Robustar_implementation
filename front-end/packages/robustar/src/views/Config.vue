<template>
  <div>
    <ul>
      <li v-for="(item, key) of configs">{{key}}:{{item}}</li>
    </ul>
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