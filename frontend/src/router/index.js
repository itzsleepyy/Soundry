import { createWebHistory, createRouter } from 'vue-router'
import Home from '/src/views/Front.vue'
import Search from '/src/views/Search.vue'
import DownloadsView from '/src/views/DownloadsView.vue'
import config from '/src/config'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/search/:query',
    name: 'Search',
    component: Search,
  },
  {
    path: '/downloads',
    name: 'Downloads',
    component: DownloadsView,
  },
  // Redirect old routes to new one
  {
    path: '/list',
    redirect: '/downloads'
  },
  {
    path: '/download',
    redirect: '/downloads'
  },
]

const router = createRouter({
  history: createWebHistory(config.BASEURL),
  routes,
})

export default router
