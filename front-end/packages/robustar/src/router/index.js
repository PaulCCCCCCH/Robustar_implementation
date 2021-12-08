import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import ImageList from '../views/ImageList.vue';
import TrainPad from '../views/TrainPad.vue';
import EditImage from '@/views/EditImage';

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
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/image-list/:split',
    name: 'ImageList',
    component: ImageList,
  },
  {
    path: '/train-pad',
    name: 'TrainPad',
    component: TrainPad,
  },
  {
    path: '/edit',
    name: 'EditImage',
    component: EditImage,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
