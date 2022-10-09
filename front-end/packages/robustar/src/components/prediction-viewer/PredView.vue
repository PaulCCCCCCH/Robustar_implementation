<template>
  <div
    :style="{ width: defaultConfig.componentWidth + 'px', height: defaultConfig.figHeight + 'px' }"
  >
    <div
      :style="{
        width: defaultConfig.figWidth + 'px',
        height: (defaultConfig.figHeight * (arrLength + 2)) / (arrLength + 3) + 'px',
        transform:
          'translateX(' + (defaultConfig.componentWidth - defaultConfig.figWidth) / 2 + 'px)',
      }"
    >
      <!-- <h2 class="d-flex justify-center align-center">Model Prediction</h2> -->
      <div
        class="chart-border"
        style="transform: translateX(100%) translateX(-1px)"
        v-if="maxNegative != 0"
      >
        <div class="chart-border-line" :style="{ background: defaultConfig.lineColor }"></div>
        <div
          class="num"
          :style="{ fontSize: (defaultConfig.figHeight / (arrLength + 3)) * 0.65 + 'px' }"
        >
          {{ maxNegative }}
        </div>
      </div>
      <div
        v-else
        style="float: left; height: 1px"
        :style="{ width: defaultConfig.figWidth * 0.1 + 'px' }"
      />
      <div
        class="chart-line"
        :style="{
          background: defaultConfig.lineColor,
          transform:
            'translateX(' +
            (maxNegative * defaultConfig.figWidth) / (maxNegative - maxPositive) +
            'px) translateX(-50%)',
        }"
      >
        <ul data-test="table">
          <li v-for="(item, index) in dataArr[1]" :key="index">
            <div
              :style="{
                height: defaultConfig.figHeight / (arrLength + 3) + 'px',
                fontSize: (defaultConfig.figHeight / (arrLength + 3)) * 0.65 + 'px',
                transform:
                  'translateX(' +
                  ((-maxNegative * defaultConfig.figWidth) / (maxNegative - maxPositive) -
                    defaultConfig.figWidth * 0.05) +
                  'px) translateX(-100%)',
              }"
            >
              {{ dataArr[0][index] }}
            </div>
            <div
              :data-test="`item-${index}`"
              class="box"
              :title="item"
              :class="item >= 0 ? 'box-pos' : 'box-neg'"
              :style="{
                width:
                  item >= 0
                    ? (item * defaultConfig.figWidth) / (maxPositive - maxNegative) + 'px'
                    : (item * -1 * defaultConfig.figWidth) / (maxPositive - maxNegative) + 'px',
                background: item >= 0 ? defaultConfig.posColor : defaultConfig.negColor,
                height: defaultConfig.figHeight / (arrLength + 3) + 'px',
              }"
            />
          </li>
        </ul>
        <div
          class="num"
          :style="{ fontSize: (defaultConfig.figHeight / (arrLength + 3)) * 0.65 + 'px' }"
        >
          0
        </div>
      </div>
      <div
        class="chart-border"
        :style="{ transform: 'translateX(' + (defaultConfig.figWidth - 1) + 'px)' }"
        v-if="maxPositive != 0"
      >
        <div class="chart-border-line" :style="{ background: defaultConfig.lineColor }"></div>
        <div
          class="num"
          :style="{ fontSize: (defaultConfig.figHeight / (arrLength + 3)) * 0.65 + 'px' }"
        >
          {{ String(maxPositive).slice(0, 6) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataArr: {
      type: Array,
      default: () => [
        ['bird', 'cat', 'crab', 'dog', 'fish', 'frog', 'insect', 'primate', 'turtle'],
        [0, 0, 0, 0.7, 0, 0, 0, 0, 0.3],
      ],
    },
    config: {
      type: Object,
      default: () => {},
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
        posColor: 'rgba(25,118,210,0.9)',
        // line color of negative numbers
        negColor: 'rgba(25,118,210,0.9)',
        // bottom line color
        lineColor: '#262626',
        // the maximan border and the minimun border
        dataRange: [0, 1],
      },

      arrLength: 0,
      maxNegative: 0,
    };
  },
  watch: {
    config() {
      this.updateConfig();
    },
  },
  computed: {
    maxPositive() {
      return Math.max(...this.dataArr[1]);
    },
  },

  mounted() {
    this.arrLength = this.dataArr[0].length;
    this.maxNegative = 0;
    this.updateConfig();
  },
  methods: {
    updateConfig() {
      this.defaultConfig = Object.assign(this.defaultConfig, this.config);
    },
  },
};
</script>

<style>
@import './PredView.css';
</style>
