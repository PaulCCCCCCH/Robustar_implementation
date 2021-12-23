<template>
  <div class="about">
    <PredView :dataArr="predDataArr" :config="predViewConfig" style="padding-left: 500px" />
    <Visualizer :ImgUrl="predImgUrl" style="padding-left: 500px">
    </div>
</template>

<script>
import PredView from '@/components/prediction-viewer/PredView.vue';
import Visualizer from '../components/prediction-viewer/Visualizer.vue';
import { APIPredict } from '@/apis/predict';
import { configs } from '@/configs.js';

export default {
  components: { PredView, Visualizer },
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
  mounted() {
    this.view_prediction(split, image_id);
  },
  methods: {
    view_prediction(split, image_id) {
      const success = (response) => {
        let responseData = response.data.data;
        const split = localStorage.getItem('split');
        const image_id = localStorage.getItem('image_id');
        this.predDataArr = [responseData[0], responseData[1]];
        this.predImgUrl = [];
        for (let i = 0; i < 4; i++) {
          this.predImgUrl.push(`${configs.serverUrl}/visualize` + responseData[2][i]);
        }
        console.log(success);
        console.log(split);
        console.log(responseData);
        console.log(image_id);
        console.log(this.predDataArr);
        console.log(this.predImgUrl);
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
