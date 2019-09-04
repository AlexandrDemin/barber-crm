<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-bind="{'header':'Мои проекты', 'crumbs': []}"></breadcrumbs>
    <div class="projects grid-x" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert cell small-12">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading" class="cell large-8">
          <table class="projects-table stack">
              <thead>
                  <tr>
                      <th>Статус</th>
                      <th>Услуга</th>
                      <th>Сайт</th>
                      <th>ProjectId</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="project in projects" :key="project.projectId" @click="$router.push('/project/' + project.projectId)">
                    <td>
                      <svg width="8" height="8" viewBox="0 0 8 8" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="4" cy="4" r="4" v-bind:fill="$store.getters.getStatusColor(project.status)"/>
                      </svg>
                      &nbsp;
                      {{$store.getters.getStatusText(project.status)}}
                    </td>
                    <td>{{project.service}}</td>
                    <td>{{project.domain}}</td>
                    <td>{{project.projectId}}</td>
                </tr>
              </tbody>
          </table>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '@/components/BreadCrumbs'

export default {
  name: 'Projects',
  components: {
    breadcrumbs: BreadCrumbs
  },
  mounted: function () {
    this.$store.dispatch('getProjects')
  },
  computed: {
    errors: {
      get () {
        return this.$store.state.projectsState.errors
      }
    },
    isValid: {
      get () {
        return this.$store.state.projectsState.isValid
      }
    },
    isLoaded: {
      get () {
        return this.$store.state.projectsState.isLoaded
      }
    },
    isLoading: {
      get () {
        return this.$store.state.projectsState.isLoading
      }
    },
    projects: {
      get () {
        return this.$store.state.projectsState.projects
      }
    }
  }
}
</script>

<style>
  .projects-table tbody tr:hover {
    background: #F0F2F4;
    cursor: pointer;
  }
</style>
