import { defineConfig } from "cypress";

export default defineConfig({
  chromeWebSecurity: false,
  viewportWidth: 1920,
  viewportHeight: 1080,
  hideXHR: true,
  video: false,

  e2e: {
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      return require("./cypress/plugins/index.js")(on, config);
    },
    baseUrl: "http://localhost:8080/#/",
    specPattern: "cypress/tests/components/*spec.{js,jsx,ts,tsx}",
  },

  component: {
    setupNodeEvents(on, config) {},
    viewportHeight: 600,
    viewportWidth: 800,
    specPattern: "packages/robustar/src/**/*spec.{js,jsx,ts,tsx}",
  },

  component: {
    devServer: {
      framework: "vue-cli",
      bundler: "webpack",
    },
  },
});
