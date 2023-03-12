<template>
  <!-- App-Header -->
  <v-app-bar app color="white">
    <!-- Robustar Logo -->
    <a href="index">
      <img src="../../assets/images/brand/logo.png" style="width: 130px" alt="logo" />
    </a>

    <v-spacer></v-spacer>

    <div v-click-outside="onClickOutside">
      <v-btn icon color="primary" @click="toggleTaskspanel" data-test="header-toggle-tasks-panel">
        <v-icon>mdi-format-list-bulleted-type</v-icon>
      </v-btn>
      <TaskPanel v-show="showTaskPanel"></TaskPanel>
    </div>

    <!-- Full screen button -->
    <v-btn icon color="primary" @click="toggleFullscreen">
      <v-icon v-if="!isFullscreen">mdi-fullscreen</v-icon>
      <v-icon v-else>mdi-fullscreen-exit</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import TaskPanel from '@/components/common/TaskPanel';

export default {
  name: 'Header',
  components: {
    TaskPanel,
  },
  data() {
    return {
      isFullscreen: false,
      showTaskPanel: false,
    };
  },
  methods: {
    toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
      this.isFullscreen = !this.isFullscreen;
    },
    toggleTaskspanel() {
      this.showTaskPanel = !this.showTaskPanel;
    },
    onClickOutside() {
      if (this.showTaskPanel == true) {
        this.showTaskPanel = false;
      }
    },
  },
};
</script>

<style>
@import './Header.css';
</style>
