import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    services: [
      {
        'Id': 1,
        'name': 'Стрижка мужская',
        'prices': {
          1: 600
        }
      },
      {
        'Id': 2,
        'name': 'Стрижка женская',
        'prices': {
          1: 1000
        }
      },
      {
        'Id': 3,
        'name': 'Укладка',
        'prices': {
          1: 300
        }
      },
      {
        'Id': 4,
        'name': 'Маникюр',
        'prices': {
          1: 300
        }
      },
      {
        'Id': 5,
        'name': 'Стрижка усов и бороды',
        'prices': {
          1: 300
        }
      }
    ],
    goods: [
      {
        'Id': 1,
        'name': 'Восстанавливающая маска для поврежденных волос Ggongji Hair Pack 8мл',
        'price': 1000
      },
      {
        'Id': 2,
        'name': 'Лак для волос сильной фиксации Mugens Impressive Control Hard Spray 300мл',
        'price': 200
      },
      {
        'Id': 3,
        'name': 'Эссенция для волос Around Me Rose Hip Perfume Water Essence 200мл',
        'price': 200
      },
      {
        'Id': 4,
        'name': 'Murray\'s eXelento Pomad - Помада для укладки волос',
        'price': 200
      },
      {
        'Id': 5,
        'name': 'Baxter of California Pomade: Cream - Средство для укладки волос 60 мл',
        'price': 200
      }
    ],
    employeePaymentTypes: [
      {
        'id': 1,
        'name': 'Расход',
        'sum': 500
      },
      {
        'id': 2,
        'name': 'Штраф',
        'sum': 500
      },
      {
        'id': 1,
        'name': 'Премия',
        'sum': 1000
      }
    ],
    spendTypes: [
      {
        'id': 1,
        'name': 'Вывоз мусора',
        'sum': 600
      },
      {
        'id': 2,
        'name': 'Прочие расходы',
        'sum': 1000
      }
    ]
  },
  getters: {
    getEmployeeName: (state) => (status) => {
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
