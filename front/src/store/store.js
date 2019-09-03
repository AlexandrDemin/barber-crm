import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    projectsState: {
      errors: [],
      isValid: true,
      isLoaded: false,
      isLoading: false,
      projects: []
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
    }
  },
  actions: {
    getProjects (context) {
      HTTP.post(`GetProjects/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'projectsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false,
              isValid: true,
              projects: data
            }
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'projectsState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false,
              isValid: true
            }
          })
        })
    }
  }
})
