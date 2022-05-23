<template>
  <div style="height: 100%; max-width: 30vw">
    <v-sheet v-if="isActive" class="pa-4 sticky-content" color="white" elevation="1">
      <v-btn class="mb-4" icon @click="closeVisualizer">
        <v-icon>mdi-close</v-icon>
      </v-btn>

      <v-expansion-panels :multiple="true" v-model="panels" style="width: auto">
        <!-- Model Prediction -->
        <v-expansion-panel @click="toggle_panel">
          <v-expansion-panel-header expand-icon="mdi-menu-down">
            Model Prediction
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div class="d-flex justify-center align-center">
              <PredView :dataArr="predDataArr" :config="predViewConfig" />
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Model Focus -->
        <v-expansion-panel @change="toggle_panel">
          <v-expansion-panel-header expand-icon="mdi-menu-down">
            Model Focus
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <FocusView :focusImgUrl="focusImgUrl" />
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Influence -->
        <v-expansion-panel @change="toggle_panel">
          <v-expansion-panel-header expand-icon="mdi-menu-down">
            Influence Images
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <InfluView :influImgUrl="influImgUrl" />
          </v-expansion-panel-content>
        </v-expansion-panel>

        <!-- View Proposed Annotation -->
        <v-expansion-panel @change="toggle_panel">
          <v-expansion-panel-header expand-icon="mdi-menu-down">
            Proposed annotation
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <ProposedEditView :proposedEditUrl="proposedEditUrl" />
          </v-expansion-panel-content>
        </v-expansion-panel> </v-expansion-panels
    ></v-sheet>
    <v-btn v-else class="float-button" color="secondary" outlined large @click="openVisualizer">
      <v-icon left>mdi-eye</v-icon>VISUALIZER
    </v-btn>
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
    isActive: {
      type: Boolean,
      default: false,
    },
    split: {
      type: String,
      default: () => '',
    },
    image_url: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      predDataArr: [
        ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
      ],
      focusImgUrl: [],
      influImgUrl: [],
      proposedEditUrl: '',
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
    };
  },
  watch: {
    image_url: function () {
      this.get_visualize_data();
    },
    split: function () {
      this.get_visualize_data();
    },
  },
  mounted() {
    const panels = sessionStorage.getItem('visualizer_panels');
    if (panels) {
      this.panels = JSON.parse(panels);
    }
    if (this.split === 'annotated') {
      this.split = 'train';
    }
    this.get_visualize_data();
  },
  methods: {
    get_visualize_data() {
      if (this.split && this.image_url) {
        this.view_prediction(this.split, this.image_url);
        this.get_influence(this.split, this.image_url);
        this.get_proposed_edit(this.split, this.image_url);
      }
    },
    get_proposed_edit(split, image_url) {
      const success = (response) => {
        if (response.data.code == -1) {
          this.proposedEditUrl = '';
          return;
        }
        const proposedPath = response.data.data;
        this.proposedEditUrl = `${configs.imagePathServerUrl}/${proposedPath}`;
      };
      const failed = (err) => {
        console.log(err);
      };
      APIGetProposedEdit(split, image_url, success, failed);
    },
    view_prediction(split, image_url) {
      const success = (response) => {
        let cap = 10;
        let responseData = response.data.data;
        let temp_buffer = responseData[0].map((e, i) => {
          return [e, responseData[1][i]];
        });
        temp_buffer.sort((a, b) => {
          return b[1] - a[1];
        });
        if (temp_buffer.length > cap) temp_buffer = temp_buffer.slice(0, cap);
        this.predDataArr = [
          temp_buffer.map((e) => {
            return e[0];
          }),
          temp_buffer.map((e) => {
            return e[1];
          }),
        ];
        this.focusImgUrl = [];
        for (let i = 0; i < 4; i++) {
          this.focusImgUrl.push(`${configs.serverUrl}/visualize` + responseData[2][i]);
        }
      };
      const failed = (err) => {
        console.log(err);
        alert('Server error. Check console.');
      };
      APIPredict(split, image_url, success, failed);
    },

    get_influence(split, image_url) {
      const success = (response) => {
        // If influence not predicted:
        if (response.data.code == -1) {
          this.influImgUrl = [];
          return;
        }
        console.log(response);

        const responseData = response.data.data;
        this.influImgUrl = [];
        for (let i = 0; i < 4; i++) {
          // responseData[i] is a length 2 array [image_path, image_url]
          const url = responseData[i][1];
          this.influImgUrl.push(`${configs.imagePathServerUrl}/${url}`);
        }
      };

      const failed = (err) => {
        console.log(err);
      };

      APIGetInfluenceImages(split, image_url, success, failed);
    },

    toggle_panel() {
      setTimeout(() => {
        sessionStorage.setItem('visualizer_panels', JSON.stringify(this.panels));
      }, 0);
    },

    openVisualizer() {
      this.$emit('open');
    },

    closeVisualizer() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.float-button {
  position: fixed;
  right: 10px;
  top: 50vh;
  transform: translate(50%, -50%);
}

.float-button:hover {
  transform: translate(0, -50%);
  transition: 0.3s;
}

.sticky-content {
  position: sticky;
  top: 65px;
  height: 95vh;
  z-index: 9999;
  background-color: white;
}
</style>
