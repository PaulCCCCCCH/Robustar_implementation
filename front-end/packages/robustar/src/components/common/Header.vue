<template>
  <!-- App-Header -->
  <v-app-bar app color="white">
    <!-- Robustar Logo -->
    <a href="index">
      <img src="../../assets/images/brand/logo.png" style="width: 130px" alt="logo" />
    </a>

    <v-spacer></v-spacer>

    <!-- Full screen button -->
    <v-btn icon color="primary" @click="toggleTaskspanel" data-test="header-toggle-tasks-panel">
      <v-icon>mdi-format-list-bulleted-type</v-icon>
    </v-btn>
    <v-btn icon color="primary" @click="toggleFullscreen">
      <v-icon v-if="!isFullscreen">mdi-fullscreen</v-icon>
      <v-icon v-else>mdi-fullscreen-exit</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header',

  props: {
    isTaskspanelHidden: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      isFullscreen: false,
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
      this.$emit('toggleTaskspanel');
    },
  },
};
</script>

<style>
@import './Header.css';
</style>
