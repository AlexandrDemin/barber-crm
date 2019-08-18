import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    offerid: '',
    maxRivalsCount: 100000,
    sqiDiffCoef: 100,
    maxPos: 10,
    minCountInSerm: 6,
    rivals: [],
    startDate: '',
    keywordsStr: '',
    regionsStr: '',
    notRivals: [],
    keywords: [],
    regions: [],
    keywordsWithData: [],
    minKeywordRivals: 2,
    keywordsToRemove: {},
    rivalsState: {
      errors: [],
      isValid: true,
      isLoaded: false,
      isLoading: false
    },
    keywordsState: {
      errors: [],
      isLoaded: false,
      isLoading: false
    },
    keywordsToRemoveState: {
      errors: [],
      isLoaded: false,
      isLoading: false
    }
  },
  mutations: {
    updateStore (state, payload) {
      state[payload.name] = payload.value
    },
    updateIfExists (state, payload) {
      var data = payload.data
      var key = payload.key
      if (data[key]) {
        state[key] = data[key]
      }
    },
    updateRival (state, rival) {
      var rivals = state.rivals
      var rivalKey = 0
      for (var key in rivals) {
        if (rivals[key].domain === rival.domain) {
          rivalKey = key
          break
        }
      }
      Vue.set(rivals, rivalKey, rival)
    }
  },
  actions: {
    loadData (context, offerid) {
      HTTP.post(`LoadData/`, {
        offerid: offerid
      })
        .then(response => {
          var data = response.data
          context.commit('updateIfExists', {'data': data, 'key': 'rivals'})
          context.commit('updateIfExists', {'data': data, 'key': 'keywords'})
          context.commit('updateIfExists', {'data': data, 'key': 'startDate'})
          context.commit('updateIfExists', {'data': data, 'key': 'keywordsStr'})
          context.commit('updateIfExists', {'data': data, 'key': 'regionsStr'})
          context.commit('updateIfExists', {'data': data, 'key': 'regions'})
          context.commit('updateIfExists', {'data': data, 'key': 'offerid'})
          context.commit('updateIfExists', {'data': data, 'key': 'keywordsWithData'})
          context.commit('updateIfExists', {'data': data, 'key': 'keywordsToRemove'})
          context.commit('updateIfExists', {'data': data, 'key': 'minKeywordRivals'})
          context.commit('updateIfExists', {'data': data, 'key': 'notRivals'})
          context.commit('updateIfExists', {'data': data, 'key': 'maxRivalsCount'})
          context.commit('updateIfExists', {'data': data, 'key': 'sqiDiffCoef'})
          context.commit('updateIfExists', {'data': data, 'key': 'maxPos'})
          context.commit('updateIfExists', {'data': data, 'key': 'minCountInSerm'})
          context.commit('updateStore', {
            'name': 'rivalsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false,
              isValid: true
            }
          })
          context.commit('updateStore', {
            'name': 'keywordsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false
            }
          })
          context.commit('updateStore', {
            'name': 'keywordsToRemoveState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false
            }
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'rivalsState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false,
              isValid: true
            }
          })
        })
      return true
    },
    getRivals (context) {
      context.commit('updateStore', {
        'name': 'keywordsState',
        'value': {
          errors: [],
          isLoaded: false,
          isLoading: false
        }
      })
      context.commit('updateStore', {
        'name': 'keywordsToRemoveState',
        'value': {
          errors: [],
          isLoaded: false,
          isLoading: false
        }
      })
      HTTP.post(`GetRivals/`, {
        offerid: context.state.offerid,
        maxRivalsCount: context.state.maxRivalsCount,
        sqiDiffCoef: context.state.sqiDiffCoef,
        maxPos: context.state.maxPos,
        minCountInSerm: context.state.minCountInSerm
      })
        .then(response => {
          var data = response.data
          context.commit('updateStore', {'name': 'rivals', 'value': data.rivals})
          context.commit('updateStore', {'name': 'keywords', 'value': data.keywords})
          context.commit('updateStore', {'name': 'startDate', 'value': data.startDate})
          context.commit('updateStore', {'name': 'keywordsStr', 'value': data.keywordsStr})
          context.commit('updateStore', {'name': 'regionsStr', 'value': data.regionsStr})
          context.commit('updateStore', {'name': 'regions', 'value': data.regions})
          context.commit('updateStore', {'name': 'offerid', 'value': data.offerid})
          context.commit('updateStore', {
            'name': 'rivalsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false,
              isValid: true
            }
          })
          for (var index in data['rivals']) {
            var domain = data['rivals'][index]['domain']
            HTTP.post(`GetDomainInfo/`, {
              domain: domain
            })
              .then(response => {
                var res = response.data
                var domain = res['domain']
                var rivals = data['rivals']
                for (index in rivals) {
                  var rival = rivals[index]
                  if (rival['domain'] === domain) {
                    rival['title'] = res['title']
                    rival['description'] = res['description']
                    rival['icon'] = res['icon']
                    context.commit('updateRival', rival)
                  }
                }
              })
          }
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'rivalsState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false,
              isValid: true
            }
          })
        })
    },
    getKeywords (context) {
      context.commit('updateStore', {
        'name': 'keywordsToRemoveState',
        'value': {
          errors: [],
          isLoaded: false,
          isLoading: false
        }
      })
      HTTP.post(`GetKeywordsRivals/`, {
        keywords: context.state.keywords,
        rivals: context.state.rivals,
        maxPos: context.state.maxPos,
        startDate: context.state.startDate,
        keywordsStr: context.state.keywordsStr,
        regionsStr: context.state.regionsStr,
        regions: context.state.regions,
        minCountInSerm: context.state.minCountInSerm,
        offerid: context.state.offerid
      })
        .then(response => {
          context.commit('updateStore', {'name': 'keywordsWithData', 'value': response.data.keywords})
          context.commit('updateStore', {'name': 'notRivals', 'value': response.data.notRivals})
          context.commit('updateStore', {
            'name': 'keywordsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false
            }
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'keywordsState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false
            }
          })
        })
    },
    getKeywordsToRemove (context) {
      HTTP.post(`GetKeywordsToRemove/`, {
        keywords: context.state.keywordsWithData,
        regions: context.state.regions,
        minKeywordRivals: context.state.minKeywordRivals,
        offerid: context.state.offerid
      })
        .then(response => {
          var data = response.data
          if (typeof response.data === 'string') {
            data = JSON.parse(response.data)
          }
          context.commit('updateStore', {'name': 'keywordsToRemove', 'value': data})
          context.commit('updateStore', {
            'name': 'keywordsToRemoveState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false
            }
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'keywordsToRemoveState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false
            }
          })
        })
    },
    toggleAllisExcluded (context, isChecked) {
      var rivals = context.state.rivals
      for (var index in rivals) {
        rivals[index].isExcluded = isChecked
      }
      context.commit('updateStore', {'name': 'rivals', 'value': rivals})
    }
  }
})
