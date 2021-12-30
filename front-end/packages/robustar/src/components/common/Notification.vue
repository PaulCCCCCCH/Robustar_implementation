<template>
  <div>
    <v-overlay :value="$root.processing" opacity="0.7">
      <v-progress-circular indeterminate size="30" class="mr-4"></v-progress-circular>
      <span style="vertical-align: middle">
        {{ $root.processingMsg }}
      </span>
    </v-overlay>

    <!-- succeeded -->
    <v-snackbar
      rounded
      dark
      right
      v-model="$root.success"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">{{ $root.successMsg }}</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="accent" text v-bind="attrs" @click="$root.success = false"> Close </v-btn>
      </template>
    </v-snackbar>

    <!-- failed -->
    <v-snackbar
      rounded
      dark
      right
      v-model="$root.error"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">{{ $root.errorMsg }}</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="$root.error = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  mounted() {
    // setInterval(() => {
    //   console.log(this.$processing);
    // }, 300);
  },
};
</script>

<style scoped>
</style>