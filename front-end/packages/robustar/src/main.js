import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import VueSocketIO from 'vue-socket.io';
import { configs } from '@/configs.js';

Vue.config.productionTip = false;

Vue.use(
  new VueSocketIO({
    debug: false,
    connection: configs.socketUrl,
  })
);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
  data() {
    return {
      // global overlay and snackbar
      processing: false,
      processingMsg: 'Processing ...',
      success: false,
      successMsg: 'Succeeded',
      error: false,
      errorMsg: 'Failed',
      // global info of image to be loaded/annotated
      imageURL: '',
      imageBase64: '',
      imageSplit: 'test_correct',
      imageClass: 'none',
      imagePageHistory: {},
    };
  },
  created() {
    this.imageURL = sessionStorage.getItem('image_url') || '';
    this.imageBase64 = sessionStorage.getItem('image_base64') || '';
    this.imageSplit = sessionStorage.getItem('image_split') || 'test_correct';
    this.imageClass = sessionStorage.getItem('image_class') || 'none';
    this.imagePageHistory = JSON.parse(sessionStorage.getItem('image_page_history')) || {};
    window.onbeforeunload = this.updateSessionStorage;
  },
  beforeDestroy() {
    this.updateSessionStorage();
  },
  methods: {
    /**
     * control global snackbar notification
     * @param {string} type type of notification
     * @param {string} message
     */
    alert(type, message) {
      if (type === 'success') {
        this.successMsg = message || 'Succeeded';
        this.success = true;
      } else {
        this.errorMsg = message || 'Failed';
        this.error = true;
      }
    },
    /**
     * toggle overlay to indicate processing state
     * @param {string} message
     */
    startProcessing(message) {
      this.processingMsg = message || 'Processing ...';
      this.processing = true;
    },
    finishProcessing() {
      this.processing = false;
    },
    updateSessionStorage() {
      sessionStorage.setItem('image_url', this.imageURL);
      sessionStorage.setItem('image_base64', this.imageBase64);
      sessionStorage.setItem('image_split', this.imageSplit);
      sessionStorage.setItem('image_class', this.imageClass);
      sessionStorage.setItem('image_page_history', JSON.stringify(this.imagePageHistory));
    },
  },
}).$mount('#app');
