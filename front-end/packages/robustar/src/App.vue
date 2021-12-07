<template>
  <div id="app">
    <v-app id="inspire">
      <Header />
      <div class="pages">
        <SideBar
          @updatewindow="updatewindow"
        ></SideBar>

        <div id="page-content">
          <router-view />
        </div>
      </div>
    </v-app>
  </div>
</template>

<script>
import Header from '@/components/common/Header';
import SideBar from '@/components/common/SideBar';

export default {
  name: 'App',
  components: {
    Header,
    SideBar,
  },
  data() {
    return {
    };
  },
  methods: {
    updatewindow: function (is_mini_side_bar) {
      const page_content = document.getElementById('page-content')
      if (!page_content) {
        return
      }

      if (is_mini_side_bar) {
        page_content.style.width = screen.width - 56 + 'px';
      } else {
        page_content.style.width = screen.width - 256 + 'px';
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.pages {
  margin: 0px 0px 0px 40px;
  height: 100%;
  float: right;
}

#app,
#page-content {
  height: 100%;
}
</style>
