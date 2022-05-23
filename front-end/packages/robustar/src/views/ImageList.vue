<template>
  <div class="d-flex justify-center align-center" style="height: 100%">
    <div class="d-flex flex-column flex-grow-1 align-center py-8">
      <!-- sticky header: settings -->
      <div class="d-flex flex-column align-center rounded px-8 sticky-header">
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
            <v-btn class="mr-4" depressed color="primary" :disabled="!hasImages" @click="gotoPage">
              GOTO PAGE
            </v-btn>
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
          <v-text-field
            v-model="imagePerPage"
            label="Number of image per page"
            type="number"
            outlined
            style="width: 170px"
            class="mr-8"
            @change="setImagePerPage"
          ></v-text-field>
          <v-text-field
            :value="imageColSpan"
            label="Number of columns (12 in total) per image"
            type="number"
            outlined
            style="width: 260px"
            @change="setImageColSpan"
          ></v-text-field>
        </div>
      </div>

      <v-divider class="mb-8 mt-4" style="width: 85%"></v-divider>

      <div v-if="!hasImages" class="d-flex text-h2 grey--text">Sorry, image list is empty</div>

      <v-row v-else class="d-flex" style="width: 85%">
        <!-- 6 images per row -->
        <v-col
          v-for="(url, idx) in imageList"
          :key="url"
          :cols="imageColSpan"
          class="d-flex child-flex"
          data-test="image-list-div-all-imgs"
        >
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
                    @click="gotoImage(idx, url, 'EditImage')"
                    :data-test="`image-list-btn-edit-image-${idx}`"
                  >
                    <v-icon left>mdi-pencil</v-icon>
                    ANNOTATE
                  </v-btn>
                  <v-btn outlined color="white" width="80%" @click="setCurrentImage(idx, url)">
                    <v-icon left>mdi-cogs</v-icon>
                    PREDICT
                  </v-btn>
                  <v-btn v-if="$route.params.split === 'annotated'" outlined color="white" width="80%" @click="deleteAnnotatedImage(idx, url)">
                    <v-icon left>mdi-cogs</v-icon>
                    DELETE
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
      imagePerPage: configs.imagePerPage,
      imageColSpan: configs.imageColSpan,
    };
  },
  mounted() {
    this.updateSplit();
    this.initImageList();
  },
  watch: {
    $route() {
      this.updateSplit();
      this.initImageList();
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
        { text: 'All', value: this.$route.params.split},
        { text: 'Correctly Classified', value: this.$route.params.split + '_correct' },
        { text: 'Incorrectly Classified', value: this.$route.params.split + '_incorrect' },
      ];
    },
    hasImages() {
      return this.imageList.length > 0;
    },
  },
  methods: {
    fetchImageUrl() {
      this.image_url = sessionStorage.getItem('image_url') || '';
    },
    updateSplit() {
      this.split = this.$route.params.split;
    },
    initImageList() {
      this.currentPage = Number(sessionStorage.getItem(this.split)) || 0;
      sessionStorage.setItem(this.split, this.currentPage);
      APIGetSplitLength(
        this.split,
        (res) => {
          this.splitLength = res.data.data;
          this.maxPage = getPageNumber(Math.max(this.splitLength - 1, 0), this.imagePerPage);
          this.getClassNames();
        },
        (err) => {
          console.log(err);
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
          console.log(res.data.data);
          this.classStartIdx = res.data.data;
          this.classNames = Object.keys(this.classStartIdx);
          this.loadImages();
        },
        (err) => {
          console.log(err);
          this.imageList = [];
        }
      );
    },
    setCurrentImage(idx, url) {
      this.image_url = getImageUrlFromFullUrl(url);
      sessionStorage.setItem('split', this.split);
      sessionStorage.setItem('image_url', this.image_url);
    },
    deleteImageSuccess(idx) {
        this.imageList.splice(idx, 1);
    },
    deleteImageFailed() {
        console.log('Delete image failed');
    },
    deleteAnnotatedImage(idx, url) {
      APIDeleteEdit(this.split, getImageUrlFromFullUrl(url), () => this.deleteImageSuccess(idx), this.deleteImageFailed);
    },

    gotoImage(idx, url, componentName) {
      this.setCurrentImage(idx, getImageUrlFromFullUrl(url));
      this.$router.push({
        name: componentName,
        params: { mode: this.$route.params.split },
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
      this.initImageList();
      this.loadImages();
    },
    setImagePerPage(value) {
      if (value > configs.MAX_IMAGE_PER_PAGE) {
        this.imagePerPage = configs.MAX_IMAGE_PER_PAGE;
      } else if (value < configs.MIN_IMAGE_PER_PAGE) {
        this.imagePerPage = configs.MIN_IMAGE_PER_PAGE;
      }
      this.initImageList();
      this.loadImages();
    },
    setImageColSpan(value) {
      if (value > configs.MAX_IMAGE_COL_SPAN) {
        this.imageColSpan = configs.MAX_IMAGE_COL_SPAN;
      } else if (value < configs.MIN_IMAGE_COL_SPAN) {
        this.imageColSpan = configs.MIN_IMAGE_COL_SPAN;
      } else {
        this.imageColSpan = value;
      }
    },
    loadImages() {
      let imgNum = this.imagePerPage;

      // handle last page
      if (this.currentPage === this.maxPage) {
        imgNum = this.splitLength - this.imagePerPage * this.maxPage;
      }

      APIGetImageList(
        this.split,
        this.currentPage,
        imgNum,
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
          console.log(err);
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
  z-index: 999;
  background-color: white;
}
</style>
