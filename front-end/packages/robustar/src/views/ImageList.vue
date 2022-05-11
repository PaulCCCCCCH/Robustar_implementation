<template>
  <div class="d-flex justify-center align-center" style="height: 100%">
    <div v-if="!hasImages" class="d-flex text-h2 grey--text">Sorry, image list is empty</div>

    <div v-if="hasImages" class="d-flex flex-column flex-grow-1 align-center px-4">
      <!-- Page header-->
      <!-- <div class="text-h5 text-center font-weight-medium mb-4 mt-8">Select the image to edit</div> -->

      <div
        v-if="$route.params.split === 'validation' || $route.params.split === 'test'"
        class="d-flex mb-4"
        style="width: 200px"
      >
        <v-select
          :items="classification"
          v-model="split"
          dense
          @change="resetImageList"
          data-test="image-list-select-classification"
        ></v-select>
      </div>

      <!-- Page navigator -->
      <div class="d-flex justify-center mb-4">
        <!-- Previous page button -->
        <v-btn
          :disabled="currentPage <= 0"
          depressed
          color="primary"
          @click="currentPage--"
          data-test="image-list-btn-prev-page"
        >
          PREV PAGE
        </v-btn>

        <!-- Refresh page button & page number -->
        <div class="d-flex mx-8">
          <v-btn class="mr-4" depressed color="primary" @click="gotoPage"> GOTO PAGE </v-btn>
          <v-text-field
            data-test="image-list-input-page-number"
            v-model="inputPage"
            dense
            label="Page Number"
            type="number"
          ></v-text-field>
        </div>

        <!-- Next page button -->
        <v-btn
          data-test="image-list-btn-next-page"
          :disabled="currentPage >= maxPage"
          depressed
          color="primary"
          @click="currentPage++"
        >
          NEXT PAGE
        </v-btn>
      </div>

      <!-- Class filter -->
      <div class="d-flex mb-4" style="width: 300px">
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
          dense
          label="Class Name"
          data-test="image-list-select-class-name"
        >
        </v-select>
      </div>

      <v-divider class="mb-8" style="width: 100%"></v-divider>

      <div class="d-flex flex-row flex-wrap justify-start" style="flex">
        <div
          v-for="(url, idx) in imageList"
          :key="url"
          class="mb-8 mr-8 row-item"
          data-test="image-list-div-all-imgs"
        >
          <v-hover v-slot="{ hover }">
            <v-img
              :src="url"
              alt="invalid image URL"
              height="200px"
              width="200px"
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
                  class="
                    d-flex
                    flex-column
                    transition-fast-in-fast-out
                    primary
                    v-card--reveal
                    text-h5
                    white--text
                  "
                  style="height: 100%"
                >
                  <v-btn
                    class="mb-4"
                    outlined
                    large
                    color="white"
                    width="150px"
                    @click="gotoImage(idx, url, 'EditImage')"
                    :data-test="`image-list-btn-edit-image-${idx}`"
                  >
                    <v-icon left>mdi-pencil</v-icon>
                    ANNOTATE
                  </v-btn>
                  <v-btn
                    outlined
                    large
                    color="white"
                    width="150px"
                    @click="setCurrentImage(idx, url)"
                  >
                    <v-icon left>mdi-cogs</v-icon>
                    PREDICT
                  </v-btn>
                </div>
              </v-expand-transition>
            </v-img>
          </v-hover>
        </div>
      </div>
    </div>

    <Visualizer
      v-if="hasImages"
      :is-active="image_id !== ''"
      :image_id="String(image_id)"
      :split="split"
      @open="fetchImageId"
      @close="image_id = ''"
    />
  </div>
</template>

<script>
import { configs } from '@/configs.js';
import { imagePageIdx2Id, getPageNumber } from '@/utils/imageUtils';
import { APIGetImageList, APIGetSplitLength, APIGetClassNames } from '@/services/images';
import Visualizer from '@/components/prediction-viewer/Visualizer';

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
      configs: configs,
      splitLength: 1000,
      classNames: [],
      classStartIdx: {},
      selectedClass: 0,
      split: 'test_correct',
      image_id: '',
      image_url: '',
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
        { text: 'Correctly Classified', value: this.$route.params.split + '_correct' },
        { text: 'Incorrectly Classified', value: this.$route.params.split + '_incorrect' },
      ];
    },
    hasImages() {
      return this.imageList.length > 0;
    },
  },
  methods: {
    fetchImageId() {
      this.image_id = sessionStorage.getItem('image_id') || '';
    },
    updateSplit() {
      this.split = this.$route.params.split;
      if (this.split === 'validation' || this.split === 'test') {
        this.split += '_correct';
      }
    },
    initImageList() {
      this.currentPage = Number(sessionStorage.getItem(this.split)) || 0;
      sessionStorage.setItem(this.split, this.currentPage);
      APIGetSplitLength(
        this.split,
        (res) => {
          this.splitLength = res.data.data;
          this.maxPage = getPageNumber(Math.max(this.splitLength - 1, 0));
          console.log(res.data.data);
          this.getClassNames();
        },
        (err) => console.log(err)
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
        (err) => console.log(err)
      );
    },
    setCurrentImage(idx, url) {
      const image_id = imagePageIdx2Id(this.currentPage, idx);
      this.image_id = image_id;
      this.image_url = url;
      sessionStorage.setItem('split', this.split);
      sessionStorage.setItem('image_id', image_id);
      sessionStorage.setItem('image_url', url);
      sessionStorage.setItem('save_image_id', image_id);
      sessionStorage.setItem('save_image_split', this.$route.params.split);
    },
    gotoImage(idx, url, componentName) {
      this.setCurrentImage(idx, url);
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
      }
      this.currentPage = this.inputPage;
    },
    gotoClass() {
      let startIdx = this.classStartIdx[this.selectedClass];
      this.currentPage = Math.floor(startIdx / configs.imagePerPage);
      this.loadImages();
    },
    loadImages() {
      let imgNum = configs.imagePerPage;

      // handle last page
      if (this.currentPage === this.maxPage) {
        imgNum = this.splitLength - configs.imagePerPage * this.maxPage;
      }

      APIGetImageList(
        this.split,
        this.currentPage,
        imgNum,
        (res) => {
          const list = res.data.data;
          this.$nextTick(() => {
            this.imageList = [];
            list.forEach((image) => {
              this.imageList.push(`${configs.imagePathServerUrl}${image[0]}`);
            });
          });
        },
        (err) => console.log(err)
      );
    },
  },
};
</script>

<style scoped>
.row-item:last-child {
  margin-right: 0 !important;
}

.v-card--reveal {
  justify-content: center;
  align-items: center;
  position: absolute;
  bottom: 0;
  width: 100%;
  opacity: 0.8;
}
</style>
