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
      const [image_id, split] = getImageUrlFromFullUrl(url);
      sessionStorage.setItem('split', split);
      sessionStorage.setItem('image_id', image_id);
      sessionStorage.setItem('image_url', url);
      sessionStorage.setItem('save_image_id', split);
      sessionStorage.setItem('save_image_split', image_id);
      this.$router.push({ name: 'EditImage', params: { mode: split } });
    },
  },
};
</script>
