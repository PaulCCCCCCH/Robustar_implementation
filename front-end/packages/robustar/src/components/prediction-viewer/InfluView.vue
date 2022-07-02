<template>
  <!-- Influence functions (if calculated) -->
  <div class="d-flex flex-column align-center">
    <div v-if="influImgUrlList.length === 0">
      <p>Influence not calculated.</p>

      <div v-if="split === 'test'">
        <v-btn depressed color="primary" @click="calculateInfluence"> Calculate Influence </v-btn>
        <p>Current config: r_averaging: {{ r_averaging }}</p>
      </div>
    </div>
    <div class="d-flex flex-row align-center justify-center" v-else>
      <div v-for="(url, index) in influImgUrlList" :key="index">
        <button @click="() => gotoImage(url)">
          <img :src="url" style="width: 15vh" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { getImageUrlFromFullUrl } from '@/utils/imageUtils';
import { APICalculateInfluence } from '@/services/predict';
import { configs } from '@/configs.js';

export default {
  props: {
    influImgUrlList: Array,
    victimUrl: String,
    split: String,
  },
  data() {
    return {
      r_averaging: configs.defaultRAveraging,
    };
  },
  mounted() {
    console.log(this.influImgUrlList)
    this.r_averaging = sessionStorage.getItem('r_averaging') || configs.defaultRAveraging;
  },
  methods: {
    gotoImage(url) {
      sessionStorage.setItem('split', 'train');
      sessionStorage.setItem('image_url', getImageUrlFromFullUrl(url));
      this.$router.push({ name: 'EditImage', params: { split: 'train' } });
    },
    calculateInfluence() {
      this.$root.startProcessing('The influence is being calculated. Please wait...');
      const success = (response) => {
        this.$root.finishProcessing();
        this.$root.alert('success', 'Influence calculation succeeded');
      };
      const failed = (err) => {
        alert('Server error. Check console.');
        this.$root.finishProcessing();
        this.$root.alert('error', 'Influence calculation failed');
      };

      APICalculateInfluence(
        {
          configs: {
            test_sample_start_idx: -1,
            test_sample_end_idx: -1, // Don't need to specify start/end for instance influence calculation
            r_averaging: this.r_averaging, // TODO: Read from session storage
            is_batch: false, // not batch calculation
            instance_path: this.victimUrl, // only calculate influence for this image
          },
        },
        success,
        failed
      );
    },
  },
};
</script>
