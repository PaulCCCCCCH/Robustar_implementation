<template>
  <v-app>
    <v-app-bar app color="white">
      <!-- Robustar Logo -->
      <a href="index">
        <img src="./assets/images/brand/logo.png" style="width: 130px" alt="logo" />
      </a>

      <v-spacer></v-spacer>

      <!-- Full screen button -->
      <v-btn icon color="primary" @click="toggleTaskspanel">
        <v-icon>mdi-format-list-bulleted-type</v-icon>
      </v-btn>
      <v-btn icon color="primary" @click="toggleFullscreen">
        <v-icon v-if="!isFullscreen">mdi-fullscreen</v-icon>
        <v-icon v-else>mdi-fullscreen-exit</v-icon>
      </v-btn>
    </v-app-bar>

    <SideBar></SideBar>

    <v-main class="page-content">
      <v-row v-if="!isTaskspanelHidden" align="center" justify="center">
        <v-col cols="12" lg="6"></v-col>
        <v-col cols="12" lg="6">

        <v-card
          style="position:fixed; width: 40%; z-index:10; padding-top:3rem; padding-bottom: 3rem; align: center;"
          elevation="4"
        >
          <v-row v-for="(item, index) in digest" align="center" justify="center">
              <v-col cols="12" lg="1" align="center" justify="center">
                <v-btn color="red" icon><v-icon>mdi-minus-box</v-icon></v-btn>
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



            <v-col cols="12" lg="3" align="center" justify="center">Training</v-col>
            <v-col cols="12" lg="6" align="center" justify="center">
              <v-row align="center" justify="center">
                <v-col cols="12" v-bind:lg="training" style="padding-left:0; padding-right:0;">
                  <v-progress-linear
                    color="primary"
                    height="4"
                    indeterminate
                    buffer-value="100"
                  ></v-progress-linear>
                </v-col>
                <v-col cols="12" v-bind:lg="nonTraining" style="padding-left:0; padding-right:0;">
                  <v-progress-linear
                    color="secondary"
                    height="4"
                    buffer-value="100"
                  ></v-progress-linear>
                </v-col>
              </v-row>
            </v-col align="center" justify="center">
            <v-col cols="12" lg="3">Time left</v-col>
          </v-row>
        
        </v-card>
        
        </v-col>
      </v-row>

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
  data() {
    return {
      isFullscreen: false,
      isTaskspanelHidden: true,
      training: 6,
      nonTraining: 6,
      progress: 50,
      // socket: io('wss://localhost:8000/'),
      digest: [],
    };
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
      this.isTaskspanelHidden = !this.isTaskspanelHidden;
    }
  },
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
