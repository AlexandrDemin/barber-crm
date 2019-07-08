<template>
    <div>
        <h2>Запросы для удаления</h2>
        <div class="large-12 cell">
            <label>Минимальное количество конкурентов</label>
            <input v-model="minKeywordRivals" type="text" autocomplete="on" v-on:keyup.enter="fetchKeywordsToRemove"/>
        </div>
        <div class="large-12 cell">
            <button class="button primary" type="button" v-on:click="fetchKeywordsToRemove">Получить запросы с количеством конкурентов меньше {{minKeywordRivals}} </button>
        </div>
        <div class="keywordsToRemove" v-if="isLoading || isLoaded">
            <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="error-text">
            <p>Ошибка получения данных с сервера:</p>
            <p>{{error}}</p>
          </div>
          <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
          <div v-if="isLoaded && !isLoading">
              <div v-for="region in data" v-bind:key="region.region" class="large-12 cell">
                  <label>{{region.region}}</label>
                  <textarea rows="10" :value="region.keywordsToDelete.join('\n')"></textarea>
              </div>
              <p v-if="data.length === 0">Нет запросов для удаления.</p>
              <div class="large-12 cell">
                  <button class="button primary" type="button" v-on:click="exportToExcel">Выгрузить в .xlsx</button>
              </div>
              <iframe v-if="filename.length > 0" :src="'download/' + filename" style='display: none;'></iframe>
          </div>
        </div>
    </div>
</template>

<script>
import { HTTP } from '../api/api.js'

export default {
  name: 'KeywordsToRemove',
  props: ['keywords', 'regions', 'rivals', 'offerid', 'maxRivalsCount', 'sqiDiffCoef', 'maxPos', 'minCountInSerm'],
  data () {
    return {
      data: {},
      errors: [],
      isLoaded: false,
      isLoading: false,
      minKeywordRivals: 5,
      filename: ''
    }
  },
  methods: {
    fetchKeywordsToRemove: function () {
      this.errors = []
      this.isLoading = true
      HTTP.post(`GetKeywordsToRemove/`, {
        keywords: this.keywords,
        regions: this.regions,
        minKeywordRivals: this.minKeywordRivals
      })
        .then(response => {
          this.data = response.data
          if (typeof response.data === 'string') {
            this.data = JSON.parse(response.data)
          }
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
    },
    exportToExcel: function () {
      this.filename = ''
      HTTP.post(`ExportToExcel/`, {
        keywords: this.keywords,
        regions: this.regions,
        rivals: this.rivals,
        offerid: this.offerid,
        maxRivalsCount: this.maxRivalsCount,
        sqiDiffCoef: this.sqiDiffCoef,
        maxPos: this.maxPos,
        minCountInSerm: this.minCountInSerm,
        minKeywordRivals: this.minKeywordRivals,
        keywordsToDelete: this.data
      })
        .then(response => {
          this.filename = response.data
        })
        .catch(e => {
          alert(e)
        })
    }
  }
}
</script>

<style>
  .error-text {
    color: crimson;
  }
</style>
