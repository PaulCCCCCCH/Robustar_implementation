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
      <div v-for="item in items" :key="item.text" class="mb-2">
        <v-list-item v-if="!item.children" color="primary" :to="{ path: '/' + item.link }">
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title> </v-list-item-content
        ></v-list-item>
        <v-list-group v-else :value="isGroupActive" :prepend-icon="item.icon" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </template>

          <!-- second level -->
          <div v-for="child in item.children" :key="child.text">
            <v-list-item v-if="!child.children" color="primary" :to="{ path: '/' + child.link }">
              <v-list-item-icon>
                <v-icon v-text="child.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="child.text"></v-list-item-title> </v-list-item-content
            ></v-list-item>
            <v-list-group v-else no-action sub-group>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title>{{ child.text }}</v-list-item-title>
                </v-list-item-content>
              </template>
              <!-- third level -->
              <v-list-item v-if="!item.children" color="primary" :to="{ path: '/' + item.link }">
                <v-list-item-icon>
                  <v-icon v-text="item.icon"></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title v-text="item.text"></v-list-item-title> </v-list-item-content
              ></v-list-item>
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title v-text="item.text"></v-list-item-title>
                </v-list-item-content>
              </template>

              <!-- fourth level -->
              <v-list-item
                v-for="desc in child.children"
                :key="desc.text"
                :to="{ path: '/' + desc.link }"
              >
                <v-list-item-subtitle v-text="desc.text"></v-list-item-subtitle>
              </v-list-item>
            </v-list-group>
          </div>
        </v-list-group>
      </div>
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
        { text: 'Annotate', icon: 'mdi-draw', link: 'edit' },
        { text: 'Models', icon: 'mdi-function-variant', link: 'model' },
        { text: 'Influence', icon: 'mdi-vector-link', link: 'influence-pad' },
        {
          text: 'Inspect Data',
          icon: 'mdi-eye',
          children: [
            { text: 'Training Data', icon: '', link: 'image-list/train' },
            { text: 'Annotated Data', icon: '', link: 'image-list/annotated' },
            {
              text: 'Validation Data',
              icon: '',
              link: 'image-list/validation',
            },
            {
              text: 'Test Data',
              icon: '',
              link: 'image-list/test',
            },
          ],
        },
        { text: 'Test', icon: 'mdi-code-braces', link: 'test' },
        { text: 'Auto Annotate', icon: 'mdi-auto-fix', link: 'auto-annotate' },
        { text: 'Config', icon: 'mdi-file-table-box', link: 'config' },
        { text: 'About', icon: 'mdi-information', link: 'about' },
      ],
    };
  },
  computed: {
    isGroupActive() {
      return this.$route.path.startsWith('/image-list/');
    },
  },
};
</script>
