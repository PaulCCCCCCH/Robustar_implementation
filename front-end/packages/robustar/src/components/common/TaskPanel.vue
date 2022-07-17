<template>
  <v-row align="center" justify="center">
    <v-col cols="12" lg="6"></v-col>
    <v-col cols="12" lg="6">
      <v-card
        style="
          position: fixed;
          width: 40%;
          z-index: 10;
          padding-top: 3rem;
          padding-bottom: 3rem;
          align: center;
        "
        elevation="4"
      >
        <v-row align="center" justify="center">
          <v-col cols="12" lg="12" align="center" justify="center" v-if="digest.length == 0">
            <p style="color: gray">No task is running now.</p>
          </v-col>
        </v-row>
        <!-- <v-row v-for="(item, index) in digest" align="center" justify="center" :key="item[0]"> -->
        <v-row v-for="(item, index) in digest" align="center" justify="center" :key="index">
          <v-col cols="12" lg="1" align="center" justify="center">
            <v-btn color="red" icon @click="stopTask(item[4])"
              ><v-icon>mdi-minus-box</v-icon></v-btn
            >
          </v-col>
          <v-col cols="12" lg="2" align="center" justify="center">{{ item[0] }}</v-col>
          <v-col cols="12" lg="5" align="center" justify="center">
            <v-progress-linear
              :color="getProgressColor(Math.round(item[1] * 100) / 1)"
              height="20"
              v-bind:value="item[1] * 100"
              >{{ Math.round(item[1] * 100) / 1 }}% ({{ item[2] }})</v-progress-linear
            >
          </v-col>
          <v-col cols="12" lg="4" align="center" justify="center">{{ item[3] }}</v-col>
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
    };
  },
  sockets: {
    connect() {
      console.log('connect');
    },
    afterConnect(data) {
      console.log(data);
    },

    // get digest from backend
    digest(data) {
      this.digest = data.digest;
    },
  },
  methods: {
    // toggleTaskspanel() {
    //   this.isTaskspanelHidden = !this.isTaskspanelHidden;
    // },
    getProgressColor(successPercent) {
      let colorBar = '';
      if (successPercent < 50) {
        colorBar = '#f50';
      } else if (successPercent >= 50 && successPercent < 90) {
        colorBar = '#FF9900';
      } else if (successPercent >= 90) {
        colorBar = '#87d068';
      }
      return colorBar;
    },
    async stopTask(tid) {
      try {
        await APIStopTask(tid);
      } catch (error) {
        console.log(error);
        this.$root.alert('error', 'Failed to stop task');
      }
    },
  },
};
</script>
