<template>
  <div class="d-flex flex-column align-center">
    <!-- Page header-->
    <div class="text-h5 text-center font-weight-medium mb-4 mt-8">
      Select the image to edit
    </div>

    <!-- Image list controller -->
    <div class="d-flex justify-space-between px-16 py-8" style="width: 60%">
      <!-- Previous page button -->
      <v-btn depressed color="primary" @click="prevPage"> Prev Page </v-btn>

      <!-- Refresh page button & page number -->
      <div class="d-flex">
        <v-btn class="mr-4" depressed color="primary" @click="gotoPage"> Goto Page </v-btn>
        <v-text-field v-model="currentPage" dense label="Page Number"></v-text-field>
      </div>

      <!-- Next page button -->
      <v-btn v-if="isListEnd" depressed disabled color="primary" @click="nextPage"> Next Page </v-btn>
      <v-btn v-else depressed color="primary" @click="nextPage"> Next Page </v-btn>
    </div>

    <!-- Image List -->
    <div v-for="(imgline, row) in imageMatrix" :key="row">
      <div class="d-flex">
        <div class="mb-8 mr-8 row-item" v-for="(url, col) in imgline" :key="col">
          <!-- minus 1 is necessary since Vue counts from 1 -->
          <!-- <img :src="url" alt="img" class="w-95" @click="editImage(row, col, url)" /> -->
          <v-hover v-slot="{ hover }">
            <v-img :src="url" alt="invalid image URL" height="200px" width="200px" @error="onListEnd">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    v-if="!isListEnd"
                    indeterminate
                    color="primary lighten-3"
                  ></v-progress-circular>
                </v-row>
              </template>
              <v-expand-transition>
                <div
                  v-if="hover"
                  class="d-flex flex-column transition-fast-in-fast-out primary v-card--reveal text-h5 white--text"
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
                    @click="gotoImage(row, col, url, 'Prediction')"
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

    <div v-if="imageMatrix.length === 0" class="d-flex text-h2 grey--text mt-16 pt-16">
      Sorry, image list is empty
    </div>
  </div>
</template>

<script>
import { configs } from '@/configs.js';
import { imagePageIdx2Id, imageCoord2Idx, getPageNumber } from '@/utils/image_list';
import { APIGetSplitLength } from '@/apis/images'

export default {
  name: 'ImageList',
  components: {},
  data() {
    return {
      currentPage: 0,
      imageMatrix: [],
      configs: configs,
      isListEnd: false,
      splitLength: 1000
    };
  },
  mounted() {
    this.getMaxPage();
    this.loadImages();
  },
  watch: {
    $route() {
      this.currentPage = 0;
      this.getMaxPage();
      this.loadImages();
    },
  },
  methods: {
    getMaxPage() {
      APIGetSplitLength(this.$route.params.split,
        (res) => {this.splitLength = res.data.data; console.log(res.data.data)},
        (err) => console.log(err)
      )
    }, 
    nextPage() {
      this.currentPage++;
      this.loadImages();
    },
    prevPage() {
      if (this.currentPage <= 0) {
        return;
      }
      this.currentPage--;
      this.loadImages();
    },
    gotoImage(row, col, url, componentName) {
      const idx = imageCoord2Idx(row, col);
      const image_id = imagePageIdx2Id(this.currentPage, idx);
      localStorage.setItem('split', this.$route.params.split);
      localStorage.setItem('image_id', image_id);
      localStorage.setItem('image_url', url);
      this.$router.push({ name: componentName });
    },
    calcMaxPage() {
      return getPageNumber(Math.max(this.splitLength - 1, 0));
    },
    gotoPage() {
      this.currentPage = Math.min(this.calcMaxPage(), this.currentPage);
      console.log(this.currentPage)
      this.loadImages();
    },
    loadImages() {
      this.isListEnd = false;
      this.imageMatrix = [];
      for (let row = 0; row < configs.imageListRow; row++) {
        let line = [];
        for (let col = 0; col < configs.imageListCol; col++) {
          const idx = imageCoord2Idx(row, col);
          const imgid = imagePageIdx2Id(this.currentPage, idx);
          // TODO: '/train/' should be a component prop, not hard-coded
          line.push(`${configs.imageServerUrl}/${this.$route.params.split}/${imgid}`);
        }
        this.imageMatrix.push(line);
      }
    },
    onListEnd() {
      this.isListEnd = true;
      this.$root.alert('error', 'This is the end of the list.');
    }
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
