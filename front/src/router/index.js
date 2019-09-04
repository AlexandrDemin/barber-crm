import Vue from 'vue'
import Router from 'vue-router'
import Projects from '@/components/Projects'
import Project from '@/components/Project'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Projects',
      component: Projects,
      meta: {
        title: 'Мои проекты'
      }
    },
    {
      path: '/project/:projectId',
      name: 'Project',
      component: Project,
      meta: {
        title: 'Проект'
      }
    }
  ]
})
