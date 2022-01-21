<template>
  <!-- Two colums of visualizations -->
    <!-- Flash torch visualizations -->
    <div class="d-flex flex-row align-center justify-center">
      <div v-for="(url, index) in focusImgUrl" :key="index">
        <img :src="url" style="width: 15vh" />
      </div>
    </div>
</template>

<script>
import { getImageUrlFromFullUrl } from '@/utils/image_utils';

export default {
  props: {
    focusImgUrl: Array,
  },
  methods: {
    gotoImage(url) {
      console.log(url);
      const [image_id, split] = getImageUrlFromFullUrl(url);
      localStorage.setItem('split', split);
      localStorage.setItem('image_id', image_id);
      localStorage.setItem('image_url', url);
      this.$router.push({ name: 'EditImage' });
    },
  },
};
</script>
