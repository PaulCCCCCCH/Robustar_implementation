<template>
  <div style="height: 100%; max-width: 30vw">
    <v-sheet
      v-if="isActive"
      class="pa-4 sticky-content overflow-auto"
      color="white"
      elevation="1"
      data-test="visualizer-sheet"
    >
      <v-btn class="mb-4" icon @click="close">
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-expansion-panels :multiple="true" v-model="panels" style="width: auto">
        <!-- Model Prediction -->
        <v-expansion-panel @click="togglePanel" v-if="show">
          <v-expansion-panel-header expand-icon="mdi-menu-down" data-test="model-prediction">
            Model Prediction
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div class="d-flex justify-center align-center">
              <PredView
                :dataArr="predDataArr"
                :config="predViewConfig"
                data-test="model-prediction-sheet"
              />
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Model Focus -->
        <v-expansion-panel v-if="!show">
          <div style="float: right">
            <v-icon @click="showCount"> mdi-magnify-minus</v-icon>
          </div>
          <div style="overflow-y: scroll">
            <div v-for="(url, index) in focusImgUrl" :key="index">
              <img :src="url" />
            </div>
          </div>
        </v-expansion-panel>
        <v-expansion-panel @change="togglePanel" v-if="show">
          <v-expansion-panel-header expand-icon="mdi-menu-down" data-test="model-focus">
            Model Focus
            <template v-slot:actions>
              <v-icon> mdi-menu-down </v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div style="overflow-x: scroll">
              <FocusView :focusImgUrl="focusImgUrl" data-test="model-focus-panel" />
            </div>
            <v-icon @click="showCount" style="float: right"> mdi-magnify-plus</v-icon>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Influence -->
        <v-expansion-panel @change="togglePanel" v-if="show">
          <v-expansion-panel-header expand-icon="mdi-menu-down" data-test="influence-images">
            Influence Images
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <InfluView :influImgUrl="influImgUrl" data-test="influence-images-panel" />
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Proposed Annotation -->
        <v-expansion-panel @change="togglePanel" v-if="show">
          <v-expansion-panel-header expand-icon="mdi-menu-down" data-test="proposed-annotation">
            Proposed annotation
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <ProposedEditView
              :proposedEditBase64="proposedEditBase64"
              data-test="proposed-annotation-panel"
            />
          </v-expansion-panel-content>
        </v-expansion-panel> </v-expansion-panels
    ></v-sheet>
    <v-tooltip v-else left>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          class="float-button"
          color="secondary"
          outlined
          fab
          large
          @click="open"
          v-bind="attrs"
          v-on="on"
          data-test="visualizer-btn"
        >
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </template>
      <span>Visualization Panel</span>
    </v-tooltip>
  </div>
</template>

<script>
import PredView from '@/components/prediction-viewer/PredView.vue';
import InfluView from '@/components/prediction-viewer/InfluView.vue';
import FocusView from '@/components/prediction-viewer/FocusView.vue';
import ProposedEditView from '@/components/prediction-viewer/ProposedEditView.vue';
import { APIPredict, APIGetInfluenceImages } from '@/services/predict';
import { APIGetProposedEdit } from '@/services/edit';
import { configs } from '@/configs.js';

export default {
  components: { PredView, InfluView, FocusView, ProposedEditView },
  props: {
    split: {
      type: String,
      default: () => '',
    },
    imageURL: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      isActive: false,
      predDataArr: [
        ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
      ],
      focusImgUrl: [],
      influImgUrl: [],
      proposedEditBase64: '',
      predViewConfig: {
        componentWidth: 300,
        figHeight: 300,
        figWidth: 300,
        // posColor: "#234567",
        // negColor: "#67891a",
        // lineColor: "#abcedf",
        dataRange: [0, 1],
      },
      configs: configs,
      panels: [],
      show: true,
    };
  },
  watch: {
    imageURL: function () {
      this.getVisualizeData();
    },
    split: function () {
      this.getVisualizeData();
    },
  },
  mounted() {
    const panels = sessionStorage.getItem('visualizer_panels');
    if (panels) {
      this.panels = JSON.parse(panels);
    }
  },
  methods: {
    showCount: function () {
      this.show = !this.show;
    },
    getVisualizeData() {
      if (this.split && this.imageURL) {
        this.viewPrediction(this.split, this.imageURL);
        this.getInfluence(this.split, this.imageURL);
        this.getProposedEdit(this.split, this.imageURL);
      }
    },
    async getProposedEdit(split, imageURL) {
      try {
        const res = await APIGetProposedEdit(split, imageURL);
        if (res.data.code === -1) {
          this.proposedEditBase64 = '';
          return;
        }
        const { base64 } = res.data.data;
        this.proposedEditBase64 = base64;
      } catch (error) {
        console.log(error);
        this.$root.alert('error', error.response?.data?.detail || 'Server error. Check console.');
      }
    },
    async viewPrediction(split, imageURL) {
      try {
        const res = await APIPredict(split, imageURL);
        let cap = 10;
        let responseData = res.data.data;
        let tempBuffer = responseData[0].map((e, i) => {
          return [e, responseData[1][i]];
        });
        tempBuffer.sort((a, b) => {
          return b[1] - a[1];
        });
        if (tempBuffer.length > cap) tempBuffer = tempBuffer.slice(0, cap);
        this.predDataArr = [
          tempBuffer.map((e) => {
            return e[0];
          }),
          tempBuffer.map((e) => {
            return e[1];
          }),
        ];
        this.focusImgUrl = [];
        for (let i = 0; i < 4; i++) {
          this.focusImgUrl.push(
            `${configs.serverUrl}/visualize?${configs.imagePathParamName}=${responseData[2][i]}`
          );
        }
      } catch (error) {
        console.log(error);
        this.$root.alert('error', error.response?.data?.detail || 'Server error. Check console.');
      }
    },

    async getInfluence(split, imageURL) {
      try {
        const res = await APIGetInfluenceImages(split, imageURL);
        // If influence not predicted:
        if (res.status !== 200 || res.data.code == -1) {
          this.influImgUrl = [];
          return;
        }
        const responseData = res.data.data;
        this.influImgUrl = [];
        for (let i = 0; i < 4; i++) {
          // responseData[i] is a length 2 array [image_path, imageURL]
          const url = responseData[i][1];
          this.influImgUrl.push(
            `${configs.imagePathServerUrl}?${configs.imagePathParamName}=${url}`
          );
        }
      } catch (error) {
        console.log(error);
        this.$root.alert('error', error.response?.data?.detail || 'Server error. Check console.');
      }
    },

    togglePanel() {
      setTimeout(() => {
        sessionStorage.setItem('visualizer_panels', JSON.stringify(this.panels));
      }, 0);
    },

    open() {
      this.isActive = true;
      // this.getVisualizeData();
    },

    close() {
      this.isActive = false;
    },
  },
};
</script>

<style scoped>
.float-button {
  position: fixed;
  right: 5px;
  top: 50vh;
  transform: translate(50%, -50%);
}

.float-button:hover {
  transform: translate(0, -55%);
  transition: 0.3s;
}

.sticky-content {
  position: sticky;
  top: 65px;
  height: 94vh;
  z-index: 9;
  background-color: white;
}
</style>
