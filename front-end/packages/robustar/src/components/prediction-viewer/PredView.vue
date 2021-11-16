<template>
  <div :style="{width:defaultConfig.componentWidth+'px',
                height:defaultConfig.figHeight+'px',
                }">
    <div :style="{width:defaultConfig.figWidth+'px',
                  height:defaultConfig.figHeight*(arrLength+2)/(arrLength+3)+'px',
                  transform:'translateX('+(defaultConfig.componentWidth-defaultConfig.figWidth)/2+'px)'}">
      <div
        class="chart-border"
        style="transform:translateX(100%) translateX(-1px)"
        v-if="maxNegative != 0"
      >
        <div class="chart-border-line" :style="{background:defaultConfig.lineColor}"></div>
        <div class="num" :style="{fontSize:defaultConfig.figHeight/(arrLength+3)*0.65+'px'}">{{maxNegative}}</div>
      </div>
      <div v-else style="float:left; height: 1px" :style="{width:defaultConfig.figWidth*0.1+'px'}"/>
      <div
        class="chart-line"
        :style="{background:defaultConfig.lineColor,
                transform:'translateX('+maxNegative*defaultConfig.figWidth/(maxNegative-maxPositive)+'px) translateX(-50%)'}"
      >
        <ul>
          <li v-for="(item, index) in dataArr" :key=index>
            <div
              :style="{height:defaultConfig.figHeight/(arrLength+3)+'px',
                      fontSize:defaultConfig.figHeight/(arrLength+3)*0.65+'px',
                      transform:'translateX('+(-maxNegative*defaultConfig.figWidth/(maxNegative-maxPositive)-defaultConfig.figWidth*0.05)+'px) translateX(-100%)'}"
            > {{item[0]}} </div>
            <div
              class="box"
              :title="item[1]"
              :class="item[1]>=0?'box-pos':'box-neg'"
              :style="{width:item[1]>=0?item[1]*defaultConfig.figWidth/(maxPositive-maxNegative)+'px'
                                      :item[1]*(-1)*defaultConfig.figWidth/(maxPositive-maxNegative)+'px',
                      background:(item[1]>=0)?defaultConfig.posColor:defaultConfig.negColor,
                      height:defaultConfig.figHeight/(arrLength+3)+'px'}"
            />
          </li>
        </ul>
        <div class="num" :style="{fontSize:defaultConfig.figHeight/(arrLength+3)*0.65+'px'}">0</div>
      </div>
      <div
        class="chart-border"
        :style="{transform:'translateX('+(defaultConfig.figWidth-1)+'px)'}"
        v-if="maxPositive != 0"
      >
        <div class="chart-border-line" :style="{background:defaultConfig.lineColor}"></div>
        <div class="num" :style="{fontSize:defaultConfig.figHeight/(arrLength+3)*0.65+'px'}">{{maxPositive}}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataArr: {
      type: Array,
      default: () => [["bird", 0], ["cat", 0], ["crab", 0], ["dog", 0], ["fish", 0], 
                      ["frog", 0], ["insect", 0], ["primate", 0], ["turtle", 1]]
    },
    config: {
      type: Object,
      default: () => {}
    },
  },
  data() {
    return {
      defaultConfig: {
        // width of the component
        componentWidth: 400,
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
        // the maximan border and the minimun border
        dataRange: null,
      },

      arrLength: 0,
      maxPositive: 0,
      maxNegative: 0,
    }
  },
  watch: {
    config() {
      this.updateConfig();
    },
  },
  created() {
    this.arrLength = this.dataArr.length;
    setTimeout(function() {
      if (this.defaultConfig.dataRange != null) {
        this.maxNegative = this.defaultConfig.dataRange[0];
        this.maxPositive = this.defaultConfig.dataRange[1];
      } else {
        for (var i = 0; i < this.arrLength; i++) {
          if (this.dataArr[i][1]>this.maxPositive) this.maxPositive = this.dataArr[i][1];
          if (this.dataArr[i][1]<this.maxNegative) this.maxNegative = this.dataArr[i][1];
        }
      }
    }.bind(this), 0);
  },
  mounted() {
    this.updateConfig();
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