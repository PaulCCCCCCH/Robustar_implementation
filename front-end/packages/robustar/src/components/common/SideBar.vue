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
        { text: 'Influence', icon: 'mdi-vector-link', link: 'influence-pad' },
        {
          text: 'Inspect Data',
          icon: 'mdi-eye',
          children: [
            { text: 'Training Data', icon: '', link: 'image-list/train' },
            {
              text: 'Validation Data',
              icon: '',
              children: [
                { text: 'Correctly Classified', link: 'image-list/validation_correct' },
                { text: 'Incorrectly Classified', link: 'image-list/validation_incorrect' },
              ],
            },
            {
              text: 'Test Data',
              icon: '',
              children: [
                { text: 'Correctly Classified', link: 'image-list/test_correct' },
                { text: 'Incorrectly Classified', link: 'image-list/test_incorrect' },
              ],
            },
          ],
        },
        { text: 'Test', icon: 'mdi-code-braces', link: 'test' },
        { text: 'About', icon: 'mdi-information', link: 'about' },
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
};
</script>
