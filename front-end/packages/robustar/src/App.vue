<template>
  <v-app>
    <Header></Header>
    <SideBar></SideBar>

    <v-main class="page-content">
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

export default {
  name: 'App',
  components: {
    Header,
    SideBar,
    Notification,
  },
};
</script>

<style>
/* global css here */

#app,
.page-content {
  position: relative;
  min-height: 100%;
  width: 100%;
}

.v-btn {
  text-transform: none !important;
}
</style>
