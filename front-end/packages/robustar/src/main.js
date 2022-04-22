import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import VueSocketIO from 'vue-socket.io';
import SocketIO from 'socket.io-client';
import { configs } from '@/configs.js';

Vue.config.productionTip = false;

Vue.use(
  new VueSocketIO({
    debug: false,
    // connection: SocketIO(configs.serverUrl, { transports: ['websocket'] }),
    connection: configs.serverUrl,
    extraHeaders: { 'Access-Control-Allow-Origin': '*' },
    // options: { transports: ['websocket'] },
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
    };
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
  },
}).$mount('#app');
