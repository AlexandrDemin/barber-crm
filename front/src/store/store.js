import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    projectsState: {
      errors: [],
      isLoaded: false,
      isLoading: false,
      projects: []
    },
    projectState: {
      errors: [],
      isLoaded: false,
      isLoading: false,
      project: null
    }
  },
  getters: {
    getStatusColor: (state) => (status) => {
      if (status === 'active') {
        return '#69E2B2'
      }
      return '#DCE0E5'
    },
    getStatusText: (state) => (status) => {
      if (status === 'active') {
        return 'Активен'
      }
      return 'Остановлен'
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
      context.commit('updateStore', {
        'name': 'projectsState',
        'value': {
          errors: [],
          isLoaded: false,
          isLoading: true,
          projects: []
        }
      })
      HTTP.post(`GetProjects/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'projectsState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false,
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
              isLoading: false
            }
          })
        })
    },
    getProject (context, projectId) {
      context.commit('updateStore', {
        'name': 'projectState',
        'value': {
          errors: [],
          isLoaded: false,
          isLoading: true,
          project: {}
        }
      })
      HTTP.post(`GetProject/`, {
        'projectId': projectId
      })
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'projectState',
            'value': {
              errors: [],
              isLoaded: true,
              isLoading: false,
              project: data
            }
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'projectState',
            'value': {
              errors: [e],
              isLoaded: true,
              isLoading: false,
              project: {}
            }
          })
        })
    }
  }
})
