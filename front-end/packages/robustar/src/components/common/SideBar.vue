<template>
  <div class="side-bar">
    <v-card class="mx-auto" style="height: 100%">
      <v-navigation-drawer
        v-model="drawer"
        :mini-variant.sync="is_mini_side_bar"
        permanent
        style="height: 100%"
      >
        <v-list-item class="px-2">
          <v-btn icon v-if="!is_mini_side_bar" @click="changewindow">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn icon v-if="is_mini_side_bar" @click="changewindow">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>
        <v-list dense>
          <!-- Module 1: Training -->
          <v-list-item @click="navigateTo('/train-pad')">
            <v-list-item-icon>
              <v-icon class="side-bar-level1-icon">mdi-chart-line</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              <div class="side-bar-level1-title">
                <span>Train</span>
              </div>
            </v-list-item-title>
          </v-list-item>

          <!-- Module 2: Annotate -->
          <v-list-item @click="navigateTo('/edit')">
            <v-list-item-icon>
              <v-icon class="side-bar-level1-icon">mdi-bookmark</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              <div class="side-bar-level1-title">
                <span>Annotate</span>
              </div>
            </v-list-item-title>
          </v-list-item>

          <!-- Module 3: Inspect data -->
          <v-list-group prepend-icon="mdi-eye" eager>
            <template v-slot:activator>
              <v-list-item-title class="side-bar-level1-title"> Inspect Data </v-list-item-title>
            </template>

            <!-- Inspect training data -->
            <v-list-item class="side-bar-level2-title" @click="navigateTo('/image-list/train')">
              <v-list-item-title>
                <div class="side-bar-level1-title">
                  <span>Training Data</span>
                </div>
              </v-list-item-title>
            </v-list-item>

            <!-- Inspect validation data -->
            <v-menu open-on-hover right :offset-x="true">
              <template v-slot:activator="{ on, attrs }">
                <v-list-item class="side-bar-level2-title" v-bind="attrs" v-on="on">
                  <v-list-item-title>
                    <div class="side-bar-level1-title">
                      <span>Validation Data</span>
                    </div>
                  </v-list-item-title>
                </v-list-item>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-title> Correctly Classified </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title> Incorrectly Classified </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>

            <!-- Inspect test data -->
            <v-menu open-on-hover right :offset-x="true">
              <template v-slot:activator="{ on, attrs }">
                <v-list-item class="side-bar-level2-title" v-bind="attrs" v-on="on">
                  <v-list-item-title>
                    <div class="side-bar-level1-title">
                      <span>Test Data</span>
                    </div>
                  </v-list-item-title>
                </v-list-item>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-title> Correctly Classified </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title> Incorrectly Classified </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-list-group>
        </v-list>
        <div id="nav">
          <router-link to="/">Home</router-link> |
          <router-link to="/about">About</router-link>
        </div>
      </v-navigation-drawer>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      is_mini_side_bar: false,
    };
  },
  methods: {
    navigateTo(path) {
      if (this.$route.path != path) {
        this.$router.push(path);
      }
    },
    changewindow() {
      this.is_mini_side_bar = !this.is_mini_side_bar;
      this.$emit('updatewindow', this.is_mini_side_bar);
    },
  },
  created() {
    this.changewindow(this.is_mini_side_bar);
  },
};
</script>

<style>
@import './SideBar.css';

li a {
  text-decoration: none;
}

/* #nav {
  padding: 30px;
} */

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#nav {
  position: fixed;
  bottom: 0;
  right: 0;
  float: right;
  margin-right: 10px;
}

.v-list-group__header__append-icon {
  min-width: 24px !important;
}
</style>
