import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue'),
  },
  {
    path: '/image-list/:split',
    name: 'ImageList',
    component: () => import(/* webpackChunkName: "about" */ '@/views/ImageList.vue'),
  },
  {
    path: '/train-pad',
    name: 'TrainPad',
    component: () => import(/* webpackChunkName: "about" */ '@/views/TrainPad.vue'),
  },
  {
    path: '/edit',
    name: 'ImageAnnotation',
    component: () => import(/* webpackChunkName: "about" */ '@/views/ImageAnnotation.vue'),
    props: true,
  },
  {
    path: '/test',
    name: 'TestPad',
    component: () => import(/* webpackChunkName: "about" */ '@/views/TestPad.vue'),
  },
  {
    path: '/influence-pad',
    name: 'InfluencePad',
    component: () => import(/* webpackChunkName: "about" */ '@/views/InfluencePad.vue'),
  },
  {
    path: '/predict',
    name: 'Prediction',
    component: () => import(/* webpackChunkName: "about" */ '@/views/Prediction.vue'),
  },
  {
    path: '/config',
    name: 'Config',
    component: () => import(/* webpackChunkName: "about" */ '@/views/Configuration.vue'),
  },
  {
    path: '/auto-annotate',
    name: 'AutoAnnotatePad',
    component: () => import(/* webpackChunkName: "about" */ '@/views/AutoAnnotatePad.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
