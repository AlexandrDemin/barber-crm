<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-bind="{'header': 'TEREC LSI', 'crumbs': [{'text': 'Мои проекты', 'link': ''}, {'text': project.domain, 'link': '#/project/' + project.projectId}]}"></breadcrumbs>
    <div class="project" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading" class="grid-x">
        <projectinfo class="cell small-12" v-bind="{'project': project}"></projectinfo>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '@/components/BreadCrumbs'
import ProjectInfo from '@/components/ProjectInfo'

export default {
  name: 'Terec',
  components: {
    breadcrumbs: BreadCrumbs,
    projectinfo: ProjectInfo
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
</style>
