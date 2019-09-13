<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-if="project" v-bind="{'header': 'TEREC LSI', 'crumbs': [{'text': 'Мои проекты', 'link': ''}, {'text': project.domain, 'link': '#/project/' + project.projectId}]}"></breadcrumbs>
    <div class="project" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading" class="grid-x">
        <projectinfo class="cell small-12" v-bind="{'project': project}"></projectinfo>
        <form class="cell large-6">
            <div class="large-12 cell">
                <label>Целевые страницы</label>
                <textarea rows="5" v-bind:disabled="generating" v-model="urls" autofocus="autofocus" autocomplete="on" v-on:keyup.enter="startGeneration"></textarea>
            </div>
            <div class="large-12 cell">
                <label>Запросы</label>
                <textarea rows="5" v-bind:disabled="generating" v-model="queries"></textarea>
            </div>
            <div class="large-12 cell">
                <button v-bind:disabled="generating" class="button primary" type="button" v-on:click="startGeneration">Получить рекомендации</button>
            </div>
        </form>
        <div class="cell large-12" v-if="generating || isGenerated">
          <h3>Рекомендации по написанию текстов</h3>
          <p v-if="generating">Получение рекомендаций. Пожалуйста, подождите.</p>
          <div class="grid-x" v-if="terec && isGenerated" v-for="item in terec" v-bind:key="item">
            <p class="cell large-12" v-if="terec.length > 1">Страница: {{Object.keys(terec).find(key => terec[key] === item)}}</p>
            <table class="cell large-6">
              <thead>
                <tr>
                  <th>Лемма из запроса</th>
                  <th>Минимальное число вхождений</th>
                  <th>Максимальное число вхождений</th>
                </tr>
              </thead>
              <tbody>
                <tr>{{url}}</tr>
                <tr v-for="word in item" v-bind:key="word">
                  <td>{{word['BaseForm']}}</td>
                  <td>{{word['MinCount']}}</td>
                  <td>{{word['MaxCount']}}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="cell small-12" v-if="terec && isGenerated">
            <button class="button primary" type="button" v-on:click="downloadTerec">Выгрузить в .xlsx</button>
          </div>
        </div>
        <iframe v-if="filename" :src="'download/' + filename" style='display: none;'></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '@/components/BreadCrumbs'
import ProjectInfo from '@/components/ProjectInfo'
import { HTTP } from '../api/api.js'

export default {
  name: 'Terec',
  components: {
    breadcrumbs: BreadCrumbs,
    projectinfo: ProjectInfo
  },
  mounted: function () {
    this.$store.dispatch('getProject', this.$route.params.projectId)
  },
  data () {
    return {
      generating: false,
      urls: '',
      queries: '',
      isGenerated: false,
      error: '',
      terec: '',
      filename: ''
    }
  },
  methods: {
    startGeneration: function () {
      this.generating = true
      this.generationEnded = ''
      this.isGenerated = false
      HTTP.post(
        `GetTerec/`,
        {
          urls: this.urls,
          queries: this.queries
        }
      )
        .then(response => {
          this.terec = response.data
          this.generating = false
          this.isGenerated = true
        })
        .catch(e => {
          this.error = e
          this.generating = false
          this.isGenerated = true
        })
    },
    downloadTerec: function () {
      this.filename = ''
      HTTP.post(
        `DownloadTerec/`,
        {
          terec: this.terec
        }
      )
        .then(response => {
          this.filename = response.data.filename
        })
        .catch(e => {
          this.error = e
        })
    }
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
