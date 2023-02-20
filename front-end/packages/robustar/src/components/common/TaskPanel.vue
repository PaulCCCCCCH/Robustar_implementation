<template>
  <v-card
    style="position: absolute; top: 50px; right: 100px; width: 1000px; z-index: 999; padding: 30px"
    elevation="4"
  >
    <v-row align="center" justify="center">
      <v-col v-if="digest.length == 0" cols="12" lg="12" align="center" justify="center">
        <p data-test="task-center-p-no-task" style="color: gray">No task is running now.</p>
      </v-col>
    </v-row>

    <!-- <v-row v-for="(item, index) in digest" align="center" justify="center" :key="item[0]"> -->
    <v-row v-for="(item, index) in digest" align="center" justify="center" :key="index">
      <v-col cols="12" lg="1" align="center" justify="center" data-test="task-panel-item-name">
        <v-btn
          v-if="item[5]"
          color="green"
          icon
          @click="stopTask(item[4])"
          data-test="task-panel-task-done"
          ><v-icon>mdi-checkbox-marked</v-icon></v-btn
        >
        <v-btn v-else color="red" icon @click="stopTask(item[4])" data-test="task-panel-stop-task"
          ><v-icon>mdi-minus-box</v-icon></v-btn
        >
      </v-col>
      <v-col cols="12" lg="2" align="center" justify="center">{{ item[0] }}</v-col>
      <v-col cols="12" lg="5" align="center" justify="center">
        <v-progress-linear
          data-test="task-panel-progress-linear"
          :color="getProgressColor(Math.round(item[1] * 100) / 1)"
          height="20"
          v-bind:value="item[1] * 100"
          >{{ Math.round(item[1] * 100) / 1 }}% ({{ item[2] }})</v-progress-linear
        >
      </v-col>
      <v-col cols="12" lg="3" align="center" justify="center">{{ item[3] }}</v-col>
    </v-row>

    <v-row align="center" justify="center">
      <v-col v-if="digest.length > 0" cols="12" lg="12" align="center" justify="center">
        <v-btn color="warning" outlined @click="stopAllTasks" data-test="task-panel-stop-all-tasks"
          >stop all tasks <v-icon class="ml-2">mdi-trash-can-outline</v-icon></v-btn
        >
      </v-col>
    </v-row>
  </v-card>
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
        this.$root.alert('error', error.response?.data?.detail || 'Failed to stop task');
      }
    },
    async stopAllTasks() {
      try {
        await Promise.all(this.digest.map((task) => this.stopTask(task[4])));
      } catch (error) {
        console.log(error);
        this.$root.alert('error', 'Failed to stop task');
      }
    },
  },
};
</script>
