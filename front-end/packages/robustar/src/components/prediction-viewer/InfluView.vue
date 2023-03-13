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
          <img :src="toFullImgUrl(url)" style="width: 15vh" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { configs } from '@/configs.js';

export default {
  props: {
    influImgUrl: Array,
  },
  methods: {
    gotoImage(url) {

      this.$root.imageURL = url;
      this.$root.imageSplit = 'train';
      this.$root.imageURL = url;
      this.$router.push({ name: 'ImageAnnotation' });
    },
    toFullImgUrl(url) {
      return `${configs.imagePathServerUrl}?${configs.imagePathParamName}=${url}`;
    }
  },
};
</script>
