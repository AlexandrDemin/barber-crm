import Vue from 'vue'
import Router from 'vue-router'
import Rivals from '@/components/Rivals'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Rivals',
      component: Rivals
    }
  ]
})
