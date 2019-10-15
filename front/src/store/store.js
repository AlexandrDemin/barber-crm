import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    isStateLoading: false,
    isStateLoaded: false,
    stateLoadDetails: {
      serviceTypes: false,
      goodsTypes: false,
      employeePaymentTypes: false,
      spendTypes: false,
      offices: false,
      employees: false,
      clients: false,
      masterCategories: false
    },
    stateGetError: '',
    currentOfficeId: null,
    currentSessionGetError: '',
    isCurrentSessionLoading: false,
    currentSession: {},
    currentSession1: {
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
        id: 'serviceoperation',
        name: 'Услуга'
      },
      {
        id: 'goodsoperation',
        name: 'Продажа товара'
      },
      {
        id: 'spendoperation',
        name: 'Расход'
      },
      {
        id: 'employeepayment',
        name: 'Выплата сотруднику'
      }
    ],
    officeStates: [
      {
        id: 'open',
        name: 'Работает'
      },
      {
        id: 'closed',
        name: 'Не работает'
      }
    ],
    goodsStates: [
      {
        id: 'active',
        name: 'В продаже'
      },
      {
        id: 'notactive',
        name: 'Не продается'
      }
    ],
    userRoles: [
      {
        id: 'officeAdmin',
        name: 'Администратор офиса'
      },
      {
        id: 'manager',
        name: 'Управляющий'
      },
      {
        id: 'master',
        name: 'Мастер'
      },
      {
        id: 'other',
        name: 'Сотрудник'
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
    serviceTypes: [],
    goodsTypes: [],
    employeePaymentTypes: [],
    spendTypes: [],
    offices: [],
    employees: [],
    clients: [],
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
    getMasterCategoryName: (state) => (id) => {
      var item = state.masterCategories.filter(e => e.id === id)[0]
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
    getOperationLink: (state) => (operation) => {
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
    },
    getOfficeStateName: (state) => (id) => {
      var officeState = state.officeStates.filter(e => e.id === id)[0]
      if (officeState) {
        return officeState.name
      }
      return '–'
    },
    getGoodsStateName: (state) => (id) => {
      var goodsState = state.goodsStates.filter(e => e.id === id)[0]
      if (goodsState) {
        return goodsState.name
      }
      return '–'
    },
    getUserRoleName: (state) => (id) => {
      var userRole = state.userRoles.filter(e => e.id === id)[0]
      if (userRole) {
        return userRole.name
      }
      return '–'
    },
    getUserPicturePlaceholderText: (state) => (name) => {
      var initials = ''
      name.split(' ').map(n => {
        initials += n[0].toUpperCase()
      })
      return initials
    }
  },
  mutations: {
    updateStore (state, payload) {
      state[payload.name] = payload.value
    },
    updateStateLoadingDetails (state, payload) {
      state.stateLoadDetails[payload.name] = payload.value
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
    getCurrentSession (context) {
      context.commit('updateStore', {
        'name': 'isCurrentSessionLoading',
        'value': true
      })
      HTTP.post(`GetCurrentSession/`, {
        'officeId': context.state.currentOfficeId,
        'withOperations': true
      })
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'currentSession',
            'value': data
          })
          context.commit('updateStore', {
            'name': 'isCurrentSessionLoading',
            'value': false
          })
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'currentSessionGetError',
            'value': e
          })
          context.commit('updateStore', {
            'name': 'isCurrentSessionLoading',
            'value': false
          })
        })
    },
    checkIfStateLoaded (context) {
      var isLoaded = Object.values(context.state.stateLoadDetails).every(x => x)
      if (isLoaded !== context.state.isStateLoaded) {
        context.commit('updateStore', {
          'name': 'isStateLoaded',
          'value': isLoaded
        })
        context.commit('updateStore', {
          'name': 'isStateLoading',
          'value': !isLoaded
        })
      }
    },
    getState (context, actions) {
      if (!context.state.isStateLoaded) {
        context.commit('updateStore', {
          'name': 'isStateLoading',
          'value': true
        })
        context.commit('updateStore', {
          'name': 'isStateLoaded',
          'value': false
        })
      }
      HTTP.post(`GetServicesPrices/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'serviceTypes',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'serviceTypes',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetGoods/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'goodsTypes',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'goodsTypes',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetEmployeePaymentTypes/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'employeePaymentTypes',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'employeePaymentTypes',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetSpendTypes/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'spendTypes',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'spendTypes',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetOffices/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'offices',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'offices',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetEmployees/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'employees',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'employees',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetClients/`, {q: ''})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'clients',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'clients',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
      HTTP.post(`GetBarberCategories/`, {})
        .then(response => {
          var data = response.data
          context.commit('updateStore', {
            'name': 'masterCategories',
            'value': data
          })
          context.commit('updateStateLoadingDetails', {
            'name': 'masterCategories',
            'value': true
          })
          context.dispatch('checkIfStateLoaded')
        })
        .catch(e => {
          context.commit('updateStore', {
            'name': 'stateGetError',
            'value': e
          })
        })
    }
  }
})
