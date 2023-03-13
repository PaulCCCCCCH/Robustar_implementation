import { defineConfig } from "cypress";

export default defineConfig({
  viewportWidth: 1920,
  viewportHeight: 1080,
  video: false,

  env: {
    hideXHR: true,
  },

  e2e: {
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      return require("./cypress/plugins/index.js")(on, config);
    },
    baseUrl: "http://localhost:8080/#/",
    specPattern: "cypress/tests/components/*spec.{js,jsx,ts,tsx}",
    retries: {
      // Configure retry attempts for `cypress run`
      // Default is 0
      runMode: 2,
      // Configure retry attempts for `cypress open`
      // Default is 0
      openMode: 0
    }
  },

  component: {
    setupNodeEvents(on, config) {},
    viewportHeight: 600,
    viewportWidth: 800,
    specPattern: "packages/robustar/src/**/*spec.{js,jsx,ts,tsx}",
    devServer: {
      framework: "vue-cli",
      bundler: "webpack",
    },
  },
});
