<template>
  <v-row align="center" justify="center">
    <v-col cols="12" lg="6"></v-col>
    <v-col cols="12" lg="6">

    <v-card
      style="position:fixed; width: 40%; z-index:10; padding-top:3rem; padding-bottom: 3rem; align: center;"
      elevation="4"
    >
      <v-row align="center" justify="center">
        <v-col cols="12" lg="12" align="center" justify="center" v-if="digest.length==0">
          <p style="color: gray;">No task is running now.</p>
        </v-col>
      </v-row>
      <v-row v-for="item in digest" align="center" justify="center" :key="item[0]">
        <v-col cols="12" lg="1" align="center" justify="center">
          <v-btn color="red" icon @click="stopTask(item[3])"><v-icon>mdi-minus-box</v-icon></v-btn>
        </v-col>
        <v-col cols="12" lg="2" align="center" justify="center">{{item[0]}}</v-col>
        <v-col cols="12" lg="5" align="center" justify="center">
          <v-progress-linear
            color="primary"
            height="20"
            v-bind:value="item[1]*100"
            striped
          >{{Math.round(item[1]*10000)/100}}%</v-progress-linear>
        </v-col>
        <v-col cols="12" lg="4" align="center" justify="center">{{item[2]}}</v-col>
      </v-row>
    
    </v-card>
    
    </v-col>
  </v-row>
</template>

<script>
import { APIStopTask } from '@/services/task';

export default {
  name: 'TaskPanel',
  data() {
    return {
      digest: [],
    }
  },
  sockets: {
    connect(){
      console.log('connect');
    },
    afterConnect(data){
      console.log(data);
    },

    // get digest from backend
    digest(data){
      this.digest = data.digest;
    },
  },
  methods: {
    // toggleTaskspanel() {
    //   this.isTaskspanelHidden = !this.isTaskspanelHidden;
    // },
    stopTaskSuccess(res){
        console.log(res);
        alert("Successfully stop task");
    },
    stopTaskFailed(res){
        console.log(res);
        alert("Failed to stop task");
    },
    stopTask(tid){
        APIStopTask(tid, this.stopTaskSuccess, this.stopTaskFailed);
    }
  },
};
</script>
