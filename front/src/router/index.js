import Vue from 'vue'
import Router from 'vue-router'
import Projects from '@/components/Projects'
import Project from '@/components/Project'
import Semcore from '@/components/Semcore'
import Terec from '@/components/Terec'
import MetaTags from '@/components/MetaTags'
import TrafficForecast from '@/components/TrafficForecast'
import TimeToTopForecast from '@/components/TimeToTopForecast'
import ConversionForecast from '@/components/ConversionForecast'
import TextGeneration from '@/components/TextGeneration'
import TonalityForecast from '@/components/TonalityForecast'
import ClientReport from '@/components/ClientReport'
import SiteAudit from '@/components/SiteAudit'
import FilterRivals from '@/components/FilterRivals'
import SocialSeo from '@/components/SocialSeo'

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
    },
    {
      path: '/project/:projectId/Semcore',
      name: 'Semcore',
      component: Semcore,
      meta: {
        title: 'Генерация семантического ядра'
      }
    },
    {
      path: '/project/:projectId/Terec',
      name: 'Terec',
      component: Terec,
      meta: {
        title: 'TEREC LSI'
      }
    },
    {
      path: '/project/:projectId/MetaTags',
      name: 'MetaTags',
      component: MetaTags,
      meta: {
        title: 'Генерация мета-тегов'
      }
    },
    {
      path: '/project/:projectId/TrafficForecast',
      name: 'TrafficForecast',
      component: TrafficForecast,
      meta: {
        title: 'Прогноз трафика из ПС'
      }
    },
    {
      path: '/project/:projectId/TimeToTopForecast',
      name: 'TimeToTopForecast',
      component: TimeToTopForecast,
      meta: {
        title: 'Прогноз срока вывода в топ'
      }
    },
    {
      path: '/project/:projectId/ConversionForecast',
      name: 'ConversionForecast',
      component: ConversionForecast,
      meta: {
        title: 'Прогноз конверсии по запросам'
      }
    },
    {
      path: '/project/:projectId/TextGeneration',
      name: 'TextGeneration',
      component: TextGeneration,
      meta: {
        title: 'Генерация текстов объявлений'
      }
    },
    {
      path: '/project/:projectId/TonalityForecast',
      name: 'TonalityForecast',
      component: TonalityForecast,
      meta: {
        title: 'Разметка тональности отзывов'
      }
    },
    {
      path: '/project/:projectId/ClientReport',
      name: 'ClientReport',
      component: ClientReport,
      meta: {
        title: 'Отчёт для клиентов'
      }
    },
    {
      path: '/project/:projectId/SiteAudit',
      name: 'SiteAudit',
      component: SiteAudit,
      meta: {
        title: 'Аудит сайта'
      }
    },
    {
      path: '/project/:projectId/FilterRivals',
      name: 'FilterRivals',
      component: FilterRivals,
      meta: {
        title: 'Фильтрация запросов по конкурентам'
      }
    },
    {
      path: '/project/:projectId/SocialSeo',
      name: 'SocialSeo',
      component: SocialSeo,
      meta: {
        title: 'Продвижение групп в соц. сетях'
      }
    }
  ]
})
