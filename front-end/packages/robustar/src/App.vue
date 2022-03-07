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
  // sockets: {
  //   connect(){
  //     console.log('connect');
  //   },
  //   afterConnect(data){
  //     console.log(data);
  //   },

  //   // get digest from backend
  //   digest(data){
  //     this.digest = data.digest;
  //   },
  // },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #eee;
}

.pages {
  margin: 0px 0px 0px 40px;
  height: 100%;
  float: right;
}

#app,
.page-content {
  min-height: 100%;
  width: 100%;
}

body::-webkit-scrollbar {
  display: none !important;
}
</style>
