import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    currentSession: {
      'id': 1,
      'dateOpened': '21.09.2019 09:30',
      'dateClosed': null,
      'employees': [
        {
          'id': 1,
          'name': 'Алексей Луцай',
          'role': 'officeAdmin',
          'pictureUrl': '',
          'workHours': 6
        },
        {
          'id': 2,
          'name': 'Мария Попова',
          'role': 'master',
          'pictureUrl': 'static/user_photos/мария.jpg',
          'workHours': 6
        },
        {
          'id': 3,
          'name': 'Макс Корж',
          'role': 'master',
          'pictureUrl': 'static/user_photos/макс.jpg',
          'workHours': 6
        },
        {
          'id': 4,
          'name': 'Прокофий Иванов',
          'role': 'master',
          'pictureUrl': '',
          'workHours': 6
        }
      ],
      'officeId': 1,
      'state': 'open',
      'operations': [
        {
          'operationType': 'service',
          'sessionId': 1,
          'id': 1,
          'officeId': 1,
          'type': 1,
          'startDatetime': '21.09.2019 09:30',
          'finishDatetime': '21.09.2019 10:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 600,
          'cashlessSum': 0,
          'discountSum': 0,
          'adminBonus': 30,
          'masterBonus': 120,
          'score': null,
          'review': '',
          'photoUrls': [],
          'comment': ''
        },
        {
          'operationType': 'goodSell',
          'id': 2,
          'officeId': 1,
          'sessionId': 1,
          'type': 1,
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
          'amount': 1,
          'adminBonus': 30,
          'masterBonus': 120,
          'comment': ''
        },
        {
          'operationType': 'goodSell',
          'id': 3,
          'officeId': 1,
          'sessionId': 1,
          'type': 2,
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
          'amount': 1,
          'adminBonus': 30,
          'masterBonus': 120,
          'comment': ''
        },
        {
          'operationType': 'goodSell',
          'id': 4,
          'officeId': 1,
          'sessionId': 1,
          'type': 3,
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
          'amount': 1,
          'adminBonus': 30,
          'masterBonus': 120,
          'comment': ''
        },
        {
          'operationType': 'goodSell',
          'id': 5,
          'officeId': 1,
          'sessionId': 1,
          'type': 4,
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
          'amount': 1,
          'adminBonus': 30,
          'masterBonus': 120,
          'comment': ''
        },
        {
          'operationType': 'goodSell',
          'id': 6,
          'officeId': 1,
          'sessionId': 1,
          'type': 5,
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
          'amount': 1,
          'adminBonus': 30,
          'masterBonus': 120,
          'comment': ''
        },
        {
          'operationType': 'spend',
          'id': 2,
          'officeId': 1,
          'sessionId': 1,
          'type': 2,
          'datetime': '21.09.2019 12:44',
          'sum': 600,
          'comment': ''
        },
        {
          'operationType': 'employeePayment',
          'id': 2,
          'officeId': 1,
          'sessionId': 1,
          'employeeId': 4,
          'type': 2,
          'datetime': '21.09.2019 18:22',
          'sum': 600,
          'comment': ''
        }
      ]
    },
    operationTypes: [
      {
        id: 'service',
        name: 'Услуга'
      },
      {
        id: 'goodSell',
        name: 'Продажа товара'
      },
      {
        id: 'spend',
        name: 'Расход'
      },
      {
        id: 'employeePayment',
        name: 'Продажа товара'
      }
    ],
    serviceTypes: [
      {
        'id': 1,
        'name': 'Стрижка мужская',
        'prices': {
          1: 600,
          2: 800
        }
      },
      {
        'id': 2,
        'name': 'Стрижка женская',
        'prices': {
          1: 1000,
          2: 1200
        }
      },
      {
        'id': 3,
        'name': 'Укладка',
        'prices': {
          1: 300,
          2: 500
        }
      },
      {
        'id': 4,
        'name': 'Маникюр',
        'prices': {
          1: 300,
          2: 800
        }
      },
      {
        'id': 5,
        'name': 'Стрижка усов и бороды',
        'prices': {
          1: 300,
          2: 500
        }
      }
    ],
    goodsTypes: [
      {
        'id': 1,
        'name': 'Восстанавливающая маска для поврежденных волос Ggongji Hair Pack 8мл',
        'price': 1000
      },
      {
        'id': 2,
        'name': 'Лак для волос сильной фиксации Mugens Impressive Control Hard Spray 300мл',
        'price': 200
      },
      {
        'id': 3,
        'name': 'Эссенция для волос Around Me Rose Hip Perfume Water Essence 200мл',
        'price': 200
      },
      {
        'id': 4,
        'name': 'Murray\'s eXelento Pomad - Помада для укладки волос',
        'price': 200
      },
      {
        'id': 5,
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
    ],
    offices: [
      {
        'id': 1,
        'name': 'Краснодар',
        'state': 'works'
      },
      {
        'id': 2,
        'name': 'Калуга',
        'sum': 'works'
      },
      {
        'id': 3,
        'name': 'Новороссийск',
        'sum': 'doesntWork'
      }
    ],
    employees: [
      {
        'id': 1,
        'name': 'Алексей Луцай',
        'pictureUrl': '',
        'state': 'works',
        'servicesPercent': 10,
        'goodsPercent': 10,
        'masterCategory': null,
        'roles': ['officeAdmin']
      },
      {
        'id': 2,
        'name': 'Мария Попова',
        'pictureUrl': 'static/user_photos/мария.jpg',
        'state': 'works',
        'servicesPercent': 10,
        'goodsPercent': 10,
        'masterCategory': 2,
        'roles': ['master', 'officeAdmin']
      },
      {
        'id': 3,
        'name': 'Макс Корж',
        'pictureUrl': 'static/user_photos/макс.jpg',
        'state': 'works',
        'servicesPercent': 10,
        'goodsPercent': 10,
        'masterCategory': 3,
        'roles': ['master']
      },
      {
        'id': 4,
        'name': 'Прокофий Иванов',
        'pictureUrl': '',
        'state': 'works',
        'servicesPercent': 10,
        'goodsPercent': 10,
        'masterCategory': 1,
        'roles': ['master', 'officeAdmin']
      }
    ],
    clients: [
      {
        id: 1,
        name: 'Иван',
        photoUrl: '',
        operationsCount: 6,
        contacts: [
          {
            type: 'phone',
            value: '89203342284'
          },
          {
            type: 'email',
            value: 'mail@gmail.com'
          }
        ]
      },
      {
        id: 2,
        name: 'Евгения',
        photoUrl: '',
        operationsCount: 1,
        contacts: [
          {
            type: 'phone',
            value: '89152286369'
          },
          {
            type: 'email',
            value: 'ewwwwe@mail.ru'
          }
        ]
      },
      {
        id: 3,
        name: 'Василий',
        photoUrl: '',
        operationsCount: 0,
        contacts: []
      }
    ],
    contactTypes: [
      {
        id: 'phone',
        name: 'Телефон'
      },
      {
        id: 'whatsapp',
        name: 'WhatsApp'
      },
      {
        id: 'telegram',
        name: 'Telegram'
      },
      {
        id: 'viber',
        name: 'Viber'
      },
      {
        id: 'email',
        name: 'Почта'
      },
      {
        id: 'instagram',
        name: 'Instagram'
      },
      {
        id: 'vk',
        name: 'ВКонтакте'
      },
      {
        id: 'facebook',
        name: 'Facebook'
      },
      {
        id: 'other',
        name: 'Другое'
      }
    ],
    masterCategories: []
  },
  getters: {
    getZeroPaddedNumber: (state) => (number, len) => {
      var strNum = number.toString()
      while (strNum.length < len) {
        strNum = '0' + strNum
      }
      return strNum
    },
    getDateTimeNow: (state, getters) => {
      var date = new Date()
      var hours = getters.getZeroPaddedNumber(date.getHours(), 2)
      var minutes = getters.getZeroPaddedNumber(date.getMinutes(), 2)
      var day = getters.getZeroPaddedNumber(date.getDate(), 2)
      var month = getters.getZeroPaddedNumber(date.getMonth() + 1, 2)
      var year = getters.getZeroPaddedNumber(date.getFullYear(), 2)
      return `${day}.${month}.${year} ${hours}:${minutes}`
    },
    getServiceName: (state) => (id) => {
      var service = state.serviceTypes.filter(e => e.id === id)[0]
      if (service) {
        return service.name
      }
      return '–'
    },
    getEmployeeName: (state) => (id) => {
      var employee = state.employees.filter(e => e.id === id)[0]
      if (employee) {
        return employee.name
      }
      return '–'
    },
    getItemName: (state) => (id) => {
      var item = state.goodsTypes.filter(e => e.id === id)[0]
      if (item) {
        return item.name
      }
      return '–'
    },
    getContactTypeName: (state) => (id) => {
      var item = state.contactTypes.filter(e => e.id === id)[0]
      if (item) {
        return item.name
      }
      return '–'
    },
    getSpendTypeName: (state) => (id) => {
      var item = state.spendTypes.filter(e => e.id === id)[0]
      if (item) {
        return item.name
      }
      return '–'
    },
    getEmployeePaymentTypeName: (state) => (id) => {
      var item = state.employeePaymentTypes.filter(e => e.id === id)[0]
      if (item) {
        return item.name
      }
      return '–'
    },
    getClientDescription: (state) => (id) => {
      if (id === null) {
        return null
      }
      var client = state.clients.filter(c => c.id === id)[0]
      if (client) {
        var phone = client.contacts.filter(c => c.type === 'phone')[0]
        if (phone) {
          return `${client.name} (${phone.value})`
        }
        return client.name + ' (телефон не указан)'
      }
      return '–'
    },
    getDateTimeFromOperation: (state) => (operation) => {
      var datetimestr = ''
      if (operation.startDatetime) {
        datetimestr = operation.startDatetime
      } else if (operation.datetime) {
        datetimestr = operation.datetime
      }
      return datetimestr
    },
    getTimeFromOperation: (state) => (operation) => {
      var datetimestr = ''
      if (operation.startDatetime) {
        datetimestr = operation.startDatetime
      } else if (operation.datetime) {
        datetimestr = operation.datetime
      }
      var len = datetimestr.length
      return datetimestr.slice(len - 5, len)
    },
    getEmployeeNameFromOperation: (state, getters) => (operation) => {
      if (operation.masterId) {
        return getters.getEmployeeName(operation.masterId)
      }
      if (operation.adminId) {
        return getters.getEmployeeName(operation.adminId)
      }
      if (operation.employeeId) {
        return getters.getEmployeeName(operation.employeeId)
      }
      return '–'
    },
    getOperationContent: (state, getters) => (operation) => {
      if (operation.operationType === 'service') {
        return getters.getServiceName(operation.type)
      }
      if (operation.operationType === 'goodSell') {
        return getters.getItemName(operation.type)
      }
      if (operation.operationType === 'spend') {
        return getters.getSpendTypeName(operation.type)
      }
      if (operation.operationType === 'employeePayment') {
        return getters.getEmployeePaymentTypeName(operation.type)
      }
      return '–'
    },
    getOperationSum: (state) => (operation) => {
      if (operation.operationType === 'service') {
        return operation.cashSum + operation.cashlessSum - operation.discountSum
      }
      if (operation.operationType === 'goodSell') {
        return operation.cashSum + operation.cashlessSum - operation.discountSum
      }
      if (operation.operationType === 'spend') {
        return operation.sum
      }
      if (operation.operationType === 'employeePayment') {
        return operation.sum
      }
      return '–'
    },
    getOperationBonus: (state) => (operation) => {
      if (operation.operationType === 'service') {
        return operation.masterBonus + operation.adminBonus
      }
      if (operation.operationType === 'goodSell') {
        return operation.masterBonus + operation.adminBonus
      }
      return '–'
    },
    getOperationLink: (store) => (operation) => {
      if (operation.operationType === 'service') {
        return '/EditService/' + operation.id.toString()
      }
      if (operation.operationType === 'goodSell') {
        return '/EditGoodsSell/' + operation.id.toString()
      }
      if (operation.operationType === 'spend') {
        return '/EditExpense/' + operation.id.toString()
      }
      if (operation.operationType === 'employeePayment') {
        return '/EditEmployeePayment/' + operation.id.toString()
      }
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
