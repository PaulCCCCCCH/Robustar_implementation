<template>
  <div class="container">
    <div class="view-home">
      <br />
      <h1 data-test="home-page-welcome-msg">Start your exploration!</h1>
      <br /><br />
      <div class="d-flex flex-wrap justify-space-around">
        <div class="feature-item" v-for="(item, i) in items" :key="i">
          <v-list-item
            :data-test="`home-${item.text}-entrance`"
            :to="{ path: '/' + item.link }"
            class="d-flex align-start"
          >
            <div>
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>
            </div>
            <div>
              <v-list-item-content
                class="font-weight-medium"
                v-text="item.text"
              ></v-list-item-content>
              <v-list-item-content v-text="item.explain"></v-list-item-content>
            </div>
          </v-list-item>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  name: 'Home',
  data() {
    return {
      items: [
        {
          icon: 'mdi-chart-line',
          link: 'train-pad',
          text: 'Train',
          explain: 'The model can be trained elsewhere then fed into the software',
        },
        {
          icon: 'mdi-vector-link',
          link: 'influence-pad',
          text: 'Influence',
          explain:
            ' With new test samples, the model can help identify the samples that are responsible for the prediction through influence function',
        },
        {
          icon: 'mdi-cogs',
          link: 'image-list/train',
          text: 'Predict',
          explain:
            'The software offers saliency map to help the user know which part of the features the model are paying necessary attention',
        },
        {
          icon: 'mdi-draw',
          link: 'image-list/train',
          text: 'Annotate',
          explain: 'The users can use the drawing tools to brush out the superficial pixels',
        },
      ],
    };
  },
  methods: {
    navigateTo(path) {
      if (this.$route.path != path) {
        this.$router.push(path);
      }
    },
  },
};
</script>

<style scoped>
.feature-item {
  height: auto;
  width: 45%;
  padding: 20px 30px;
  margin: 5px;
  border-radius: 10px;
  background-color: #fff;
  text-align: left;
}
.container {
  text-align: center;
}
</style>
