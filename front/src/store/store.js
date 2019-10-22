import Vuex from 'vuex'
import Vue from 'vue'
import { HTTP } from '../api/api.js'
import moment from 'moment'

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
    spendTypeStates: [
      {
        id: 'active',
        name: 'Используется'
      },
      {
        id: 'notactive',
        name: 'Не используется'
      }
    ],
    employeePaymentTypeStates: [
      {
        id: 'active',
        name: 'Используется'
      },
      {
        id: 'notactive',
        name: 'Не используется'
      }
    ],
    masterCategoryStates: [
      {
        id: 'active',
        name: 'Используется'
      },
      {
        id: 'notactive',
        name: 'Не используется'
      }
    ],
    employeeStates: [
      {
        id: 'working',
        name: 'Работает'
      },
      {
        id: 'notworking',
        name: 'Не работает'
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
    getClientDescription: (state) => (clientOrClientId) => {
      if (clientOrClientId === null) {
        return null
      }
      var client = clientOrClientId
      if (typeof client === 'number') {
        client = state.clients.filter(c => c.id === client)[0]
      }
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
      return moment(datetimestr).format('DD.MM.YYYY HH:mm')
    },
    getTimeFromOperation: (state) => (operation) => {
      var datetimestr = ''
      if (operation.startDatetime) {
        datetimestr = operation.startDatetime
      } else if (operation.datetime) {
        datetimestr = operation.datetime
      }
      return moment(datetimestr).format('HH:mm')
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
      if (operation.type === 'serviceoperation') {
        return getters.getServiceName(operation.serviceId)
      }
      if (operation.type === 'goodsoperation') {
        var names = []
        for (var i in operation.goodsIds) {
          names.push(getters.getItemName(operation.goodsIds[i]))
        }
        return names.join('\n')
      }
      if (operation.type === 'spendoperation') {
        return getters.getSpendTypeName(operation.expenseTypeId)
      }
      if (operation.type === 'employeepayment') {
        return getters.getEmployeePaymentTypeName(operation.employeePaymentTypeId)
      }
      return '–'
    },
    getOperationSum: (state) => (operation) => {
      if (operation.type === 'serviceoperation') {
        return operation.cashSum + operation.cashlessSum - operation.discountSum
      }
      if (operation.type === 'goodsoperation') {
        return operation.cashSum + operation.cashlessSum - operation.discountSum
      }
      if (operation.type === 'spendoperation') {
        return operation.sum
      }
      if (operation.type === 'employeepayment') {
        return operation.sum
      }
      return '–'
    },
    getOperationBonus: (state) => (operation) => {
      if (operation.type === 'serviceoperation') {
        return operation.masterBonus + operation.adminBonus
      }
      if (operation.type === 'goodsoperation') {
        return operation.masterBonus + operation.adminBonus
      }
      return '–'
    },
    getOperationLink: (state) => (operation) => {
      if (operation.type === 'serviceoperation') {
        return '/EditService/' + operation.id.toString()
      }
      if (operation.type === 'goodsoperation') {
        return '/EditGoodsSell/' + operation.id.toString()
      }
      if (operation.type === 'spendoperation') {
        return '/EditExpense/' + operation.id.toString()
      }
      if (operation.type === 'employeepayment') {
        return '/EditEmployeePayment/' + operation.id.toString()
      }
    },
    getOfficeName: (state) => (id) => {
      var office = state.offices.filter(e => e.id === id)[0]
      if (office) {
        return office.name
      }
      return '–'
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
    getSpendTypeStateName: (state) => (id) => {
      var spendTypeState = state.spendTypeStates.filter(e => e.id === id)[0]
      if (spendTypeState) {
        return spendTypeState.name
      }
      return '–'
    },
    getEmployeePaymentStateName: (state) => (id) => {
      var employeePaymentTypeState = state.employeePaymentTypeStates.filter(e => e.id === id)[0]
      if (employeePaymentTypeState) {
        return employeePaymentTypeState.name
      }
      return '–'
    },
    getMasterCategoryStateName: (state) => (id) => {
      var masterCategoryState = state.masterCategoryStates.filter(e => e.id === id)[0]
      if (masterCategoryState) {
        return masterCategoryState.name
      }
      return '–'
    },
    getEmployeeStateName: (state) => (id) => {
      var employeeState = state.employeeStates.filter(e => e.id === id)[0]
      if (employeeState) {
        return employeeState.name
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
