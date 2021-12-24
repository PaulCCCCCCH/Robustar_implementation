<template>
  <div class="d-flex flex-column justify-center align-center" style='width: 30vw'>
    <!-- View the prediction-->
    <PredView :dataArr="predDataArr" :config="predViewConfig" />
    <VisuView :influImgUrl="influImgUrl" :predImgUrl="predImgUrl" /> 
  </div>
</template>

<script>
import PredView from '@/components/prediction-viewer/PredView.vue';
import VisuView from '@/components/prediction-viewer/VisuView.vue';
import { APIPredict, APIGetInfluenceImages } from '@/apis/predict';
import { configs } from '@/configs.js';

export default {
  components: { PredView, VisuView },
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
        figHeight: 300,
        figWidth: 300,
        // posColor: "#234567",
        // negColor: "#67891a",
        // lineColor: "#abcedf",
        dataRange: [0, 1],
      },
      configs: configs,
    };
  },

  mounted() {
    const split = localStorage.getItem('split');
    const image_id = localStorage.getItem('image_id');
    this.view_prediction(split, image_id)
    this.get_influence(split, image_id)
  },
  methods: {
    view_prediction(split, image_id) {
      const success = (response) => {
        let responseData = response.data.data;
        this.predDataArr = [responseData[0], responseData[1]];
        this.predImgUrl = [];
        for (let i = 0; i < 4; i++) {
          this.predImgUrl.push(`${configs.serverUrl}/visualize` + responseData[2][i]);
        }
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APIPredict(split, image_id, success, failed);
    },

    get_influence(split, imageId) {
      const success = (response) => {
        // If influence not predicted:
        if (response.data.code == -1) {
          this.influImgUrl = []
          return
        }

        const responseData = response.data.data;
        this.influImgUrl = [];
        for (let i = 0; i < 4; i++) {
          const url = responseData[i]
          this.influImgUrl.push(`${configs.serverUrl}/dataset/${url}`)
        }

      }

      const failed = (err) => {
        console.log(err)
      }

      APIGetInfluenceImages(split, imageId, success, failed)
    }

  },
};
</script>