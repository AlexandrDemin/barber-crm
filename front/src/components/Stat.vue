<template>
  <div class="main">
    <header>
      <div class="input-group">
        <input type="text" class="input-group-field" placeholder="id проекта" v-model="projectId" v-on:keyup.enter="validateAndFetch">
        <div class="input-group-button">
          <button type="button" v-on:click="validateAndFetch" class="button">Получить данные</button>
        </div>
      </div>
      <p v-if="!projectIdIsValid" class="error-text">Укажите корректный id проекта</p>
    </header>
    <div class="content grid-container fluid">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="error-text">
        <p>Ошибка получения данных с сервера:</p>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...</p>
      <div v-if="isLoaded" v-for="projectData in data" :key="projectData.projectId">
        <projectStat v-bind="projectData"></projectStat>
      </div>
    </div>
  </div>
</template>

<script>
import { HTTP } from '../api/api.js'
import ProjectStat from '@/components/ProjectStat'

export default {
  name: 'Stat',
  components: {
    projectStat: ProjectStat
  },
  data () {
    return {
      data: {},
      errors: [],
      isLoaded: false,
      isLoading: false,
      projectId: this.$route.params.projectId,
      projectIdIsValid: true
    }
  },
  methods: {
    validateAndFetch: function () {
      this.$router.push({name: 'StatWithProject', params: {projectId: this.projectId}})
      var pid = parseInt(this.projectId)
      if (pid > 0) {
        this.projectIdIsValid = true
        this.isLoading = true
        HTTP.get(`getStat/` + this.projectId)
          .then(response => {
            this.data = response.data
            this.errors = []
            this.isLoaded = true
            this.isLoading = false
          })
          .catch(e => {
            this.errors = []
            this.errors.push(e)
            this.isLoaded = true
            this.isLoading = false
          })
      } else {
        this.projectIdIsValid = false
        this.isLoading = false
      }
    }
  },
  created () {
    if (this.$route.params.projectId) {
      setInterval(this.validateAndFetch, 60000)
      this.validateAndFetch()
    }
  }
}
</script>

<style>
  header {
    padding: 10px 15px 0;
    position: fixed;
    top: 0;
    width: 100%;
    background: white;
    z-index: 9000;
    border-bottom: 2px solid rgba(0,0,0,0.1)
  }
  .content {
    padding-top: 80px;
  }
  .error-text {
    color: crimson;
  }
</style>
