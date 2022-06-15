<template>
  <div class="d-flex justify-center align-center" style="height: 100%">
    <div class="d-flex flex-column flex-grow-1 align-center py-8">
      <!-- sticky header: settings -->
      <div class="d-flex flex-column align-center rounded px-8 elevation-2 sticky-header">
        <div
          v-if="$route.params.split === 'validation' || $route.params.split === 'test'"
          style="width: 200px"
        >
          <v-select
            v-model="split"
            :items="classification"
            @change="resetImageList"
            data-test="image-list-select-classification"
          ></v-select>
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
            <v-btn
              :disabled="selectedClass === 0"
              class="mr-4"
              depressed
              color="primary"
              @click="gotoClass"
            >
              GOTO CLASS
            </v-btn>
            <v-select
              :items="classNames"
              v-model="selectedClass"
              label="Class Name"
              data-test="image-list-select-class-name"
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
          >
          </v-select>
          <v-select
            :items="Object.keys(imageSizeMap)"
            v-model="imageSize"
            label="Image size"
            outlined
            @change="setImageSize"
          >
          </v-select>
        </div>
      </div>
      <v-divider class="mb-8 mt-4" style="width: 85%"></v-divider>

      <div v-if="!hasImages" class="d-flex text-h2 grey--text">Sorry, image list is empty</div>

      <v-row v-else class="d-flex" style="width: 85%">
        <!-- 6 images per row -->

        <v-col
          v-for="(url, idx) in imageList"
          :key="url"
          :cols="imageSizeMap[imageSize]"
          data-test="image-list-div-all-imgs"
        >
          <!-- class="d-flex child-flex" -->
          <div class="d-flex align-right">
            <v-btn
              v-if="$route.params.split === 'annotated'"
              color="secondary"
              class="mr-n1 mb-n1 mx-auto"
              icon
              small
              @click="deleteAnnotatedImage(idx, url)"
            >
              <v-icon color="red">mdi-close-box</v-icon>
            </v-btn>
          </div>
          <v-hover v-slot="{ hover }">
            <v-img
              :src="url"
              alt="invalid image URL"
              aspect-ratio="1"
              :data-test="`image-list-img-${idx}`"
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
                    @click="gotoImage(url, 'EditImage')"
                    :data-test="`image-list-btn-edit-image-${idx}`"
                  >
                    <v-icon>mdi-pencil</v-icon>
                    <span v-if="imageSize !== 'extra small'" class="ml-2">ANNOTATE</span>
                  </v-btn>
                  <v-btn
                    outlined
                    color="white"
                    width="80%"
                    @click="setCurrentImage(url)"
                    :data-test="`image-list-btn-predict-image-${idx}`"
                  >
                    <v-icon>mdi-cogs</v-icon>
                    <span v-if="imageSize !== 'extra small'" class="ml-2">PREDICT</span>
                  </v-btn>
                </div>
              </v-expand-transition>
            </v-img>
          </v-hover>
        </v-col>
      </v-row>
    </div>

    <Visualizer
      v-if="hasImages"
      :is-active="image_url !== ''"
      :image_url="image_url"
      :split="split"
      @open="fetchImageUrl"
      @close="image_url = ''"
    />
  </div>
</template>

<script>
import { configs } from '@/configs.js';
import { imagePageIdx2Id, getPageNumber } from '@/utils/imageUtils';
import { APIDeleteEdit } from '@/services/edit';
import { APIGetImageList, APIGetSplitLength, APIGetClassNames } from '@/services/images';
import Visualizer from '@/components/prediction-viewer/Visualizer';
import { getImageUrlFromFullUrl } from '@/utils/imageUtils';

export default {
  name: 'ImageList',
  components: {
    Visualizer,
  },
  data() {
    return {
      currentPage: 0,
      inputPage: 0,
      maxPage: 0,
      imageList: [],
      splitLength: 1000,
      classNames: [],
      classStartIdx: {},
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
    this.updateSplit();
    this.fetchCurrentPage();
    this.imagePerPage = this.imagePerPageOptions[1];
    this.initImageList();
  },
  watch: {
    $route() {
      this.updateSplit();
      this.fetchCurrentPage();
      this.initImageList();
      this.image_url = ''; // Reset current image url for visualizaer
    },
    currentPage() {
      sessionStorage.setItem(this.split, this.currentPage);
      this.inputPage = this.currentPage;
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
    fetchImageUrl() {
      this.image_url = sessionStorage.getItem('image_url') || '';
    },
    fetchCurrentPage() {
      this.currentPage = Number(sessionStorage.getItem(this.split)) || 0;
      sessionStorage.setItem(this.split, this.currentPage);
    },
    updateSplit() {
      this.split = this.$route.params.split;
    },
    initImageList() {
      APIGetSplitLength(
        this.split,
        (res) => {
          this.splitLength = res.data.data;
          this.maxPage = getPageNumber(Math.max(this.splitLength - 1, 0), this.imagePerPage);
          this.getClassNames();
          this.loadImages();
        },
        (err) => {
          this.$root.alert('error', 'Image list initialization failed');
          this.imageList = [];
        }
      );
    },
    resetImageList() {
      this.currentPage = 0;
      this.classNames = [];
      this.classStartIdx = {};
      this.selectedClass = 0;
      this.initImageList();
    },
    getClassNames() {
      APIGetClassNames(
        this.split,
        (res) => {
          this.classStartIdx = res.data.data;
          this.classNames = Object.keys(this.classStartIdx);
        },
        (err) => {
          this.$root.alert('error', 'Fetching class names failed');
          this.imageList = [];
        }
      );
    },
    setCurrentImage(url) {
      this.image_url = getImageUrlFromFullUrl(url);
      sessionStorage.setItem('split', this.split);
      sessionStorage.setItem('image_url', this.image_url);
    },
    deleteImageSuccess() {
      this.initImageList();
    },
    deleteImageFailed() {
      this.$root.alert('error', 'Image deletion failed');
    },
    deleteAnnotatedImage(idx, url) {
      APIDeleteEdit(
        this.split,
        getImageUrlFromFullUrl(url),
        () => this.deleteImageSuccess(idx),
        this.deleteImageFailed
      );
    },
    gotoImage(url, componentName) {
      this.setCurrentImage(getImageUrlFromFullUrl(url));
      this.$router.push({
        name: componentName,
        params: { split: this.$route.params.split },
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
      let startIdx = this.classStartIdx[this.selectedClass];
      this.currentPage = Math.floor(startIdx / this.imagePerPage);
      this.loadImages();
    },
    setImageSize() {
      this.imagePerPage = this.imagePerPageOptions[1];
      this.resetImageList();
    },
    loadImages() {
      APIGetImageList(
        this.split,
        this.currentPage,
        this.imagePerPage,
        (res) => {
          const list = res.data.data;
          this.$nextTick(() => {
            this.imageList = [];
            list.forEach((imagePath) => {
              this.imageList.push(`${configs.imagePathServerUrl}${imagePath}`);
            });
          });
        },
        (err) => {
          this.$root.alert('error', 'Loading images failed');
          this.imageList = [];
        }
      );
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
  background-color: white;
}
</style>
