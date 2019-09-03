<template>
  <div class="main grid-container">
    <h1>Мои проекты</h1>
    <div class="rivals" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading && !errors">
          <table>
              <thead>
                  <tr>
                      <th>Статус</th>
                      <th>Услуга</th>
                      <th>Сайт</th>
                      <th class="text-right">ProjectId</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="project in projects" :key="project.projectId">
                    <td>
                      <svg width="8" height="8" viewBox="0 0 8 8" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="4" cy="4" r="4" fill="{{getStatusColor(project.status)}}"/>
                      </svg>
                      {{project.status}}
                    </td>
                    <td>{{project.service}}</td>
                    <td>{{project.domain}}</td>
                    <td>{{project.domain}}</td>
                    <td class="text-right">{{project.projectId}}</td>
                </tr>
              </tbody>
          </table>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Projects',
  mounted: function () {
    this.$store.dispatch('getProjects')
  },
  methods: {
    getStatusColor: function (status) {
      if (status === 'active') {
        return '#69E2B2'
      }
      return '#DCE0E5'
    }
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

</style>
