<template>
  <v-navigation-drawer app v-model="drawer" :mini-variant.sync="mini" permanent class="pt-4">
    <v-list-item class="px-2">
      <v-spacer v-if="!mini"></v-spacer>
      <v-btn v-if="!mini" icon @click.stop="mini = !mini">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn v-else icon @click.stop="mini = !mini">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav>
      <!-- first level -->
      <div v-for="(item, i) in items" :key="i">
        <v-list-item v-if="!item.children" color="primary" :to="{ path: '/' + item.link }">
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title> </v-list-item-content
        ></v-list-item>
        <v-list-group v-else :value="false" :prepend-icon="item.icon">
          <template v-slot:activator>
            <v-list-item-title>{{ item.text }}</v-list-item-title>
          </template>
          <!-- second level -->
          <div v-for="(child, i) in item.children" :key="i">
            <v-list-item v-if="!child.children" color="primary" :to="{ path: '/' + child.link }">
              <v-list-item-icon>
                <v-icon v-text="child.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="child.text"></v-list-item-title> </v-list-item-content
            ></v-list-item>
            <v-list-group v-else :value="true" no-action sub-group>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title>{{ child.text }}</v-list-item-title>
                </v-list-item-content>
              </template>
              <!-- third level -->
              <v-list-item
                v-for="(desc, i) in child.children"
                :key="i"
                :to="{ path: '/' + desc.link }"
              >
                <v-list-item-subtitle v-text="desc.text"></v-list-item-subtitle>
              </v-list-item>
            </v-list-group>
          </div>
        </v-list-group>
      </div>

      <!-- Module 1: Training -->
      <!-- <v-list-item @click="navigateTo('/train-pad')">
        <v-list-item-icon @click="changewindow">
          <v-icon class="side-bar-level1-icon">mdi-chart-line</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          <div class="side-bar-level1-title">
            <span>Train</span>
          </div>
        </v-list-item-title>
      </v-list-item> -->

      <!-- Module 2: Annotate -->
      <!-- <v-list-item @click="navigateTo('/edit')">
        <v-list-item-icon @click="changewindow">
          <v-icon class="side-bar-level1-icon">mdi-bookmark</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          <div class="side-bar-level1-title">
            <span>Annotate</span>
          </div>
        </v-list-item-title>
      </v-list-item> -->

      <!-- Module 3: Inspect data -->
      <!-- <v-list-group :value="!mini && true" prepend-icon="mdi-eye" eager @click="changewindow">
        <template v-slot:activator>
          <v-list-item-title class="side-bar-level1-title"> Inspect Data </v-list-item-title>
        </template> -->

      <!-- Inspect training data -->
      <!-- <v-list-item class="side-bar-level2-title" @click="navigateTo('/image-list/train')">
          <v-list-item-title>
            <div class="side-bar-level1-title">
              <span>Training Data</span>
            </div>
          </v-list-item-title>
        </v-list-item> -->

      <!-- Inspect validation data -->
      <!-- <v-menu open-on-hover right offset-x="true">
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
        </v-menu> -->

      <!-- Inspect test data -->
      <!-- <v-menu open-on-hover right offset-x="true">
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
      </v-list-group> -->

      <!-- Module 4: Generate Paired Data -->
      <!-- <v-list-item @click="navigateTo('/generate')">
        <v-list-item-icon @click="changewindow">
          <v-icon class="side-bar-level1-icon">mdi-file-document-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          <div class="side-bar-level1-title">
            <span>Generate</span>
          </div>
        </v-list-item-title>
      </v-list-item> -->
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      mini: false,
      items: [
        { text: 'Train', icon: 'mdi-chart-line', link: 'train-pad' },
        { text: 'Annotate', icon: 'mdi-bookmark', link: 'edit' },
        {
          text: 'Inspect Data',
          icon: 'mdi-eye',
          children: [
            { text: 'Training Data', icon: '', link: 'image-list/train' },
            {
              text: 'Validation Data',
              icon: '',
              children: [{ text: 'Correctly Classified' }, { text: 'Incorrectly Classified' }],
            },
            {
              text: 'Test Data',
              icon: '',
              children: [{ text: 'Correctly Classified' }, { text: 'Incorrectly Classified' }],
            },
          ],
        },
        { text: 'Generate', icon: 'mdi-file-document-outline', link: 'generate' },
      ],
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
    // this.mini = this.f_mini;
    // this.changewindow();
  },
  watch: {
    // mini(newVal) {
    //   console.log(newVal);
    //   this.f_mini_return = this.mini;
    //   console.log('show-mini', newVal);
    //   console.log('show-mini-re', this.f_mini_return);
    // },
  },
};
</script>

<style>
/* @import './SideBar.css'; */

/* li a {
  text-decoration: none;
} */

/* #nav {
  padding: 30px;
} */

/* #nav a {
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
} */
</style>
