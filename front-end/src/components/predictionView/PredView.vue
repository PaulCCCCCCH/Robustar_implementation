<template>
  <div :style="{width:defaultConfig.figWidth+'px', height:defaultConfig.figHeight+'px'}">
    <div
      class="line-chart"
      :style="{background:defaultConfig.lineColor, marginTop:defaultConfig.figHeight/2+'px'}"
    >
      <ul>
        <li v-for="(item, index) in dataArr" :key=index>
          <div
            class="box"
            :class="item[1]>=0?'box-pos':'box-neg'"
            :style="{height:dataPercentageArr[index]*defaultConfig.figHeight/2+'px',
                     background:(item[1]>=0)?defaultConfig.posColor:defaultConfig.negColor,
                     width:defaultConfig.figWidth/(arrLength+2)+'px'}"
          >
            <!-- <span class="num">{{item[1]}}</span> -->
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataArr: {
      type: Array,
      default: () => [["bird", 0], ["cat", 0], ["crab", 0], ["dog", 0], ["fish", 0], 
                      ["frog", 0], ["insect", 0], ["primate", 0], ["turtle", 0]]
    },
    config: {
      type: Object,
      default: () => {}
    },
  },
  data() {
    return {
      dataPercentageArr: [],
      defaultConfig: {
        // height of the figure
        figHeight: 300,
        // width of the figure
        figWidth: 300,
        // line color of positive numbers
        posColor: "#f22323",
        // line color of negative numbers
        negColor: "#00a000",
        // bottom line color
        lineColor: "#262626",
      },

      arrLength: 0,
    }
  },
  watch: {
    config() {
      this.updateConfig();
    },
  },
  created() {
    /* calculate maxPositive, maxNegative, maxNumber */
    let maxNegative = 0, maxPositive = 0;
    this.dataArr.forEach(function(v) {
      if ((v[1]>0) && (v[1]>maxPositive)) maxPositive = v[1];
      if ((v[1]<0) && (v[1]<maxNegative)) maxNegative = v[1];
    });
    let maxNumber=Math.max(maxPositive, Math.abs(maxNegative));
    // console.log(maxNegative, maxPositive, maxNumber)
    // calculate marginTop of line-chart
    this.$nextTick(function () {
      if (maxPositive != -maxNegative) {{
        document.querySelector('.line-chart').style.marginTop = maxPositive*this.defaultConfig.figHeight/(maxPositive-maxNegative)+'px';
      }}
    })
    /* ... */
    setTimeout(function() {
      for (var i = 0; i < this.arrLength; i++) {
        this.dataPercentageArr.push(Math.abs(this.dataArr[i][1]) / maxNumber);
      }
      console.log(this.dataArr);
      console.log(this.dataPercentageArr);
    }.bind(this), 0)
  },
  mounted() {
    this.updateConfig();
    this.arrLength = this.dataArr.length;
  },
  methods: {
    updateConfig() {
      this.defaultConfig = Object.assign(this.defaultConfig, this.config);
    },
  }
};
</script>

<style>
@import "./PredView.css";
</style>