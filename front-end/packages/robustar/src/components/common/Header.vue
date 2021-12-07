<template>
  <!-- App-Header -->
  <div class="app-header header">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center">
        <!-- Robustar Logo -->
        <a class="header-brand" href="index">
          <img src="../../assets/images/brand/logo.png" class="app-header-brand-logo" alt="logo" />
        </a>

        <!-- Right icons -->
        <div class="d-flex">
          <!-- Full screen icon -->
          <!-- TODO: Function not implimented -->
          <div>
            <a class="nav-link" href="#">
              <i class="el-icon-full-screen" />
            </a>
          </div>

          <!-- Toggle side bar -->
          <!-- TODO: Function not implimented -->
          <div>
            <a
              aria-label="Hide Sidebar"
              class="nav-link icon full-screen-link nav-link-bg"
              data-toggle="sidebar"
              href="#"
            >
              <i class="el-icon-s-fold" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
@import './Header.css';
</style>
