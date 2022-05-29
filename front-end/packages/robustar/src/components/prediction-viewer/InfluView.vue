<template>
  <!-- Influence functions (if calculated) -->
  <div class="d-flex flex-column align-center">
    <div v-if="influImgUrl.length === 0">
      <p>Influence not calculated.</p>
      <p>To calculate influence</p>
      <p>please go to Influence page from the side bar</p>
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

export default {
  props: {
    influImgUrl: Array,
  },
  methods: {
    gotoImage(url) {
      sessionStorage.setItem('split', 'train');
      sessionStorage.setItem('image_url', getImageUrlFromFullUrl(url));
      this.$router.push({ name: 'EditImage', params: { split: "train"} });
    },
  },
};
</script>
