<template>
  <div class="about">
    <!-- <PredView :dataArr="predDataArr" :config="predViewConfig" style="padding-left: 500px" /> -->

    <div v-for="(url, index) in predImgUrl" :key="index" style="padding-left: 500px">
      <img :src="url" style="width: 100px" />
    </div>
  </div>
</template>

<script>
// import PredView from '@/components/prediction-viewer/PredView.vue';
import { APIPredict } from '@/apis/predict';
import { configs } from '@/configs.js';

export default {
  components: { PredView },
  data() {
    return {};
  },
  props: { ImgUrl: Array },

  methods: {},
};
