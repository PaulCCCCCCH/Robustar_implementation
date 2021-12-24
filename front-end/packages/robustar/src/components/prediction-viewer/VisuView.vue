<template>
    <!-- Two colums of visualizations -->
    <div class='d-flex flex-row justify-space-around'>

      <!-- Flash torch visualizations -->
      <div class="d-flex flex-column align-center">
        <div v-for="(url, index) in predImgUrl" :key="index">
          <img :src="url" style="width: 15vh" />
        </div>
      </div>

      <!-- Influence functions (if calculated) -->
      <div class="d-flex flex-column align-center">
        <div v-if="influImgUrl.length === 0">
          <h1>Influence</h1>
          <h1>Not </h1>
          <h1>Available</h1>
        </div>
        <div v-else>
          <div v-for="(url, index) in influImgUrl" :key="index">
            <img :src="url" style="width: 15vh" />
          </div>
        </div>
      </div>
  </div>
</template>

<script>

export default {
  props: {
    predImgUrl: Array,
    influImgUrl: Array
  },
};
</script>