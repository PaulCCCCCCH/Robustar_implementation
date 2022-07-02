<template>
  <!-- Two colums of visualizations -->
  <!-- Flash torch visualizations -->
  <div class="d-flex flex-row align-center">
    <div v-for="(url, index) in focusImgUrl" :key="index">
      <img :src="url" style="width: 10vw" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    focusImgUrl: Array,
  },
};
</script>
