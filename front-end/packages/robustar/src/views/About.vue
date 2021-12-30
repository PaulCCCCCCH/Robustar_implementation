<template>
  <div class="about">
    <h1>This is an about page</h1>
    <img alt="Vue logo" src="../assets/logo.png" />
    <v-btn depressed color="primary" class="mx-auto" @click="view_prediction('train', '0')">
      testPredictionViewer /train/0
    </v-btn>
    <v-btn depressed color="primary" class="mx-auto" @click="view_prediction('train', '2000')">
      test /train/2000
    </v-btn>
    <v-btn depressed color="primary" class="mx-auto" @click="view_prediction('train', '4000')">
      test /train/4000
    </v-btn>
    <v-btn depressed color="primary" class="mx-auto" @click="view_prediction('test', '100')">
      test /test/100
    </v-btn>

    <PredView :dataArr="predDataArr" :config="predViewConfig" style="padding-left: 500px" />

    <div v-for="(url, index) in predImgUrl" :key="index" style="padding-left: 500px">
      <img :src="url" style="width: 100px" />
    </div>

    <v-btn depressed color="primary" class="mx-auto" @click="get_influence('test', '0')">
      influ: test/0
    </v-btn>

    <v-btn depressed color="primary" class="mx-auto" @click="get_influence('test', '1')">
      influ: test/1
    </v-btn>

    <v-btn depressed color="primary" class="mx-auto" @click="get_influence('test', '2')">
      influ: test/2
    </v-btn>

    <v-btn depressed color="primary" class="mx-auto" @click="get_influence('test', '30')">
      influ: test/30
    </v-btn>

    <div v-for="(url, index) in influImgUrl" :key="index" style="padding-left: 500px">
      <img :src="url" style="width: 100px" />
    </div>
  </div>
</template>

<script>
import PredView from '@/components/prediction-viewer/PredView.vue';
import { APIPredict, APIGetInfluenceImages } from '@/apis/predict';
import { configs } from '@/configs.js';

export default {
  components: { PredView },
  data() {
    return {
      predDataArr: [
        ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
      ],
      predImgUrl: [],
      influImgUrl: [],
      predViewConfig: {
        componentWidth: 300,
        figHeight: 200,
        figWidth: 200,
        // posColor: "#234567",
        // negColor: "#67891a",
        // lineColor: "#abcedf",
        dataRange: [0, 1],
      },
      configs: configs,
    };
  },
  methods: {
    view_prediction(split, imageId) {
      const success = (response) => {
        let responseData = response.data.data;
        this.predDataArr = [responseData[0], responseData[1]];
        this.predImgUrl = [];
        for (let i = 0; i < 4; i++) {
          this.predImgUrl.push(`${configs.serverUrl}/visualize` + responseData[2][i]);
        }
        // console.log(responseData);
        // console.log(this.predDataArr);
        // console.log(this.predImgUrl);
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      // console.log(split);
      // console.log(imageId);
      // console.log(`predict/${split}/${imageId}`);
      APIPredict(split, imageId, success, failed);
    },
    get_influence(split, imageId) {
      const success = (response) => {
        // If influence not predicted:
        if (response.data.code == -1) {
          this.influImgUrl = [];
          return;
        }

        const responseData = response.data.data;
        this.influImgUrl = [];
        for (let i = 0; i < 4; i++) {
          const url = responseData[i];
          this.influImgUrl.push(`${configs.serverUrl}/dataset/${url}`);
        }
      };

      const failed = (err) => {
        console.log(err);
      };

      APIGetInfluenceImages(split, imageId, success, failed);
    },
  },
};
</script>

<style></style>
