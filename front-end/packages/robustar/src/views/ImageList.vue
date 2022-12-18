<template>
  <div class="d-flex justify-center align-center" style="height: 100%">
    <div class="d-flex flex-column flex-grow-1 align-center py-8">
      <div class="sticky-header d-flex mb-4">
        <!-- image list settings -->
        <v-sheet
          class="d-flex flex-column align-center justify-center rounded px-8 mr-4 elevation-2"
          color="white"
        >
          <div v-if="$route.params.split === 'validation' || $route.params.split === 'test'" style = "height:50px">
            <v-row no-gutters class="mb-6">
              <v-select
                class="pa-2"
                v-model="$root.imageSplit"
                :items="classification"
                v-bind:value="classification"
                @change="resetImageList"
                              data-test="image-list-select-classification"

              ></v-select>

              <v-menu class="pa-2" :close-on-content-click="false" :nudge-width="5" offset-x>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn v-bind="attrs" v-on="on"> SPLIT STATISTICS </v-btn>
                </template>
                <v-list>
                  <v-list-item>
                    <div>Accuracy: {{ accuarcy.value }}</div>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-row>
          </div>

          <!-- Page navigator -->
          <div class="d-flex justify-center align-center my-4">
            <!-- Previous page button -->
            <v-btn
              :disabled="currentPage <= 0 || !hasImages"
              depressed
              color="primary"
              @click="currentPage--"
              data-test="image-list-btn-prev-page"
            >
              PREV PAGE
            </v-btn>

            <!-- Refresh page button & page number -->
            <div class="d-flex align-center mx-8">
              <v-btn class="mr-4" depressed color="primary" @click="gotoPage"> GOTO PAGE </v-btn>
              <v-text-field
                data-test="image-list-input-page-number"
                v-model="inputPage"
                label="Page Number"
                type="number"
              ></v-text-field>
            </div>

            <!-- Next page button -->
            <v-btn
              data-test="image-list-btn-next-page"
              :disabled="currentPage >= maxPage || !hasImages"
              depressed
              color="primary"
              @click="currentPage++"
            >
              NEXT PAGE
            </v-btn>

            <v-divider vertical class="mx-8"></v-divider>

            <!-- Class filter -->
            <div class="d-flex align-center">
              <v-btn class="mr-4" depressed color="primary" @click="gotoClass"> GOTO CLASS </v-btn>
              <v-select
                :items="classNames"
                v-model="$root.imageClass"
                label="Class Name"
                data-test="image-list-select-class-name"
                clearable
              >
              </v-select>
            </div>
          </div>

          <!-- row & col settings -->
          <div class="d-flex">
            <v-select
              :items="imagePerPageOptions"
              v-model="imagePerPage"
              label="Number of image per page"
              class="mr-8"
              outlined
              @change="resetImageList"
              data-test="image-list-input-num-per-page"
            >
            </v-select>
            <v-select
              class="mr-8"
              :items="Object.keys(imageSizeMap)"
              v-model="imageSize"
              label="Image size"
              outlined
              @change="setImageSize"
            >
            </v-select>

            <v-btn
              v-if="$route.params.split === 'annotated'"
              depressed
              color="primary"
              @click="clearAnnotatedImage"
              data-test="image-list-btn-clear-annotated-imgs"
            >
              DELETE ALL
            </v-btn>
          </div>
        </v-sheet>

        <!-- influence calculation & auto annotate -->
        <v-sheet class="d-flex align-center justify-center rounded px-8 elevation-2" color="white">
          <div v-if="showExtraSettings" class="mr-4">
            <p>Click image to select its index</p>
            <v-radio-group v-model="imageIdxSelection" mandatory row>
              <v-radio :label="`Start Index : ${imageStartIdx}`" value="start"></v-radio>
              <v-radio :label="`End Index : ${imageEndIdx}`" value="end"></v-radio>
            </v-radio-group>
            <p v-if="imageEndIdx < imageStartIdx" style="color: red">
              End Index smaller than Start Index
            </p>
            <v-btn
              depressed
              outlined
              color="primary"
              class="mr-4"
              @click="
                $router.push({
                  name: 'InfluencePad',
                  params: { startIdx: imageStartIdx, endIdx: imageEndIdx },
                })
              "
            >
              <v-icon class="mr-2">mdi-vector-link</v-icon> Influence
            </v-btn>
            <v-btn
              depressed
              outlined
              color="primary"
              @click="
                $router.push({
                  name: 'AutoAnnotatePad',
                  params: { startIdx: imageStartIdx, endIdx: imageEndIdx },
                })
              "
            >
              <v-icon class="mr-2">mdi-auto-fix</v-icon> Auto Annotate
            </v-btn>
          </div>
          <v-btn icon color="grey" large @click="showExtraSettings = !showExtraSettings">
            <v-icon v-if="!showExtraSettings">mdi-chevron-double-right</v-icon>
            <v-icon v-else>mdi-chevron-double-left</v-icon>
          </v-btn>
        </v-sheet>
      </div>
      <v-divider class="mb-8 mt-4" style="width: 85%"></v-divider>

      <div v-if="!hasImages" class="d-flex text-h2 grey--text">Sorry, image list is empty</div>

      <v-row v-else class="d-flex" style="width: 85%">
        <!-- 6 images per row -->
        <v-col
          v-for="(url_and_binary, idx) in imageList"
          :key="url_and_binary[0]"
          :cols="imageSizeMap[imageSize]"
          data-test="image-list-div-all-imgs"
        >
          <div class="d-flex align-right" data-test="image-list-div-img">
            <v-btn
              v-if="$route.params.split === 'annotated'"
              color="secondary"
              class="mr-n1 mb-n1 mx-auto"
              icon
              small
              :data-test="`image-list-btn-remove-annotated-img-${idx}`"
              @click="deleteAnnotatedImage(idx, url_and_binary[0])"
            >
              <v-icon color="red">mdi-close-box</v-icon>
            </v-btn>
          </div>
          <v-hover :disabled="showExtraSettings" v-slot="{ hover }">
            <v-badge
              :value="
                showExtraSettings &&
                calcAbsIdx(idx) >= imageStartIdx &&
                calcAbsIdx(idx) <= imageEndIdx
              "
              :color="calcAbsIdx(idx) < imageEndIdx ? 'warning' : 'success'"
              :dot="calcAbsIdx(idx) > imageStartIdx && calcAbsIdx(idx) < imageEndIdx"
              bordered
              icon="mdi-check"
              overlap
              style="width: 100%; height: 100%"
            >
              <v-img
                :src="url_and_binary[1]"
                alt="invalid image URL"
                aspect-ratio="1"
                :data-test="`image-list-img-${idx}`"
                @click="selectImage(idx)"
              >
                <template v-slot:placeholder>
                  <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="primary lighten-3">
                    </v-progress-circular>
                  </v-row>
                </template>
                <v-expand-transition>
                  <div
                    v-if="hover"
                    class="d-flex flex-column transition-fast-in-fast-out primary v-card--reveal"
                    style="height: 100%"
                  >
                    <v-btn
                      class="mb-4"
                      outlined
                      color="white"
                      width="80%"
                      @click="gotoImage(url_and_binary[0], url_and_binary[1], 'ImageAnnotation')"
                      :data-test="`image-list-btn-edit-image-${idx}`"
                    >
                      <v-icon>mdi-pencil</v-icon>
                      <span v-if="imageSize !== 'extra small'" class="ml-2">ANNOTATE</span>
                    </v-btn>
                    <v-btn
                      outlined
                      color="white"
                      width="80%"
                      @click="
                        $root.imageURL = url_and_binary[0];
                        $refs['visualizer'].open();
                      "
                      :data-test="`image-list-btn-predict-image-${idx}`"
                    >
                      <v-icon>mdi-cogs</v-icon>
                      <span v-if="imageSize !== 'extra small'" class="ml-2">PREDICT</span>
                    </v-btn>
                  </div>
                </v-expand-transition>
              </v-img>
            </v-badge>
          </v-hover>
        </v-col>
      </v-row>
    </div>

    <Visualizer
      v-if="hasImages"
      ref="visualizer"
      :image_url="$root.imageURL"
      :split="$root.imageSplit"
    />
  </div>
</template>

<script>
import { configs } from '@/configs.js';
import { getPageNumber } from '@/utils/imageUtils';
import { APIDeleteEdit, APIClearEdit } from '@/services/edit';
import {
  APIGetImageList,
  APIGetSplitLength,
  APIGetClassifiedSplitLength,
  APIGetClassNames,
} from '@/services/images';
import Visualizer from '@/components/prediction-viewer/Visualizer';
import { getImageUrlFromFullUrl } from '@/utils/imageUtils';
import pDebounce from 'p-debounce';

const APIGetImageListDebounced = pDebounce(APIGetImageList, 0);

export default {
  name: 'ImageList',
  components: {
    Visualizer,
  },
  data() {
    return {
      isLoadingImages: false,
      showExtraSettings: false,
      imageIdxSelection: 'start',
      imageStartIdx: 0,
      imageEndIdx: 0,
      currentPage: 0,
      inputPage: 0,
      maxPage: 0,
      imageList: [],
      splitLength: 1000,
      allImageLength: 1000,
      correctImageLength: 1000,
      incorrectImageLength: 1000,
      classNames: [''],
      classStartIdx: {},
      testImageList: {},
      selectedClass: 0,
      split: 'test_correct',
      image_url: '',
      imagePerPage: 0,
      imageSize: configs.imageSize,
      imageSizeMap: {
        'extra small': 1,
        small: 2,
        medium: 3,
        large: 4,
        'extra large': 6,
      },
    };
  },
  mounted() {
    this.handleRouteChange();
    this.imagePerPage = this.imagePerPageOptions[1];
    this.initImageList();
    this.initClassifiedImageList();
  },
  watch: {
    $route() {
      this.handleRouteChange();
      this.initImageList();
      this.initClassifiedImageList();

      this.$root.imageURL = ''; // Reset current image url for visualizaer
    },
    currentPage() {
      this.inputPage = this.currentPage;
      this.$root.imagePageHistory[this.$root.imageSplit] = this.currentPage;
      this.loadImages();
    },
  },
  computed: {
    classification() {
      return [
        { text: 'All', value: this.$route.params.split },
        { text: 'Correctly Classified', value: this.$route.params.split + '_correct' },
        { text: 'Incorrectly Classified', value: this.$route.params.split + '_incorrect' },
      ];
    },
    accuarcy() {
      const [allImageLength, correctImageLength, incorrectImageLength] = this.testImageList
      // const correct_image_length = this.correct_image.length;
      // return { value: currect_length };
      return { value: Math.round((correctImageLength / allImageLength) * 100) / 100 };
      // return { value: Math.round((allImageLength) * 100) / 100 };
    },
    hasImages() {
      return this.imageList.length > 0;
    },
    imagePerPageOptions() {
      const imagePerRow = 12 / this.imageSizeMap[this.imageSize];
      // images per page is a multiple of imagePerRow
      return new Array(5).fill().map((option, index) => imagePerRow * (index + 1));
    },
  },
  methods: {
    handleRouteChange() {
      this.$root.imageSplit = this.$route.params.split;
      this.currentPage = this.$root.imagePageHistory[this.$root.imageSplit] || 0;
    },
    async initImageList() {
      try {
        const res = await APIGetSplitLength(this.$root.imageSplit);
        this.splitLength = res.data.data;
      } catch (error) {
        this.$root.alert(
          'error',
          error.response?.data?.detail || 'Image list initialization failed'
        );
        this.imageList = [];
        this.splitLength = 0;
      }
      this.maxPage = getPageNumber(Math.max(this.splitLength - 1, 0), this.imagePerPage);
      this.getClassNames();
      this.loadImages();
    },
    async initClassifiedImageList() {
      try {
        const res = await APIGetClassifiedSplitLength(this.split);
        this.testImageList = res.data.data;
        // this.allSplitLength = res.data.data[0];
        // this.correctSplitLength = res.data.data[1];
        // this.incorrectSplitLength = res.data.data[2];
        // this.maxCorrectPage = getPageNumber(
        //   Math.max(this.correctSplitLength - 1, 0),
        //   this.imagePerPage
        // );
        // this.getClassNames();
        // this.loadImages();
      } catch (error) {
        console.log(error);
        this.$root.alert('error', 'Image list initialization failed');
        this.imageList = [];
      }
    },
    resetImageList() {
      this.currentPage = 0;
      this.classNames = [''];
      this.classStartIdx = {};
      this.$root.imageClass = '';
      this.initImageList();
      this.initClassifiedImageList();
    },
    async getClassNames() {
      try {
        const res = await APIGetClassNames(this.$root.imageSplit);
        this.classStartIdx = res.data.data;
        this.classNames = Object.keys(this.classStartIdx);
      } catch (error) {
        this.$root.alert('error', error.response?.data?.detail || 'Fetching class names failed');
        this.imageList = [];
      }
    },
    async deleteAnnotatedImage(idx, url) {
      try {
        await APIDeleteEdit(this.$root.imageSplit, getImageUrlFromFullUrl(url));
        this.initImageList();
        this.initClassifiedImageList();
      } catch (error) {
        this.$root.alert('error', error.response?.data?.detail || 'Image deletion failed');
      }
    },
    deleteImageFailed() {
      this.$root.alert('error', 'Image deletion failed');
    },
    async clearAnnotatedImage() {
      this.$root.startProcessing('Auto-annotating...');
      try {
        await APIClearEdit();
        this.$root.finishProcessing();
        this.$root.alert('success', 'Image deletion succeed');
        this.loadImages();
      } catch (error) {
        this.$root.finishProcessing();
        this.$root.alert('error', 'Image deletion failed');
      }
    },
    gotoImage(url, base64, componentName) {
      this.$root.imageURL = url;
      this.$root.imageBase64 = base64;
      this.$router.push({
        name: componentName,
      });
    },
    gotoPage() {
      this.inputPage = Number(this.inputPage);
      if (this.inputPage > this.maxPage) {
        this.$root.alert('error', 'This is the end of the list.');
        this.inputPage = this.maxPage;
      } else if (this.inputPage < 0) {
        this.inputPage = 0;
      }
      this.currentPage = this.inputPage;
    },
    gotoClass() {
      let startIdx = this.classStartIdx[this.$root.imageClass] || 0;
      this.currentPage = Math.floor(startIdx / this.imagePerPage);
    },
    setImageSize() {
      this.imagePerPage = this.imagePerPageOptions[1];
      this.resetImageList();
    },
    async loadImages() {
      this.isLoadingImages = true;
      try {
        const res = await APIGetImageListDebounced(
          this.$root.imageSplit,
          this.currentPage,
          this.imagePerPage
        );
        const list = res.data.data || [];
        this.$nextTick(() => {
          this.imageList = [];
          list.forEach((imagePath) => {
            // this.imageList.push(`${configs.imagePathServerUrl}${imagePath}`);
            this.imageList.push(imagePath);
          });
        });
        this.isLoadingImages = false;
      } catch (error) {
        this.$root.alert('error', error.response?.data?.detail || 'Loading images failed');
        this.imageList = [];
        this.isLoadingImages = false;
      }
    },
    selectImage(idx) {
      if (this.showExtraSettings) {
        const absoluteIdx = this.calcAbsIdx(idx);
        if (this.imageIdxSelection === 'start') {
          this.imageStartIdx = absoluteIdx;
        } else if (this.imageIdxSelection === 'end') {
          this.imageEndIdx = absoluteIdx;
        }
      }
    },
    calcAbsIdx(idx) {
      return this.currentPage * this.imagePerPage + idx;
    },
  },
};
</script>

<style scoped>
.v-card--reveal {
  justify-content: center;
  align-items: center;
  position: absolute;
  bottom: 0;
  width: 100%;
  opacity: 0.8;
}

.v-card--reveal button {
  font-size: 0.5vw;
  overflow: hidden;
}

.sticky-header {
  position: sticky;
  top: 80px;
  z-index: 9;
}
</style>

