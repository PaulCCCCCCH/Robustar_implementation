<template>
  <div class="about">
    <h1>This is an about page</h1>
    <img alt="Vue logo" src="../assets/logo.png">
    <button type="button" class="btn btn-primary"> mybutton </button>

    <PredView :dataArr="predDataArr" :config="predViewConfig"/>
    
  </div>
</template>


<script>
import PredView from "@/components/prediction-viewer/PredView.vue";

export default {
  components: { PredView },
  data() {
    return {
      // predDataArr: [["bird", 5], ["cat", 10], ["crab", -3], ["dog", 50], ["fish", 20], 
      //               ["frog", -20], ["insect", -50], ["primate", 20], ["turtle", 15]],
      // predDataArr: [["bird", 5], ["cat", 10], ["crab", -3], ["dog", 50], ["fish", 20], 
      //               ["frog", -15], ["insect", -10], ["primate", 20], ["turtle", 15]],
      // predDataArr: [["bird", 5], ["cat", 10], ["crab", -3], ["dog", 5], ["fish", 20], 
      //               ["frog", -50], ["insect", -10], ["primate", 20], ["turtle", 15]],
      predDataArr: [["bird", 5], ["cat", 10], ["crab", 3], ["dog", 50], ["fish", 20], 
                    ["frog", 20], ["insect", 49], ["primate", 20], ["turtle", 15]],
      // predDataArr: [["bird", -5], ["cat", -10], ["crab", -3], ["dog", -50], ["fish", -20], 
      //               ["frog", -20], ["insect", -49], ["primate", -20], ["turtle", -15]],
      // predDataArr: [["bird", 5], ["cat", 10], ["crab", 3], ["dog", 50], ["fish", 20], 
      //               ["frog", 20], ["insect", 49]],
      predViewConfig: {
        componentWidth: 300,
        figHeight: 200,
        figWidth: 200,
        // posColor: "#234567",
        // negColor: "#67891a",
        // lineColor: "#abcedf",
        // dataRange: [-60, 60],
      },
    }
  }
}
</script>

<style>
</style>