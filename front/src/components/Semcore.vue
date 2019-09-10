<template>
  <div class="main grid-container fluid">
    <breadcrumbs v-bind="{'header': 'Генерация семантического ядра', 'crumbs': [{'text': 'Мои проекты', 'link': ''}, {'text': project.domain, 'link': '#/project/' + project.projectId}]}"></breadcrumbs>
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
                <label>Приоритетные направления</label>
                <textarea rows="5" v-bind:disabled="generating" v-model="priority" autofocus="autofocus" autocomplete="on" v-on:keyup.enter="startGeneration"></textarea>
            </div>
            <div class="large-12 cell">
                <label>Регионы</label>
                <select v-bind:disabled="generating" v-model="selectedRegion">
                  <option
                    v-for="region in regions"
                    v-bind:key="region.id"
                    v-bind:value="region.id"
                    :selected="region.id == selectedRegion"
                  >
                    {{region.name}}
                  </option>
                </select>
            </div>
            <div class="large-12 cell">
                <label>Максимальное количество запросов</label>
                <input v-bind:disabled="generating" v-model="maxQueries" type="text" autocomplete="on" v-on:keyup.enter="startGeneration"/>
            </div>
            <div class="large-12 cell">
                <label>Минус-слова</label>
                <textarea rows="5" v-bind:disabled="generating" v-model="minusWords"></textarea>
            </div>
            <div class="large-12 cell">
                <label>Минус-фразы</label>
                <textarea rows="5" v-bind:disabled="generating" v-model="minusPhrases"></textarea>
            </div>
            <div class="large-12 cell">
                <button v-bind:disabled="generating" class="button primary" type="button" v-on:click="startGeneration">Запустить генерацию</button>
            </div>
        </form>
        <div class="cell small-12" v-if="generating || isGenerated">
          <h3>Семантическое ядро</h3>
          <p v-if="generating">Семантическое ядро генерируется. Это займёт около часа. Пожалуйста, не закрывайте эту вкладку браузера.</p>
          <p v-if="semCore && generationEnded">
            Дата генерации: {{generationEnded}}
            <br>
            Количество запросов: {{semCore.length}}
          </p>
          <button v-if="semCore && isGenerated" class="button primary" type="button" v-on:click="downloadSemCore">Выгрузить в .xlsx</button>
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
  name: 'Semcore',
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
      regions: [
        {
          name: 'Москва',
          id: 3
        },
        {
          name: 'Санкт-Петербург',
          id: 4
        },
        {
          name: 'Россия',
          id: 5
        }
      ],
      priority: '',
      selectedRegion: 3,
      maxQueries: 300,
      minusWords: '',
      minusPhrases: '',
      generationEnded: '',
      semCore: [],
      isGenerated: false,
      error: '',
      filename: ''
    }
  },
  methods: {
    startGeneration: function () {
      this.generating = true
      this.generationEnded = ''
      this.isGenerated = false
      HTTP.post(
        `GetSemcore/`,
        {
          domain: this.project.domain,
          priority: this.priority,
          regions: [this.selectedRegion],
          maxQueries: this.maxQueries,
          minusWords: this.minusWords,
          minusPhrases: this.minusPhrases
        }
      )
        .then(response => {
          this.semCore = response.data
          this.generating = false
          var dateFormatOptions = {
            day: '2-digit',
            year: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
          }
          var now = new Date()
          this.generationEnded = now.toLocaleDateString('ru-RU', dateFormatOptions)
          this.isGenerated = true
        })
        .catch(e => {
          this.error = e
          this.generating = false
          this.generationEnded = ''
          this.isGenerated = true
        })
    },
    downloadSemCore: function () {
      this.filename = ''
      HTTP.post(
        `DownloadSemcore/`,
        {
          semCore: this.semCore
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
