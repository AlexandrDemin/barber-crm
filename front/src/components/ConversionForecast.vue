<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-if="project" v-bind="{'header': 'Прогноз конверсии по запросам', 'crumbs': [{'text': 'Мои проекты', 'link': ''}, {'text': project.domain, 'link': '#/project/' + project.projectId}]}"></breadcrumbs>
    <div class="project" v-if="isLoading || isLoaded">
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="callout alert">
        <h5>Ошибка получения данных с сервера</h5>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading" class="grid-x">
        <projectinfo class="cell small-12" v-bind="{'project': project}"></projectinfo>
        <div class="large-12 cell">
          <input type="file" id="file" ref="file" v-on:change="handleFileUpload()" style="display:none"/>
          <button class="button primary" v-on:click="submitFile()">Загрузить .xlsx с запросами и получить прогноз</button>
        </div>
        <div class="large-6 cell" v-if="data">
          <table>
            <thead>
              <tr>
                <th>Запрос</th>
                <th class="text-right">Прогноз относительной конверсии</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in data" v-bind:key="item">
                <td>{{item.query}}</td>
                <td class="text-right">{{item.conversion}}%</td>
              </tr>
            </tbody>
          </table>
          <div class="cell small-12">
            <button class="button primary" type="button" v-on:click="download">Выгрузить в .xlsx</button>
          </div>
          <iframe v-if="filename" :src="'download/' + filename" style='display: none;'></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '@/components/BreadCrumbs'
import ProjectInfo from '@/components/ProjectInfo'
import { HTTP } from '../api/api.js'

export default {
  name: 'ConversionForecast',
  components: {
    breadcrumbs: BreadCrumbs,
    projectinfo: ProjectInfo
  },
  mounted: function () {
    this.$store.dispatch('getProject', this.$route.params.projectId)
  },
  data: function () {
    return {
      file: '',
      data: '',
      error: '',
      filename: ''
    }
  },
  methods: {
    submitFile: function () {
      this.$refs.file.click()
    },
    handleFileUpload: function () {
      this.data = ''
      this.file = this.$refs.file.files[0]
      let formData = new FormData()
      formData.append('file', this.file)
      HTTP.post(
        `GetConversionForecast/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
        .then(response => {
          this.data = response.data
        })
        .catch(e => {
          this.error = e
        })
      this.$refs.file.value = ''
    },
    download: function () {
      this.filename = ''
      HTTP.post(
        `DownloadConversionForecast/`,
        {
          data: this.data
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
