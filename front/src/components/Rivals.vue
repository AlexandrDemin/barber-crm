<template>
  <div class="main grid-container">
    <h1>Фильтрация запросов по количеству конкурентов</h1>
    <form class="rivals-form">
        <div class="large-12 cell">
            <label>
                Ссылка на КП
                <br>
                <small>Например, <a @click="setOfferUrl('http://client.ingate.ru/Offers/offer/5cdd6e3d7e76803de48abc1a/keywords')">
                    http://client.ingate.ru/Offers/offer/5cdd6e3d7e76803de48abc1a/keywords
                </a>
                </small>
            </label>
            <input v-model="offerUrl" type="text" autofocus="autofocus" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Не считать конкурентом, если встречается в выдаче реже этого числа раз</label>
            <input v-model="minCountInSerm" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальное количество конкурентов</label>
            <input v-model="maxRivalsCount" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальное отклонение Яндекс ИКС конкурентов (количество раз)</label>
            <input v-model="sqiDiffCoef" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="large-12 cell">
            <label>Максимальная позиция для поиска конкурентов</label>
            <input v-model="maxPos" type="text" autocomplete="on" v-on:keyup.enter="validateAndFetch"/>
        </div>
        <div class="alert-box alert" v-if="!isValid">
          Укажи ссылку на КП.
          <a href="#" class="close" v-on:click="makeValid">&times;</a>
        </div>
        <div class="large-12 cell">
            <button class="button primary" type="button" v-on:click="validateAndFetch">Получить данные по конкурентам</button>
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
          <div v-for="rival in data.rivals" :key="rival.domain">
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
                <tr v-if="!rival.isOfferDomain" v-for="rival in data.rivals" :key="rival.title + rival.domain">
                    <td>
                        <a :href="'http://' + rival.domain" target="_blank"><img width="16" height="16" :src="rival.icon">&nbsp;{{rival.domain}}</a>
                        <br>
                        {{rival.title}}
                        <br>
                        <small>{{rival.description}}</small>
                    </td>
                    <td class="text-right checkbox-td"><label class="checkbox-padding"><input type="checkbox" v-model="rival.isExcluded"></label></td>
                    <td class="text-right">{{rival.countInSerm}}</td>
                    <td class="text-right">{{rival.sqi[0]}}</td>
                    <td class="text-right">{{rival.sqiDiff.toFixed(2)}}</td>
                </tr>
              </tbody>
          </table>
      </div>
    </div>
    <keywords v-if="isLoaded && !isLoading" v-bind="rivalsData"></keywords>
  </div>
</template>

<script>
import { HTTP } from '../api/api.js'
import Keywords from '@/components/Keywords'

export default {
  name: 'Rivals',
  components: {
    keywords: Keywords
  },
  data () {
    return {
      data: {},
      errors: [],
      isValid: true,
      isLoaded: false,
      isLoading: false,
      offerUrl: 'http://client.ingate.ru/Offers/offer/5d0cc9587e76801f38a88cd0/keywords',
      maxRivalsCount: 100000,
      sqiDiffCoef: 100,
      maxPos: 10,
      minCountInSerm: 6
    }
  },
  computed: {
    rivalsData: function () {
      var rivalsData = this.data
      rivalsData['maxPos'] = this.maxPos
      rivalsData['minCountInSerm'] = this.minCountInSerm
      rivalsData['sqiDiffCoef'] = this.sqiDiffCoef
      rivalsData['minKeywordRivals'] = this.minKeywordRivals
      rivalsData['maxRivalsCount'] = this.maxRivalsCount
      return rivalsData
    }
  },
  methods: {
    validateAndFetch: function () {
      this.errors = []
      if (this.offerUrl.length > 0) {
        this.isValid = true
        this.isLoading = true
        HTTP.post(`GetRivals/`, {
          offerUrl: this.offerUrl,
          maxRivalsCount: this.maxRivalsCount,
          sqiDiffCoef: this.sqiDiffCoef,
          maxPos: this.maxPos,
          minCountInSerm: this.minCountInSerm
        })
          .then(response => {
            this.data = response.data
            this.errors = []
            this.isLoaded = true
            this.isLoading = false
            for (var index in this.data['rivals']) {
              var domain = this.data['rivals'][index]['domain']
              if (!this.data['rivals'][index]['isOfferDomain']) {
                HTTP.post(`GetDomainInfo/`, {
                  domain: domain
                })
                  .then(response => {
                    var res = response.data
                    var domain = res['domain']
                    var rivals = this.data['rivals']
                    for (index in rivals) {
                      var rival = rivals[index]
                      if (rival['domain'] === domain) {
                        rival['title'] = res['title']
                        rival['description'] = res['description']
                        rival['icon'] = res['icon']
                        this.$set(this.data['rivals'], index, rival)
                      }
                    }
                  })
              }
            }
          })
          .catch(e => {
            this.errors = []
            this.errors.push(e)
            this.isLoaded = true
            this.isLoading = false
          })
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
    toggleAllisExcluded: function (e) {
      var isChecked = e.target.checked
      for (var index in this.data.rivals) {
        var rival = this.data.rivals[index]
        rival.isExcluded = isChecked
        this.$set(this.data.rivals, index, rival)
      }
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
  }
  .checkbox-padding input[type=checkbox] {
    margin: 0;
  }
  .checkbox-padding:hover {
    background: #fafafa;
    cursor: pointer;
  }
</style>
