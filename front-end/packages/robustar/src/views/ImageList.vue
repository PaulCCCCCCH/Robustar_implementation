<template>
  <div id="imageList">
    <!-- Page header-->
    <div>
      <h5>Select the training image to edit.</h5>
    </div>

    <!-- Image list -->
    <div class="col-md-12">
      <!-- Image list controller -->
      <div class="row">
        <!-- Previous page button -->
        <div class="col-xl-4 col-lg-4 text-lg-center mt-xl-4">
          <button class="btn btn-primary mb-xl-0" @click="prevPage()">
            Prev Page
          </button>
        </div>

        <!-- Refresh page button & page number -->
        <div class="col-xl-4 col-lg-4 text-lg-center mt-xl-4">
          <div class="btn-list mb-xl-0">
            <button
              @click="gotoPage()"
              class="btn btn-primary mb-xl-0 refresh-page"
            >
              Goto Page
              <input v-model="currentPage" class="page-number" />
            </button>
          </div>
        </div>

        <!-- Next page button -->
        <div
          class="col-xl-4 col-lg-4 text-lg-center mt-xl-4"
          @click="nextPage()"
        >
          <div class="btn-list mb-xl-0">
            <a class="btn btn-primary mb-xl-0">Next Page</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Image List -->
    <div class="row train-img-list" v-for="(imgline, row) in imgmat" :key="row">
      <div
        class="card-body col-xl-2 col-sm-4"
        v-for="(url, col) in imgline"
        :key="col"
      >
        <div class="row mb-1">
          <!-- minus 1 is necessary since Vue counts from 1 -->
          <img :src="url" alt="img" class="w-95" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { configs } from "@/configs.js";
import { imagePageIdx2Id, imageCoord2Idx } from "@/utils/image_list";

export default {
  name: "ImageList",
  components: {},
  data() {
    return {
      currentPage: 0,
      imgmat: [],
      configs: configs,
    };
  },
  mounted() {
    this.loadImages();
  },
  watch: {
    $route () {
      this.currentPage = 0;
      this.loadImages()
    }
  },
  methods: {
    nextPage() {
      this.currentPage = parseInt(this.currentPage) + 1;
      this.loadImages();
    },
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 0);
      this.loadImages();
    },
    gotoPage() {
      this.loadImages();
    },
    imageClicked(index) {
      let image_id = imagePageIdx2Id(this.currentPage, index);
      this.$router.push({ path: `edit?id=${image_id}` });
    },
    getImageUrl(row, col) {
      let x = this.imgarr[imageCoord2Idx(row, col)];
      console.log(row, col, x);
    },
    loadImages() {
      this.imgmat = [];
      for (let row = 0; row < configs.imageListRow; row++) {
        let line = [];
        for (let col = 0; col < configs.imageListCol; col++) {
          let idx = imageCoord2Idx(row, col);
          let imgid = imagePageIdx2Id(this.currentPage, idx);
          // TODO: '/train/' should be a component prop, not hard-coded
          line.push(`${configs.serverUrl}/${this.$route.params.phase}/${imgid}`);
        }
        this.imgmat.push(line);
      }
      console.log(this.imgmat);
    },
  },
};
</script>

<style scoped>
img {
  cursor: pointer;
}

#imageList {
  text-align: center;
}
</style>