<template>
  <div class="stat">
    <div class="header">
      <input type="text" placeholder="Домен или id проекта" v-model="searchQuery">
    </div>
    <div class="content grid-container fluid">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error">
        <div>
          <p>Ошибка получения данных с сервера:</p>
          <p>{{error}}</p>
        </div>
      </div>
      <p v-if="!isLoaded">Загрузка...</p>
      <div v-if="isLoaded" v-for="projectData in filtered" :key="projectData.projectId">
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
      searchQuery: '',
      data: {},
      errors: [],
      isLoaded: false
    }
  },
  computed: {
    filtered: function () {
      var that = this
      if (this.searchQuery.length > 0) {
        return this.data.filter(function (el) {
          return el.domain.indexOf(that.searchQuery) !== -1 ||
            el.projectId.toString().indexOf(that.searchQuery) !== -1
        })
      } else {
        return this.data
      }
    }
  },
  methods: {
    fetch: function () {
      HTTP.get(`getStat`)
        .then(response => {
          this.data = response.data
          this.errors = []
          this.isLoaded = true
        })
        .catch(e => {
          this.errors = []
          this.errors.push(e)
          this.isLoaded = true
        })
    }
  },
  created () {
    setInterval(this.fetch, 60000)
    this.fetch()
  }
}
</script>

<style>
  .header {
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
</style>
