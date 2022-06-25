<template>
  <!-- Influence functions (if calculated) -->
  <div class="d-flex flex-column align-center">
    <div v-if="influImgUrlList.length === 0">
      <p>Influence not calculated.</p>

      <div v-if="split === 'test'">
        <v-btn
          depressed
          color="primary"
          @click="
            $router.push({
              name: 'InfluencePad',
              params: {},
            })
          "
        >
          Calculate Influence
        </v-btn>
      </div>
    </div>
    <div v-else>
      <div v-for="(url, index) in influImgUrl" :key="index">
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

export default {
  props: {
    influImgUrlList: Array,
    victimUrl: String,
    split: String,
  },
  data() {
    return {};
  },
  methods: {
    gotoImage(url) {
      sessionStorage.setItem('split', 'train');
      sessionStorage.setItem('image_url', getImageUrlFromFullUrl(url));
      this.$router.push({ name: 'EditImage', params: { split: 'train' } });
    },
    calculateInfluence() {
      APICalculateInfluence(
        {
          test_sample_start_idx: -1,
          test_sample_end_idx: -1, // Don't need to specify start/end for instance influence calculation
          r_averaging: 1, // TODO: Read from session storage
          is_batch: false, // not batch calculation
        },
        () => {},
        () => {} // TODO
      );
    },
  },
};
</script>
