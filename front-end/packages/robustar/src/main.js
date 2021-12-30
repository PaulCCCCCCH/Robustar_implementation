import Vue from 'vue';
import App from './App.vue';
import router from './router';
// import ElementUI from 'element-ui';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import './main.css';
// import 'element-ui/lib/theme-chalk/index.css';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;

// Vue.use(ElementUI);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
  data() {
    return {
      processing: false,
      processingMsg: 'Processing ...',
      success: false,
      successMsg: 'Succeeded',
      error: false,
      errorMsg: 'Failed'
    }
  },
  methods: {
    alert(type, message) {
      if (type === 'success') {
        this.successMsg = message || 'Succeeded'
        this.success = true
      } else {
        this.errorMsg = message || 'Failed'
        this.error = true
      }
    },
    startProcessing(message) {
      this.processingMsg = message || 'Processing ...'
      this.processing = true
    },
    finishProcessing() {
      this.processing = false
    }
  },
}).$mount('#app');