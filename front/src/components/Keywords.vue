<template>
    <div>
        <h2>Запросы</h2>
        <div class="large-12 cell">
            <button v-bind:disabled="isLoading" class="button primary" type="button" v-on:click="fetchKeywords">Получить данные по запросам</button>
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
                    <tr v-for="keyword in keywordsWithData" :key="keyword.id + keyword.regionName + keyword.searchEngine">
                        <td><a v-on:click="showModal(keyword)">{{keyword.keyword}}</a></td>
                        <td>{{keyword.regionName}}</td>
                        <td>{{getSearchEngineName(keyword.searchEngine)}}</td>
                        <td class="text-right">{{keyword.rivalsCount}}</td>
                    </tr>
                  </tbody>
              </table>
          </div>
          <sermModal v-if="modalData['isModalShown']" v-bind="modalData" v-on:hidemodal="hideModal"></sermModal>
          <keywordsToRemove v-if="isLoaded && !isLoading"></keywordsToRemove>
        </div>
    </div>
</template>

<script>
import KeywordsToRemove from '@/components/KeywordsToRemove'
import SermModal from '@/components/SermModal'

export default {
  name: 'Keywords',
  components: {
    keywordsToRemove: KeywordsToRemove,
    sermModal: SermModal
  },
  data () {
    return {
      isModalShown: false,
      modalData: {'isModalShown': false}
    }
  },
  computed: {
    errors: {
      get () {
        return this.$store.state.keywordsState.errors
      },
      set (value) {
        var keywordsState = this.$store.state.keywordsState
        keywordsState.errors = value
        this.$store.commit('updateStore', {'name': 'keywordsState', 'value': keywordsState})
      }
    },
    isLoaded: {
      get () {
        return this.$store.state.keywordsState.isLoaded
      },
      set (value) {
        var keywordsState = this.$store.state.keywordsState
        keywordsState.isLoaded = value
        this.$store.commit('updateStore', {'name': 'keywordsState', 'value': keywordsState})
      }
    },
    isLoading: {
      get () {
        return this.$store.state.keywordsState.isLoading
      },
      set (value) {
        var keywordsState = this.$store.state.keywordsState
        keywordsState.isLoading = value
        this.$store.commit('updateStore', {'name': 'keywordsState', 'value': keywordsState})
      }
    },
    keywordsWithData: {
      get () {
        return this.$store.state.keywordsWithData
      }
    }
  },
  methods: {
    fetchKeywords: function () {
      this.errors = []
      this.isLoading = true
      this.$store.dispatch('getKeywords')
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
      this.modalData['maxPos'] = this.$store.state.maxPos
      this.modalData['startDate'] = this.$store.state.startDate
      this.modalData['rivals'] = this.$store.state.rivals
      this.modalData['seName'] = this.getSearchEngineName(keyword['searchEngine'])
      this.modalData['regions'] = this.$store.state.regions
      this.modalData['notRivals'] = this.$store.state.notRivals
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
