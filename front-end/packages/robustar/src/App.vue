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
        <v-row align="center" justify="center">
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
    };
  },
  // created: function() {
  //   console.log("Starting connection to WebSocket Server")
  //   this.connection = new WebSocket("http://localhost:5000")

  //   this.connection.onmessage = function(event) {
  //     console.log(event);
  //   }

  //   this.connection.onopen = function(event) {
  //     console.log(event)
  //     console.log("Successfully connected to the echo websocket server...")
  //   }
  // },
  methods: {
    // updatewindow: function (is_mini_side_bar) {
    //   const page_content = document.getElementById('page-content');
    //   if (!page_content) {
    //     return;
    //   }

    //   if (is_mini_side_bar) {
    //     page_content.style.width = screen.width - 56 + 'px';
    //   } else {
    //     page_content.style.width = screen.width - 256 + 'px';
    //   }
    // },
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
