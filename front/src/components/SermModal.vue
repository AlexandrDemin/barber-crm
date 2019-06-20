<template>
    <div class="reveal-overlay" style="display: block;">
        <div class="reveal large" style="display:block">
          <h1>Выдача по запросу</h1>
          <p>Запрос: {{keyword}}</p>
          <p>Регион: {{regionName}}</p>
          <p>ПС: {{seName}}</p>
          <p>Кол-во конкурентов: {{rivalsCount}}</p>
          <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
          <div v-if="isLoaded && !isLoading">
              <p v-if="data.length === 0">Не найдено ни одного результата выдачи.</p>
              <table v-if="data.length > 0" class="unstriped">
                  <thead>
                      <th>Позиция</th>
                      <th>Домен</th>
                      <th>Страница в выдаче</th>
                      <th>Конкурент</th>
                  </thead>
                  <tbody>
                      <tr v-for="pos in data" :key="pos.position + pos.domain" v-bind:class="getTableClass(pos.isExcluded)">
                          <td>{{pos.position}}</td>
                          <td><a :href="'http://'+pos.domain" target="_blank">{{pos.domain}}</a></td>
                          <td><a :href="pos.foundUrl" target="_blank">{{pos.foundUrl}}</a></td>
                          <td>{{getIsRivalText(pos.isExcluded)}}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <button class="close-button" type="button" v-on:click="hideModal">
            <span>&times;</span>
          </button>
        </div>
    </div>
</template>

<script>
import { HTTP } from '../api/api.js'

export default {
  name: 'SermModal',
  props: ['keyword', 'regionName', 'searchEngine', 'rivalsCount', 'regionId', 'seName', 'isMobile', 'maxPos', 'startDate', 'rivals', 'regions', 'notRivals'],
  data () {
    return {
      data: [],
      errors: [],
      isLoaded: false,
      isLoading: false
    }
  },
  mounted: function () {
    this.errors = []
    this.isLoading = true
    HTTP.post(`GetSerm/`, {
      keyword: this.keyword,
      regionId: this.regionId,
      searchEngine: this.searchEngine,
      isMobile: this.isMobile,
      maxPos: this.maxPos,
      startDate: this.startDate,
      rivals: this.rivals,
      regions: this.regions,
      notRivals: this.notRivals
    })
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
  },
  methods: {
    getIsRivalText: function (isExcluded) {
      if (isExcluded) {
        return 'Нет'
      }
      return 'Да'
    },
    hideModal: function () {
      this.$emit('hidemodal')
    },
    getTableClass: function (isExcluded) {
      return {
        'dark-background': isExcluded
      }
    }
  }
}
</script>

<style>
  .error-text {
    color: crimson;
  }
  .dark-background {
    background: #f1f1f1 !important;
  }
</style>
