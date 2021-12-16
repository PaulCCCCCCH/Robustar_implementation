<template>
  <div class="about">
    <h1>This is an about page</h1>
    <img alt="Vue logo" src="../assets/logo.png" />
    <button type="button" class="btn btn-primary">mybutton</button>
    <button type="button" class="btn btn-primary" @click="view_prediction('train', '0')">
      testPredictionViewer /train/0
    </button>
    <button type="button" class="btn btn-primary" @click="view_prediction('train', '2000')">
      test /train/2000
    </button>
    <button type="button" class="btn btn-primary" @click="view_prediction('train', '4000')">
      test /train/4000
    </button>
    <button type="button" class="btn btn-primary" @click="view_prediction('test', '100')">
      test /test/100
    </button>

    <PredView :dataArr="predDataArr" :config="predViewConfig" style="padding-left: 500px" />

    <div v-for="(url, index) in predImgUrl" :key="index" style="padding-left: 500px">
      <img :src="url" style="width: 100px" />
    </div>
  </div>
</template>

<script>
import PredView from '@/components/prediction-viewer/PredView.vue';
import { APIPredict } from '@/apis/predict';
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
  },
};
</script>

<style></style>
