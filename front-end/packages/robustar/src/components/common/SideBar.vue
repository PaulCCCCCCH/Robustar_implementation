<template>
  <div class="side-bar">
    <el-menu default-active="3" @open="handleOpen" @close="handleClose">
      <!-- Module 1: Training -->
      <el-menu-item index="1" @click="navigateTo('/train-pad')">
        <template slot="title">
          <div class="side-bar-level1-title">
            <span> Train </span>
            <i class="side-bar-level1-icon el-icon-data-line"></i>
          </div>
        </template>
      </el-menu-item>

      <!-- Module 2: Annotate -->
      <el-menu-item index="2" @click="navigateTo('/edit')">
        <template slot="title">
          <div class="side-bar-level1-title">
            <span>Annotate</span>
            <i class="side-bar-level1-icon el-icon-edit"></i>
          </div>
        </template>
      </el-menu-item>

      <!-- Module 3: Inspect data -->
      <el-submenu index="3">
        <template slot="title">
          <div class="side-bar-level1-title">
            <span>Inspect Data</span>
            <i class="side-bar-level1-icon el-icon-view"></i>
          </div>
        </template>

        <!-- Inspect training data -->
        <el-menu-item index="3-1" @click="navigateTo('/image-list/train')">
          Training Data
        </el-menu-item>

        <!-- Inspect validation data -->
        <el-submenu index="3-2">
          <template slot="title">Validation Data</template>
          <el-menu-item class="sub-sub-menu" index="3-2-1"
            >Correctly Classified</el-menu-item
          >
          <el-menu-item class="sub-sum-menu" index="3-2-2"
            >Incorrectly Classified</el-menu-item
          >
        </el-submenu>

        <!-- Inspect test data -->
        <el-submenu index="3-3">
          <template slot="title">Test Data</template>
          <el-menu-item
            class="sub-sub-menu"
            index="3-3-1"
            @click="navigateTo('/image-list/test')"
            >Correctly Classified</el-menu-item
          >
          <el-menu-item
            class="sub-sub-menu"
            index="3-3-2"
            @click="navigateTo('/image-list/test')"
            >Incorrectly Classified</el-menu-item
          >
        </el-submenu>
      </el-submenu>

      <!-- Module 5: Generate Paired Data -->
      <el-menu-item index="4" @click="navigateTo('/generate')">
        <template slot="title">
          <div class="side-bar-level1-title">
            <span>Generate</span>
            <i class="side-bar-level1-icon el-icon-folder-add"></i>
          </div>
        </template>
      </el-menu-item>

      <!-- Module 5: More (Placeholder) -->
      <el-menu-item index="5" @click="navigateTo('/about')">
        <template slot="title">
          <div class="side-bar-level1-title">
            <span>More</span>
            <i class="side-bar-level1-icon el-icon-more-outline"></i>
          </div>
        </template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    navigateTo(path) {
      if (this.$route.path != path) {
        this.$router.push(path);
      }
    },
  },
};
</script>

<style>
@import "./SideBar.css";

li a {
  text-decoration: none;
}
</style>
