import Vue from 'vue'
import Router from 'vue-router'
import Stat from '@/components/Stat'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Stat',
      component: Stat
    },
    {
      path: '/:projectId',
      name: 'StatWithProject',
      component: Stat
    }
  ]
})
