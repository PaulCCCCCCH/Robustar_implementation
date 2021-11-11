<template>
  <div class="about">
    <h1>This is an about page</h1>
    <img alt="Vue logo" src="../assets/logo.png">
    <button type="button" class="btn btn-primary"> mybutton </button>

    <div>
      <PredView :dataArr="predDataArr" :config="predViewConfig"/>
    </div>
  </div>
</template>


<script>
import PredView from "@/components/predictionView/PredView.vue";

export default {
  components: { PredView },
  data() {
    return {
      predDataArr: [["bird", 5], ["cat", 10], ["crab", -3], ["dog", 50], ["fish", 20], 
                    ["frog", -20], ["insect", -49], ["primate", 20], ["turtle", 15]],
      predViewConfig: {
        figHeight: 500,
        figWidth: 500,
      },
    }
  }
}
</script>

<style>
</style>