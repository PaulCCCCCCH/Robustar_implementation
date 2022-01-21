<template>
  <div class="d-flex flex-column align-center" style="width: 100%">
    <!-- Page header-->
    <!-- <div class="text-h5 text-center font-weight-medium mb-4 mt-8">Select the image to edit</div> -->

    <!-- Image list controller -->
    <div class="d-flex justify-space-between px-16 py-8" style="width: 80%">
      <!-- Previous page button -->
      <v-btn :disabled="currentPage <= 0" depressed color="primary" @click="currentPage--">
        Prev Page
      </v-btn>

      <!-- Refresh page button & page number -->
      <div class="d-flex" style="width: 30%">
        <v-btn class="mr-4" depressed color="primary" @click="gotoPage"> Goto Page </v-btn>
        <v-text-field v-model="inputPage" dense label="Page Number" type="number"></v-text-field>
      </div>

      <!-- Next page button -->
      <v-btn :disabled="currentPage >= maxPage" depressed color="primary" @click="currentPage++">
        Next Page
      </v-btn>
      <!-- Class filter -->
      <div class="d-flex" style="width: 30%">
        <v-btn class="mr-4" v-if="selectedClass != 0" depressed color="primary" @click="gotoClass"> Goto Class </v-btn>
        <v-btn class="mr-4" v-else depressed disabled color="primary" @click="gotoClass"> Goto Class </v-btn>
        <v-select :items="classNames" v-model="selectedClass" dense label="Class Name"></v-select>
      </div>
    </div>

    <div class="d-flex flex-row justify-space-around">
    <!-- Image List -->
    <div style="width: auto">
      <div v-for="(imgline, row) in imageMatrix" :key="imgline[0]" class="d-flex">
        <div v-for="(url, col) in imgline" :key="url" class="mb-8 mr-8 row-item">
          <!-- minus 1 is necessary since Vue counts from 1 -->
          <!-- <img :src="url" alt="img" class="w-95" @click="editImage(row, col, url)" /> -->
          <v-hover v-slot="{ hover }">
            <v-img :src="url" alt="invalid image URL" height="200px" width="200px">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="primary lighten-3"
                  ></v-progress-circular>
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
                    @click="gotoImage(row, col, url, 'EditImage')"
                  >
                    <v-icon left>mdi-pencil</v-icon>
                    Annotate
                  </v-btn>
                  <v-btn
                    outlined
                    large
                    color="white"
                    width="150px"
                    @click="setCurrentImage(row, col, url)"
                  >
                    <v-icon left>mdi-cogs</v-icon>
                    Predict
                  </v-btn>
                </div>
              </v-expand-transition>
            </v-img>
          </v-hover>
        </div>
      </div>
    </div>
    
    <div style="width: 50%" v-if="image_id">
      <Visualizer :image_id="String(image_id)" :split="split"/>
    </div>
    </div>

    <div v-if="imageMatrix.length === 0" class="d-flex text-h2 grey--text mt-16 pt-16">
      Sorry, image list is empty
    </div>
  </div>
</template>

<script>
import { configs } from '@/configs.js';
import { imagePageIdx2Id, imageCoord2Idx, getPageNumber } from '@/utils/image_list';
import { APIGetSplitLength, APIGetClassNames } from '@/apis/images'
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
      imageMatrix: [],
      configs: configs,
      splitLength: 1000,
      classNames: [],
      classStartIdx: {},
      selectedClass: 0,
      split: "",
      image_id: "",
      image_url: ""
    };
  },
  mounted() {
    this.getMaxPage();
    this.getClassNames();
    this.loadImages();
  },
  watch: {
    $route() {
      this.currentPage = 0;
      this.classNames = [];
      this.classStartIdx = {};
      this.selectedClass = 0;
      this.getMaxPage();
      this.getClassNames();
      this.loadImages();
    },
    currentPage() {
      this.inputPage = this.currentPage;
      this.loadImages();
    },
  },
  methods: {
    getMaxPage() {
      APIGetSplitLength(
        this.$route.params.split,
        (res) => {
          this.splitLength = res.data.data;
          this.maxPage = getPageNumber(Math.max(this.splitLength - 1, 0));
          console.log(res.data.data);
        },
        (err) => console.log(err)
      );
    },
    getClassNames() {
      APIGetClassNames(this.$route.params.split,
        (res) => {
          console.log(res.data.data);
          this.classStartIdx = res.data.data;
          this.classNames = Object.keys(this.classStartIdx);
        },
        (err) => console.log(err)
      )
    },
    setCurrentImage(row, col, url) {
      const idx = imageCoord2Idx(row, col);
      const image_id = imagePageIdx2Id(this.currentPage, idx);
      this.split = this.$route.params.split;
      this.image_id = image_id;
      this.image_url = url;
      localStorage.setItem('split', this.$route.params.split);
      localStorage.setItem('image_id', image_id);
      localStorage.setItem('image_url', url);
    },
    gotoImage(row, col, url, componentName) {
      this.setCurrentImage(row, col, url)
      this.$router.push({ name: componentName });
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
      this.currentPage = Math.floor(startIdx / configs.imageListRow / configs.imageListCol);
      this.loadImages();
    },
    loadImages() {
      this.imageMatrix = [];
      let { imageListRow, imageListCol } = configs;
      let imgNumOfLastLine = 0;

      // last page
      if (this.currentPage === this.maxPage && this.maxPage > 0) {
        const imgNumOfLastPage = this.splitLength - configs.imagePerPage * this.maxPage;
        imageListRow = Math.floor(imgNumOfLastPage / imageListCol);
        imgNumOfLastLine = imgNumOfLastPage % imageListCol;
      }

      for (let row = 0; row < imageListRow; row++) {
        const line = [];
        for (let col = 0; col < imageListCol; col++) {
          const idx = imageCoord2Idx(row, col);
          const imgid = imagePageIdx2Id(this.currentPage, idx);
          line.push(`${configs.imageServerUrl}/${this.$route.params.split}/${imgid}`);
        }
        this.imageMatrix.push(line);
      }

      // last row of last page
      if (imgNumOfLastLine > 0) {
        const lastLine = [];
        for (let col = 0; col < imgNumOfLastLine; col++) {
          const idx = imageCoord2Idx(imageListRow, col);
          const imgid = imagePageIdx2Id(this.currentPage, idx);
          lastLine.push(`${configs.imageServerUrl}/${this.$route.params.split}/${imgid}`);
        }
        this.imageMatrix.push(lastLine);
      }
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
