<template>
    <div>
        <h2>Запросы</h2>
        <div class="large-12 cell">
            <button class="button primary" type="button" v-on:click="fetchKeywords">Получить данные по запросам</button>
        </div>
        <div class="keywords" v-if="isLoading || isLoaded">
            <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="error-text">
            <p>Ошибка получения данных с сервера:</p>
            <p>{{error}}</p>
          </div>
          <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
          <div v-if="isLoaded && !isLoading">
              <table class="unstriped">
                  <thead>
                      <tr>
                          <th>Ключевое слово</th>
                          <th>Регион</th>
                          <th>ПС</th>
                          <th class="text-right">Кол-во конкурентов в топ&nbsp;{{maxPos}}</th>
                  </thead>
                  <tbody>
                    <tr v-for="keyword in data" :key="keyword.id + keyword.regionName + keyword.searchEngine">
                        <td><a v-on:click="showModal(keyword)">{{keyword.keyword}}</a></td>
                        <td>{{keyword.regionName}}</td>
                        <td>{{getSearchEngineName(keyword.searchEngine)}}</td>
                        <td class="text-right">{{keyword.rivalsCount}}</td>
                    </tr>
                  </tbody>
              </table>
          </div>
          <sermModal v-if="modalData['isModalShown']" v-bind="modalData" v-on:hidemodal="hideModal"></sermModal>
          <keywordsToRemove v-if="isLoaded && !isLoading" v-bind="exportData"></keywordsToRemove>
        </div>
    </div>
</template>

<script>
import { HTTP } from '../api/api.js'
import KeywordsToRemove from '@/components/KeywordsToRemove'
import SermModal from '@/components/SermModal'

export default {
  name: 'Keywords',
  components: {
    keywordsToRemove: KeywordsToRemove,
    sermModal: SermModal
  },
  props: ['keywords', 'rivals', 'maxPos', 'startDate', 'keywordsStr', 'regionsStr', 'regions', 'minCountInSerm', 'offerid', 'sqiDiffCoef', 'minKeywordRivals', 'maxRivalsCount'],
  data () {
    return {
      data: {},
      notRivals: [],
      errors: [],
      isLoaded: false,
      isLoading: false,
      isModalShown: false,
      modalData: {'isModalShown': false}
    }
  },
  computed: {
    exportData: function () {
      var exportData = {}
      exportData['maxPos'] = this.maxPos
      exportData['minCountInSerm'] = this.minCountInSerm
      exportData['keywords'] = this.data
      exportData['regions'] = this.regions
      exportData['rivals'] = this.rivals
      exportData['offerid'] = this.offerid
      exportData['sqiDiffCoef'] = this.sqiDiffCoef
      exportData['minKeywordRivals'] = this.minKeywordRivals
      exportData['maxRivalsCount'] = this.maxRivalsCount
      return exportData
    }
  },
  methods: {
    fetchKeywords: function () {
      this.errors = []
      this.isLoading = true
      HTTP.post(`GetKeywordsRivals/`, {
        keywords: this.keywords,
        rivals: this.rivals,
        maxPos: this.maxPos,
        startDate: this.startDate,
        keywordsStr: this.keywordsStr,
        regionsStr: this.regionsStr,
        regions: this.regions,
        minCountInSerm: this.minCountInSerm,
        offerid: this.offerid
      })
        .then(response => {
          this.data = response.data.keywords
          this.notRivals = response.data.notRivals
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
    getSearchEngineName: function (searchEngine) {
      if (searchEngine === 1) {
        return 'Яндекс'
      } else if (searchEngine === 2) {
        return 'Google'
      }
      return '—'
    },
    showModal: function (keyword) {
      this.modalData = keyword
      this.modalData['maxPos'] = this.maxPos
      this.modalData['startDate'] = this.startDate
      this.modalData['rivals'] = this.rivals
      this.modalData['seName'] = this.getSearchEngineName(keyword['searchEngine'])
      this.modalData['regions'] = this.regions
      this.modalData['notRivals'] = this.notRivals
      this.modalData['isModalShown'] = true
    },
    hideModal: function () {
      this.modalData = {'isModalShown': false}
    }
  }
}
</script>

<style>
  .error-text {
    color: crimson;
  }
</style>
