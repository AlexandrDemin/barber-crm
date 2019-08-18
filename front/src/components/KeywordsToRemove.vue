<template>
    <div>
        <h2>Запросы для удаления</h2>
        <div class="large-12 cell">
            <label>Минимальное количество конкурентов</label>
            <input v-bind:disabled="isLoading" v-model="minKeywordRivals" type="text" autocomplete="on" v-on:keyup.enter="fetchKeywordsToRemove"/>
        </div>
        <div class="large-12 cell">
            <button v-bind:disabled="isLoading" class="button primary" type="button" v-on:click="fetchKeywordsToRemove">Получить запросы с количеством конкурентов меньше {{this.$store.state.minKeywordRivals}} </button>
        </div>
        <div class="keywordsToRemove" v-if="isLoading || isLoaded">
            <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="error-text">
            <p>Ошибка получения данных с сервера:</p>
            <p>{{error}}</p>
          </div>
          <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
          <div v-if="isLoaded && !isLoading">
              <div v-for="region in keywordsToRemove" v-bind:key="region.region" class="large-12 cell">
                  <label>{{region.region}}</label>
                  <textarea rows="10" :value="region.keywordsToDelete.join('\n')"></textarea>
              </div>
              <p v-if="keywordsToRemove.length === 0">Нет запросов для удаления.</p>
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
  data () {
    return {
      filename: ''
    }
  },
  computed: {
    errors: {
      get () {
        return this.$store.state.keywordsToRemoveState.errors
      },
      set (value) {
        var keywordsToRemoveState = this.$store.state.keywordsToRemoveState
        keywordsToRemoveState.errors = value
        this.$store.commit('updateStore', {'name': 'keywordsToRemoveState', 'value': keywordsToRemoveState})
      }
    },
    isLoaded: {
      get () {
        return this.$store.state.keywordsToRemoveState.isLoaded
      },
      set (value) {
        var keywordsToRemoveState = this.$store.state.keywordsToRemoveState
        keywordsToRemoveState.isLoaded = value
        this.$store.commit('updateStore', {'name': 'keywordsToRemoveState', 'value': keywordsToRemoveState})
      }
    },
    isLoading: {
      get () {
        return this.$store.state.keywordsToRemoveState.isLoading
      },
      set (value) {
        var keywordsToRemoveState = this.$store.state.keywordsToRemoveState
        keywordsToRemoveState.isLoading = value
        this.$store.commit('updateStore', {'name': 'keywordsToRemoveState', 'value': keywordsToRemoveState})
      }
    },
    minKeywordRivals: {
      get () {
        return this.$store.state.minKeywordRivals
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'minKeywordRivals', 'value': value})
      }
    },
    keywordsToRemove: {
      get () {
        return this.$store.state.keywordsToRemove
      }
    }
  },
  methods: {
    fetchKeywordsToRemove: function () {
      this.errors = []
      this.isLoading = true
      this.$store.dispatch('getKeywordsToRemove')
    },
    exportToExcel: function () {
      this.filename = ''
      HTTP.post(`ExportToExcel/`, {
        keywords: this.$store.state.keywordsWithData,
        regions: this.$store.state.regions,
        rivals: this.$store.state.rivals,
        offerid: this.$store.state.offerid,
        maxRivalsCount: this.$store.state.maxRivalsCount,
        sqiDiffCoef: this.$store.state.sqiDiffCoef,
        maxPos: this.$store.state.maxPos,
        minCountInSerm: this.$store.state.minCountInSerm,
        minKeywordRivals: this.$store.state.minKeywordRivals,
        keywordsToRemove: this.$store.state.keywordsToRemove
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
