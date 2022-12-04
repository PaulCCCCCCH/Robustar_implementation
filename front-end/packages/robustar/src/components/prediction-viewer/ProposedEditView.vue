<template>
  <!-- Two colums of visualizations -->
  <!-- Flash torch visualizations -->
  <div class="d-flex flex-row align-center justify-center">
    <v-img :src="proposedEditBase64" max-height="30vh" max-width="30vh" />
  </div>
</template>

<script>
export default {
  props: {
    proposedEditBase64: String,
  },
};
</script>
