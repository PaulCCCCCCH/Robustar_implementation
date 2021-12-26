<template>
  <!-- App-Header -->
  <v-app-bar app color="white">
    <!-- Robustar Logo -->
    <a class="header-brand" href="index">
      <img src="../../assets/images/brand/logo.png" class="app-header-brand-logo" alt="logo" />
    </a>

    <v-spacer></v-spacer>

    <!-- Full screen icon -->
    <!-- TODO: Function not implimented -->
    <div>
      <a class="nav-link" href="#">
        <i class="el-icon-full-screen" />
      </a>
    </div>

    <!-- Right icons -->
    <div class="d-flex">
      <!-- Full screen icon -->
      <!-- TODO: Function not implimented -->
      <!-- <div>
        <a class="nav-link" href="#">
          <i class="el-icon-full-screen" />
        </a>
      </div> -->

      <!-- Toggle side bar -->
      <!-- TODO: Function not implimented -->
      <!-- <div>
        <a
          aria-label="Hide Sidebar"
          class="nav-link icon full-screen-link nav-link-bg"
          data-toggle="sidebar"
          href="#"
        >
          <i class="el-icon-s-fold" />
        </a>
      </div> -->
    </div>
  </v-app-bar>
</template>

<script>
export default {};
</script>

<style>
@import './Header.css';
</style>
