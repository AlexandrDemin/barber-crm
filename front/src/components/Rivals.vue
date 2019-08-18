<template>
  <div class="main grid-container">
    <h1>Фильтрация запросов по количеству конкурентов</h1>
    <form class="rivals-form">
        <div class="large-12 cell">
            <label>
                ID КП или ссылка
                <br>
                <small>Например, <a @click="setOfferUrl('http://client.ingate.ru/Offers/offer/5d56807f7e76808f64a3b555/keywords')">
                    http://client.ingate.ru/Offers/offer/5d56807f7e76808f64a3b555/keywords
                </a>
                </small>
            </label>
            <input v-bind:disabled="isLoading" v-model="offerUrl" type="text" autofocus="autofocus" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Не считать конкурентом, если встречается в выдаче реже этого числа раз</label>
            <input v-bind:disabled="isLoading" v-model="minCountInSerm" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальное количество конкурентов</label>
            <input v-bind:disabled="isLoading" v-model="maxRivalsCount" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальное отклонение Яндекс ИКС конкурентов (количество раз)</label>
            <input v-bind:disabled="isLoading" v-model="sqiDiffCoef" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальная позиция для поиска конкурентов</label>
            <input v-bind:disabled="isLoading" v-model="maxPos" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="callout alert" v-if="!isValid">
          Необходимо указать ID или ссылку на КП
          <button href="#" class="close-button" v-on:click="makeValid">&times;</button>
        </div>
        <div class="large-12 cell">
            <button v-bind:disabled="isLoading" class="button primary" type="button" v-on:click="validateAndFetch">Получить данные по конкурентам</button>
        </div>
    </form>
    <div class="rivals" v-if="isLoading || isLoaded">
      <h2>Конкуренты</h2>
      <div v-if="isLoaded && errors.length > 0" v-for="error in errors" :key="error" class="error-text">
        <p>Ошибка получения данных с сервера:</p>
        <p>{{error}}</p>
      </div>
      <p v-if="isLoading">Загрузка...<br>Получение данных может занять несколько минут.</p>
      <div v-if="isLoaded && !isLoading">
          <div v-for="rival in rivals" :key="rival.domain">
              <div v-if="rival.isOfferDomain">
                  <p>Домен КП: <a :href="'http://' + rival.domain" target="_blank">{{rival.domain}}</a></p>
                  <p>Встречается в топ {{maxPos}}: {{rival.countInSerm}}</p>
                  <p>Яндекс ИКС: {{rival.sqi[0]}}</p>
                  <p>Данные только по десктопной выдаче.</p>
              </div>
          </div>
          <table class="unstriped">
              <thead>
                  <tr>
                      <th>Сайт</th>
                      <th class="text-right">Не&nbsp;конкурент&nbsp;<input type="checkbox" v-on:input="toggleAllisExcluded" id="toggle-all"></th>
                      <th class="text-right">Встречается в топ {{maxPos}}</th>
                      <th class="text-right">Яндекс ИКС</th>
                      <th class="text-right">Отклонение ИКС от сайта КП</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-if="!rival.isOfferDomain" v-for="rival in rivals" :key="rival.title + rival.domain">
                    <td>
                        <a :href="'http://' + rival.domain" target="_blank"><img width="16" height="16" :src="rival.icon">&nbsp;{{rival.domain}}</a>
                        <br>
                        {{rival.title}}
                        <br>
                        <small>{{rival.description}}</small>
                    </td>
                    <td class="text-right checkbox-td"><label class="checkbox-padding"><input type="checkbox" v-bind:checked="rival.isExcluded" v-on:change="updateRivalIsExcluded(rival)"></label></td>
                    <td class="text-right">{{rival.countInSerm}}</td>
                    <td class="text-right">{{rival.sqi[0]}}</td>
                    <td class="text-right">{{rival.sqiDiff.toFixed(2)}}</td>
                </tr>
              </tbody>
          </table>
      </div>
    </div>
    <keywords v-if="isLoaded && !isLoading"></keywords>
  </div>
</template>

<script>
import Keywords from '@/components/Keywords'

export default {
  name: 'Rivals',
  components: {
    keywords: Keywords
  },
  data () {
    return {
      offerUrl: this.$route.params.offerid
    }
  },
  mounted: function () {
    if (this.$route.params.offerid) {
      var offerid = this.$route.params.offerid
      this.offerid = offerid
      this.isLoading = true
      this.$store.dispatch('loadData', offerid)
    }
  },
  computed: {
    errors: {
      get () {
        return this.$store.state.rivalsState.errors
      },
      set (value) {
        var rivalsState = this.$store.state.rivalsState
        rivalsState.errors = value
        this.$store.commit('updateStore', {'name': 'rivalsState', 'value': rivalsState})
      }
    },
    isValid: {
      get () {
        return this.$store.state.rivalsState.isValid
      },
      set (value) {
        var rivalsState = this.$store.state.rivalsState
        rivalsState.isValid = value
        this.$store.commit('updateStore', {'name': 'rivalsState', 'value': rivalsState})
      }
    },
    isLoaded: {
      get () {
        return this.$store.state.rivalsState.isLoaded
      },
      set (value) {
        var rivalsState = this.$store.state.rivalsState
        rivalsState.isLoaded = value
        this.$store.commit('updateStore', {'name': 'rivalsState', 'value': rivalsState})
      }
    },
    isLoading: {
      get () {
        return this.$store.state.rivalsState.isLoading
      },
      set (value) {
        var rivalsState = this.$store.state.rivalsState
        rivalsState.isLoading = value
        this.$store.commit('updateStore', {'name': 'rivalsState', 'value': rivalsState})
      }
    },
    maxRivalsCount: {
      get () {
        return this.$store.state.maxRivalsCount
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'maxRivalsCount', 'value': value})
      }
    },
    sqiDiffCoef: {
      get () {
        return this.$store.state.sqiDiffCoef
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'sqiDiffCoef', 'value': value})
      }
    },
    maxPos: {
      get () {
        return this.$store.state.maxPos
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'maxPos', 'value': value})
      }
    },
    minCountInSerm: {
      get () {
        return this.$store.state.minCountInSerm
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'minCountInSerm', 'value': value})
      }
    },
    offerid: {
      get () {
        return this.$store.state.offerid
      },
      set (value) {
        this.$store.commit('updateStore', {'name': 'offerid', 'value': value})
      }
    },
    rivals: {
      get () {
        return this.$store.state.rivals
      }
    }
  },
  watch: {
    offerUrl () {
      var offerid = this.offerUrl
      if (offerid && offerid.slice(0, 7) === 'http://') {
        offerid = offerid.slice(7, offerid.length).split('/')[3]
      } else if (offerid && offerid.includes('/')) {
        offerid = offerid.split('/')[3]
      }
      this.offerid = offerid
    },
    '$route' (to, from) {
      this.offerUrl = this.$route.params.offerid
    }
  },
  methods: {
    validateAndFetch: function () {
      this.errors = []
      if (this.offerid.length > 0) {
        this.isValid = true
        this.isLoading = true
        this.$router.replace('/' + this.offerid)
        this.$store.dispatch('getRivals')
      } else {
        this.isValid = false
        this.isLoading = false
      }
    },
    makeValid: function () {
      this.isValid = true
    },
    setOfferUrl: function (offerUrl) {
      this.offerUrl = offerUrl
    },
    updateRivalIsExcluded: function (rival) {
      rival.isExcluded = !rival.isExcluded
      this.$store.commit('updateRival', rival)
    },
    toggleAllisExcluded: function (e) {
      var isChecked = e.target.checked
      this.$store.dispatch('toggleAllisExcluded', isChecked)
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
  .checkbox-td {
    overflow: hidden;
  }
  .checkbox-padding {
    padding: 200px;
    margin: -200px;
    transition: 0.2s;
  }
  .checkbox-padding input[type=checkbox] {
    margin: 0;
  }
  .checkbox-padding:hover {
    background: #fafafa;
    cursor: pointer;
  }
</style>
