<template>
  <!-- Two colums of visualizations -->
  <div class="d-flex flex-row justify-space-around" style="padding: 20px">
    <!-- Flash torch visualizations -->
    <div class="d-flex flex-column align-center" style="margin-right: 20px">
      <h2>Model focus</h2>
      <div v-for="(url, index) in predImgUrl" :key="index">
        <img :src="url" style="width: 15vh" />
      </div>
    </div>

    <!-- Influence functions (if calculated) -->
    <div class="d-flex flex-column align-center">
      <h2>Influence Images</h2>
      <div v-if="influImgUrl.length === 0">
        <h1>Influence</h1>
        <h1>Not</h1>
        <h1>Available</h1>
      </div>
      <div v-else>
        <div v-for="(url, index) in influImgUrl" :key="index">
          <button @click="() => gotoImage(url)">
            <img :src="url" style="width: 15vh" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getImageUrlFromFullUrl } from '@/utils/image_utils';

export default {
  props: {
    predImgUrl: Array,
    influImgUrl: Array,
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
