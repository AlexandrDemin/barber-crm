import Vue from 'vue'
import Router from 'vue-router'
import Rivals from '@/components/Rivals'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/:offerid?',
      name: 'Rivals',
      component: Rivals
    }
  ]
})
