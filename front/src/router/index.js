import Vue from 'vue'
import Router from 'vue-router'
import Projects from '@/components/Projects'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Projects',
      component: Projects,
      meta: {
        title: 'Мои проекты'
      }
    }
  ]
})
