<template>
  <div id="app">
    <v-app id="inspire">

    <Header />
      <div class="pages">
        <SideBar :f_mini="f_mini" :f_mini_return="f_mini_return" @updatewindow="updatewindow"></SideBar>

        <div id="page-content">
          <router-view />
        </div>
      </div>
    </v-app>
  </div>
</template>


<script>
import Header from "@/components/common/Header.vue";
import SideBar from "@/components/common/SideBar.vue";
export default {
  name: "App",
  components: {
    Header,
    SideBar,
  },
  data() {
    return {
      f_mini: true,
      f_mini_return:false,
    }
  },
  methods: {
    updatewindow: function(f_mini_return){
      if(f_mini_return==true){
        document.getElementById("page-content").style.width = (screen.width - 256) + "px";
      }
      else{
        document.getElementById("page-content").style.width = (screen.width - 56) + "px";
      }
    },
  },
  mounted () {
    this.updatewindow(true)
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.pages{
  margin: 0px 0px 0px 40px;
  height: 100%;
  float: right;
}
</style>