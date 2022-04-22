<template>
  <v-app>
    <Header @toggleTaskspanel="toggleTaskspanel"></Header>
    <SideBar></SideBar>

    <v-main class="page-content">
      <TaskPanel v-if="!isTaskspanelHidden"></TaskPanel>
      <Notification></Notification>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
// import io from 'socket.io-client';
import Header from '@/components/common/Header';
import SideBar from '@/components/common/SideBar';
import Notification from '@/components/common/Notification';
import TaskPanel from '@/components/common/TaskPanel';

export default {
  name: 'App',
  components: {
    Header,
    SideBar,
    Notification,
    TaskPanel,
  },
  methods: {
    toggleTaskspanel() {
      this.isTaskspanelHidden = !this.isTaskspanelHidden;
    },
  },
  data() {
    return {
      isTaskspanelHidden: true,
    };
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

.v-btn {
  text-transform: none !important;
}
</style>
