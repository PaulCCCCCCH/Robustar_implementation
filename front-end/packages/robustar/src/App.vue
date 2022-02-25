<template>
  <v-app>
    <v-app-bar app color="white">
      <!-- Robustar Logo -->
      <a href="index">
        <img src="./assets/images/brand/logo.png" style="width: 130px" alt="logo" />
      </a>

      <v-spacer></v-spacer>

      <!-- Full screen button -->
      <v-btn icon color="primary" @click="toggleFullscreen">
        <v-icon v-if="!isFullscreen">mdi-fullscreen</v-icon>
        <v-icon v-else>mdi-fullscreen-exit</v-icon>
      </v-btn>
    </v-app-bar>

    <SideBar></SideBar>

    <v-main class="page-content">
      <Notification></Notification>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Header from '@/components/common/Header';
import SideBar from '@/components/common/SideBar';
import Notification from '@/components/common/Notification';

export default {
  name: 'App',
  components: {
    Header,
    SideBar,
    Notification,
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
  },
};
</script>

<style>
/* global css here */

#app,
.page-content {
  min-height: 100%;
  width: 100%;
}
</style>
