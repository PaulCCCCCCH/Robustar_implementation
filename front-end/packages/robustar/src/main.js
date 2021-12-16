import Vue from 'vue';
import App from './App.vue';
import router from './router';
import ElementUI from 'element-ui';
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';
import 'element-ui/lib/theme-chalk/index.css';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;

Vue.use(ElementUI);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
