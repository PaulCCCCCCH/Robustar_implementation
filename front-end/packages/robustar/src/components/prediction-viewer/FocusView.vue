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
export default {
  props: {
    focusImgUrl: Array,
  },
};
</script>
