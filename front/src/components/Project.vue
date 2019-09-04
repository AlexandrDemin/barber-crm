<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-bind="{'header': project.domain || Проект, 'crumbs': [{'text': 'Мои проекты', 'link': ''}]}"></breadcrumbs>
    <div class="project" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading" class="grid-x grid-margin-x grid-margin-y">
        <projectinfo class="cell small-12" v-bind="{'project': project}"></projectinfo>
        <a v-bind:href="getToolHref(tool)" class="tool-card cell large-4 medium-6" v-for="tool in project.tools" v-bind:key="tool">
          <h5>{{getToolHeader(tool)}}</h5>
          <p>{{getToolDescription(tool)}}</p>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '@/components/BreadCrumbs'
import ProjectInfo from '@/components/ProjectInfo'

export default {
  name: 'Project',
  components: {
    breadcrumbs: BreadCrumbs,
    projectinfo: ProjectInfo
  },
  methods: {
    getToolHref: function (tool) {
      switch (tool) {
        case 'seooffer':
          return this.project.seoOfferHref
        case 'semcore':
          return ''
        case 'contextoffer':
          return ''
        case 'terec':
          return ''
        case 'metatags':
          return ''
        case 'trafficforecast':
          return ''
        case 'timetotopforecast':
          return ''
        case 'conversionforecast':
          return ''
        case 'textgeneration':
          return ''
        case 'tonalityforecast':
          return ''
        case 'clientreport':
          return ''
        case 'siteaudit':
          return ''
        case 'filterrivals':
          return ''
        case 'socialseo':
          return ''
        default:
          return tool
      }
    },
    getToolHeader: function (tool) {
      switch (tool) {
        case 'seooffer':
          return 'КП SEO'
        case 'semcore':
          return 'Генерация семантического ядра'
        case 'contextoffer':
          return 'КП КПК'
        case 'terec':
          return 'TEREC LSI'
        case 'metatags':
          return 'Генерация мета-тегов'
        case 'trafficforecast':
          return 'Прогноз трафика из ПС'
        case 'timetotopforecast':
          return 'Прогноз срока вывода в топ'
        case 'conversionforecast':
          return 'Прогноз конверсии по запросам'
        case 'textgeneration':
          return 'Генерация текстов объявлений'
        case 'tonalityforecast':
          return 'Разметка тональности отзывов'
        case 'clientreport':
          return 'Отчёт для клиентов'
        case 'siteaudit':
          return 'Аудит сайта'
        case 'filterrivals':
          return 'Фильтрация запросов по конкурентам'
        case 'socialseo':
          return 'Продвижение групп в соц. сетях'
        default:
          return tool
      }
    },
    getToolDescription: function (tool) {
      switch (tool) {
        case 'seooffer':
          return 'Расчёт коммерческого предложения для услуг, связанных с поисковым продвижением. Включает инструменты для генерации сем. ядра, сбора позиций и спроса, прогноза трафика и конверсий, определения геозависимости и коммерческости запросов.'
        case 'semcore':
          return 'Генерация списка запросов. Запросы набираются из нескольких источников, фильтруются по релевантности, наличию конкурентов в выдаче, корректности и конверсионности. Получившееся СЯ моно использовать как для SEO, так и для контекстной рекламы.'
        case 'contextoffer':
          return 'Расчёт коммерческого предложения для услуг, связанных с платным трафиком. Включает инструменты для генерации сем. ядра, сбора спроса, прогноза трафика, конверсий и CPC по запросам. На выходе получается  медиаплан на 12 месяцев.'
        case 'terec':
          return 'Инструмент даёт рекомендации по количеству вхождений ключевых слов в текст страницы для роста позиций в выдаче по этим словам. Алгоритм учитывает контент конкурентов и работу алгоритмов ПС, которую мы определили на основе исследований.'
        case 'metatags':
          return 'Сервис генерирует мета-теги (title и description) для страницы, чтобы повысить скорость продвижения по ключевым словам. Количество вхождений подбирается на основе принципов работы алгоритмов ПС и контента конкурентов.'
        case 'trafficforecast':
          return 'Сервис прогнозирует объём трафика по запросу на определённой позиции в выдаче на основе частотности запроса и прогноза кликабельности сниппета.'
        case 'timetotopforecast':
          return 'Сервис прогнозирует срок вывода запроса в топ ПС в зависимости от текущей позиции, спроса по запросу, количества конкурентов и объёма планируемых доработок сайта.'
        case 'conversionforecast':
          return 'Сервис определяет относительную конверсионность запроса на основе его текста. С помощью получившегося коэффициента конверсионности можно сравнивать запросы между собой и выбирать самые конверсионные.'
        case 'textgeneration':
          return 'Инструмент генерирует тексты рекламных объявлений на основе объявлений конкурентов и контента сайта. При генерации текстов учитываются акции, проходящие на сайте, и УТП сайта.'
        case 'tonalityforecast':
          return 'Сервис размечает отзывы по трём группам; позитивный, нейтральный, негативный. В сочетании с парсером отзывов инструмент позволяет контролировать репутацию бренда в сети и быстро реагировать на упоминания бренда в негативном контексте.'
        case 'clientreport':
          return 'Статус сбора данных для клиентского отчёта в Google Data Studio, ссылка на сам отчёт.'
        case 'siteaudit':
          return 'SEO аудит сайта по 9 базовым параметрам. Определяет пригодность сайта к продвижению и набор доработок, которые нужно сделать в первую очередь.'
        case 'filterrivals':
          return 'Инструмент позволяет определить количество реальных конкурентов по запросам в КП SEO, скорректировать разметку конкурентов и отфильтровать запросы в КП по исправленным данным. Данные по ручной разметке будут использованы для дообучения алгоритма.'
        case 'socialseo':
          return 'Описание методологии продвижения групп в соц. сетях на основе наших исследований.'
        default:
          return tool
      }
    }
  },
  watch: {
    project () {
      document.title = 'Проект ' + (this.project.domain || '')
    }
  },
  mounted: function () {
    this.$store.dispatch('getProject', this.$route.params.projectId)
  },
  computed: {
    errors: {
      get () {
        return this.$store.state.projectState.errors
      }
    },
    isValid: {
      get () {
        return this.$store.state.projectState.isValid
      }
    },
    isLoaded: {
      get () {
        return this.$store.state.projectState.isLoaded
      }
    },
    isLoading: {
      get () {
        return this.$store.state.projectState.isLoading
      }
    },
    project: {
      get () {
        return this.$store.state.projectState.project
      }
    }
  }
}
</script>

<style>
  .tool-card {
    color: #173D63;
    background: #FFFFFF;
    box-shadow: 0px 1px 2px rgba(23, 61, 99, 0.15);
    border-radius: 5px;
    padding: 20px 30px;
  }
  .tool-card:hover {
    color: #173D63;
    background: #69E2B2;
    transform: translateY(-3px);
    box-shadow: 0 1px 1px -1px rgba(23, 61, 99,.33), 0 10px 35px -5px rgba(105, 226, 178,.4), 0 15px 20px -15px rgba(23, 61, 99,.15);
  }
  .tool-card {
    font-size: 14px;
  }
</style>
