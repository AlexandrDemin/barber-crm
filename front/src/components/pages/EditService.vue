<template>
  <main>
    <appMenu v-bind:selected-element="canEdit ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="canEdit"><router-link to="/">Назад</router-link></li>
          <li v-else><router-link to="/SessionsHistory">История смен и операций</router-link></li>
        </ul>
      </nav>
      <h1>Услуга</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6" v-if="service">
          <label>Услуга</label>
          <v-select
            @input="updateServiceSum"
            :clearable="false"
            v-model="service.serviceId"
            :reduce="s => s.id"
            :value="service.serviceId"
            label="name"
            :options="serviceTypes"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <div class="grid-x grid-margin-x">
            <div class="cell medium-6">
              <label>Время начала</label>
              <input type="time" v-model="startTime"/>
            </div>
            <div class="cell medium-6">
              <label>Время завершения</label>
              <input type="time" v-model="endTime"/>
            </div>
          </div>
          <label>Администратор</label>
          <v-select
            :clearable="false"
            v-model="service.adminId"
            :reduce="s => s.id"
            :value="service.adminId"
            label="name"
            :options="admins"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Мастер</label>
          <v-select
            :clearable="false"
            v-model="service.masterId"
            :reduce="s => s.id"
            :value="service.masterId"
            label="name"
            :options="masters"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Клиент</label>
          <v-select
            :clearable="false"
            v-model="service.clientId"
            :reduce="s => s.id"
            :value="service.clientId"
            :get-option-label="$store.getters.getClientDescription"
            :options="clients"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <div v-if="service.clientId === null">
            <label>Имя</label>
            <input type="text" v-model="newClient.name" autofocus/>
            <!-- <label>Фото</label>
            <button type="button" class="button secondary">Выбрать</button>
            <input type="file" accept="image/*" style="display:none" ref="photoSelector"> -->
            <div v-for="(contact, index) in newClient.contacts" v-bind:key="contact">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Контакт {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeContact(index)"
                >
                  Удалить
                </button>
              </label>
              <v-select
                :clearable="false"
                v-model="contact.type"
                :reduce="s => s.id"
                :value="contact.type"
                label="name"
                :options="contactTypes"
              >
                <div slot="no-options">Ничего не найдено</div>
              </v-select>
              <input type="text" v-model="contact.value"/>
            </div>
            <div>
              <button
                class="button secondary"
                type="button"
                @click="addContact"
              >
                Добавить контакт
              </button>
            </div>
            <label>Комментарий к клиенту</label>
            <textarea rows="3" v-model="newClient.comment"></textarea>
          </div>
          <label>Сумма (наличка)</label>
          <input type="number" v-model.number="service.cashSum"/>
          <label>Сумма (безнал)</label>
          <input type="number" v-model.number="service.cashlessSum"/>
          <label>Скидка, руб.</label>
          <input type="number" v-model.number="service.discountSum"/>
          <label>Оценка от клиента от 1 до 10</label>
          <input type="number" v-model.number="service.score"/>
          <label>Отзыв клиента</label>
          <textarea rows="2" v-model="service.review"></textarea>
          <!-- <label>Фотографии</label>
          <button class="button secondary">Загрузить фотографии</button>
          <input ref="images" type="file" style="display:none" multiple="multiple" accept="image/*"> -->
          <label>Комментарий</label>
          <textarea rows="2" v-model="service.comment"></textarea>
          <div v-if="canEdit">
            <h2>Проданные товары</h2>
            <div v-for="(soldItem, index) in soldGoods" v-bind:key="soldItem.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeItem(soldItem)"
                  v-if="canEdit"
                >
                  Удалить
                </button>
              </label>
              <v-select
                @input="updateItemSum(soldItem)"
                :clearable="false"
                v-model="soldItem.goodsId"
                :reduce="s => s.id"
                :value="soldItem.goodsId"
                label="name"
                :options="goodsTypes"
              >
                <div slot="no-options">Ничего не найдено</div>
              </v-select>
              <label>Количество</label>
              <input type="number" v-model.number="soldItem.amount" @input="updateItemSum(soldItem)">
              <label>Сумма (наличка)</label>
              <input type="number" v-model.number="soldItem.cashSum">
              <label>Сумма (безнал)</label>
              <input type="number" v-model.number="soldItem.cashlessSum">
              <label>Скидка, руб.</label>
              <input type="number" v-model.number="soldItem.discountSum">
              <label>Комментарий</label>
              <textarea rows="2" v-model="soldItem.comment"></textarea>
            </div>
            <div>
              <button
                class="button secondary"
                type="button"
                @click="addItem"
                v-if="canEdit"
              >
                Добавить товар
              </button>
            </div>
            <h2>Расходы</h2>
            <div v-for="(expense, index) in expenses" v-bind:key="expense.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Расход {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeExpense(expense)"
                  v-if="canEdit"
                >
                  Удалить
                </button>
              </label>
              <v-select
                @input="updateExpenseSum(expense)"
                :clearable="false"
                v-model="expense.expenseTypeId"
                :reduce="s => s.id"
                :value="expense.expenseTypeId"
                label="name"
                :options="spendTypes"
              >
                <div slot="no-options">Ничего не найдено</div>
              </v-select>
              <label>Сумма</label>
              <input type="number" v-model.number="expense.sum">
              <label>Комментарий</label>
            <textarea rows="2" v-model="expense.comment"></textarea>
            </div>
            <div v-if="canEdit">
              <button
                class="button secondary"
                type="button"
                @click="addExpense"
              >
                Добавить расход
              </button>
            </div>
            <h2>Выплаты мастеру</h2>
            <div v-for="(payment, index) in employeePayments" v-bind:key="payment.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Выплата мастеру {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeEmployeePayment(payment)"
                  v-if="canEdit"
                >
                  Удалить
                </button>
              </label>
              <v-select
                @input="updateEmployeePaymentSum(payment)"
                :clearable="false"
                v-model="payment.employeePaymentTypeId"
                :reduce="s => s.id"
                :value="payment.employeePaymentTypeId"
                label="name"
                :options="employeePaymentTypes"
              >
                <div slot="no-options">Ничего не найдено</div>
              </v-select>
              <label>Сумма</label>
              <input type="number" v-model.number="payment.sum">
              <label>Комментарий</label>
            <textarea rows="2" v-model="payment.comment"></textarea>
            </div>
            <div v-if="canEdit">
              <button
                class="button secondary"
                type="button"
                @click="addEmployeePayment"
              >
                Добавить выплату мастеру
              </button>
            </div>
          </div>
          <div v-if="canEdit">
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary" type="button" @click="save">Сохранить</button>
          </div>
          <div v-if="savingError" class="callout alert">
            <h5>Произошла ошибка при сохранении данных</h5>
            <p>{{savingError}}</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import { HTTP } from '../../api/api.js'
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'EditService',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    } else {
      this.operations = this.getEmptyItem()
    }
  },
  mounted: function () {
    document.title = this.$route.meta.title
  },
  data () {
    return {
      isLoading: false,
      isSaving: false,
      loadingError: '',
      savingError: '',
      operations: [],
      newClient: this.getEmptyClient()
    }
  },
  methods: {
    getEmptyItem: function () {
      return [
        {
          'type': 'serviceoperation',
          'sessionId': this.currentSession.id,
          'id': null,
          'officeId': this.currentSession.officeId,
          'serviceId': this.$route.query.serviceTypeId || this.serviceTypes[0].id,
          'startDatetime': this.moment().subtract(1, 'hours'),
          'finishDatetime': this.moment(),
          'adminId': this.$route.query.adminId || this.admins[0].id,
          'masterId': this.$route.query.masterId || this.masters[0].id,
          'clientId': null,
          'cashSum': this.getServiceSum(this.$route.query.serviceTypeId, this.$route.query.masterId),
          'cashlessSum': 0,
          'discountSum': 0,
          'adminBonusSum': 0,
          'masterBonusSum': 0,
          'clientRating': null,
          'review': '',
          'photos': null,
          'comment': ''
        }
      ]
    },
    addItem: function () {
      this.operations.push({
        'type': 'goodsoperation',
        'id': null,
        'goodsId': this.goodsTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': null,
        'adminId': this.service.adminId,
        'employeeId': this.service.masterId,
        'clientId': this.service.clientId,
        'amount': 1,
        'cashSum': this.goodsTypes[0].price,
        'cashlessSum': 0,
        'discountSum': 0,
        'adminBonusSum': 0,
        'employeeBonusSum': 0,
        'comment': ''
      })
    },
    removeItem: function (item) {
      var index = this.operations.findIndex(o => o.type === 'goodsoperation' && o.goodsId === item.goodsId && o.id === item.id)
      this.operations.splice(index, 1)
    },
    updateServiceSum: function () {
      this.service.cashSum = this.getServiceSum(this.service.serviceId, this.service.masterId)
      this.service.cashlessSum = 0
    },
    updateItemSum: function (operation) {
      operation.cashSum = this.goodsTypes.filter(x => x.id === operation.goodsId)[0].price * operation.amount
      operation.cashlessSum = 0
    },
    updateExpenseSum: function (operation) {
      operation.sum = this.employeePaymentTypes.filter(x => x.id === operation.expenseTypeId)[0].defaultSum
    },
    updateEmployeePaymentSum: function (operation) {
      operation.sum = this.employeePaymentTypes.filter(x => x.id === operation.employeePaymentTypeId)[0].defaultSum
    },
    addExpense: function () {
      this.operations.push({
        'type': 'spendoperation',
        'id': null,
        'expenseTypeId': this.spendTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': null,
        'sum': this.spendTypes[0].defaultSum,
        'comment': ''
      })
    },
    removeExpense: function (item) {
      var index = this.operations.findIndex(o => o.type === 'spendoperation' && o.expenseTypeId === item.expenseTypeId && o.id === item.id)
      this.operations.splice(index, 1)
    },
    addEmployeePayment: function () {
      this.operations.push({
        'type': 'employeepayment',
        'id': null,
        'employeePaymentTypeId': this.employeePaymentTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': null,
        'employeeId': this.service.masterId,
        'sum': this.employeePaymentTypes[0].defaultSum,
        'comment': ''
      })
    },
    removeEmployeePayment: function (item) {
      var index = this.operations.findIndex(o => o.type === 'employeepayment' && o.employeePaymentTypeId === item.employeePaymentTypeId && o.id === item.id)
      this.operations.splice(index, 1)
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetServiceOperation/`, {'id': id})
        .then(response => {
          var service = response.data
          service.type = 'serviceoperation'
          service.startDatetime = this.moment.utc(service.startDatetime, 'DD.MM.YYYY HH:mm').local()
          service.finishDatetime = this.moment.utc(service.startDatetime, 'DD.MM.YYYY HH:mm').local()
          this.operations = [service]
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function () {
      this.isSaving = true
      this.savingError = ''
      var operations = this.operations
      for (var index in operations) {
        if (operations[index].type === 'serviceoperation') {
          operations[index].adminBonusSum = this.getAdminBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].adminId, operations[index].type)
          operations[index].masterBonusSum = this.getMasterBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].masterId, operations[index].type)
          operations[index].startDatetime = operations[index].startDatetime.utc()
          operations[index].finishDatetime = operations[index].finishDatetime.utc()
        } else if (operations[index].type === 'goodsoperation') {
          operations[index].adminBonusSum = this.getAdminBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].adminId, operations[index].type)
          if (operations[index].employeeId && operations[index].employeeId !== operations[index].adminId) {
            operations[index].employeeBonusSum = this.getEmployeeBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].employeeId, operations[index].type)
          }
          operations[index].datetime = this.moment().utc()
        } else {
          operations[index].datetime = this.moment().utc()
        }
      }
      this.operations = operations
      if (this.service.clientId === null) {
        var client = this.newClient
        if (client.photo === null) {
          delete client.photo
        }
        if (client.comment === null) {
          client.comment = ''
        }
        if (client.contacts === null || client.contacts === []) {
          delete client.contacts
        }
        HTTP.post(`EditClient/`, client)
          .then(response => {
            var clientId = response.data.id
            var operations = this.operations
            for (var index in operations) {
              if ('clientId' in operations[index]) {
                operations[index].clientId = clientId
              }
            }
            this.operations = operations
            HTTP.post(`EditOperations/`, this.operations)
              .then(response => {
                this.$store.dispatch('getCurrentSession')
                this.isSaving = false
                this.$router.push('/')
              })
              .catch(e => {
                this.savingError = e
                this.isSaving = false
              })
          })
          .catch(e => {
            this.savingError = e
            this.isSaving = false
          })
      } else {
        HTTP.post(`EditOperations/`, this.operations)
          .then(response => {
            this.$store.dispatch('getCurrentSession')
            this.isSaving = false
            this.$router.push('/')
          })
          .catch(e => {
            this.savingError = e
            this.isSaving = false
          })
      }
    },
    getEmptyClient: function () {
      return {
        id: null,
        name: '',
        photo: null,
        contacts: [
          {
            type: 'phone',
            value: ''
          }
        ]
      }
    },
    getServiceSum: function (serviceTypeId, masterId) {
      var serviceType = this.serviceTypes.filter(x => x.id === serviceTypeId)[0]
      var master = this.masters.filter(x => x.id === masterId)[0]
      var price = serviceType.prices.filter(x => x.category === master.categoryId)
      if (price.length) {
        return parseInt(price[0].price)
      }
      return 0
    },
    getAdminBonus: function (sum, adminId, type) {
      var admin = this.admins.filter(x => x.id === adminId)[0]
      if (type === 'serviceoperation') {
        return sum * admin.servicePercent
      }
      if (type === 'goodsoperation') {
        return sum * admin.goodsPercent
      }
    },
    getMasterBonus: function (sum, masterId, type) {
      var master = this.masters.filter(x => x.id === masterId)[0]
      if (type === 'serviceoperation') {
        return sum * master.servicePercent
      }
      if (type === 'goodsoperation') {
        return sum * master.goodsPercent
      }
    },
    getEmployeeBonus: function (sum, employeeId, type) {
      var employee = this.employees.filter(x => x.id === employeeId)[0]
      return sum * employee.goodsPercent
    },
    addContact: function () {
      if (!this.newClient.contacts) {
        this.newClient.contacts = []
      }
      this.newClient.contacts.push({
        type: 'phone',
        value: ''
      })
    },
    removeContact: function (index) {
      this.newClient.contacts.splice(index, 1)
    }
  },
  computed: {
    currentSession: {
      get () {
        return this.$store.state.currentSession
      }
    },
    serviceTypes: {
      get () {
        return this.$store.state.serviceTypes
      }
    },
    clients: {
      get () {
        var clientsCopy = [...this.$store.state.clients]
        clientsCopy.unshift(this.getEmptyClient())
        return clientsCopy
      }
    },
    admins: {
      get () {
        if (this.currentSession && Object.keys(this.currentSession).length) {
          return this.currentSession.employees.filter(e => e.role === 'officeAdmin')
        }
        return this.$store.state.employees.filter(e => e.roles.includes('officeAdmin'))
      }
    },
    masters: {
      get () {
        if (this.currentSession && Object.keys(this.currentSession).length) {
          return this.currentSession.employees.filter(e => e.role === 'master')
        }
        return this.$store.state.employees.filter(e => e.roles.includes('master'))
      }
    },
    employees: {
      get () {
        if (this.currentSession && Object.keys(this.currentSession).length) {
          return this.currentSession.employees
        }
        return this.$store.state.employees
      }
    },
    goodsTypes: {
      get () {
        return this.$store.state.goodsTypes
      }
    },
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    },
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      }
    },
    contactTypes: {
      get () {
        return this.$store.state.contactTypes
      }
    },
    service: {
      get () {
        return this.operations.filter(o => o.type === 'serviceoperation')[0]
      },
      set (item) {
        var index = this.operations.findIndex(o => o.type === 'serviceoperation') || 0
        this.operations.$set(index, item)
      }
    },
    soldGoods: {
      get () {
        return this.operations.filter(o => o.type === 'goodsoperation')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.type === 'goodsoperation' && o.goodsId === item.goodsId && o.id === item.id)
        this.operations.$set(index, item)
      }
    },
    expenses: {
      get () {
        return this.operations.filter(o => o.type === 'spendoperation')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.type === 'spendoperation' && o.expenseTypeId === item.expenseTypeId && o.id === item.id)
        this.operations.$set(index, item)
      }
    },
    employeePayments: {
      get () {
        return this.operations.filter(o => o.type === 'employeepayment')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.type === 'employeepayment' && o.employeePaymentTypeId === item.employeePaymentTypeId && o.id === item.id && o.employeeId === item.employeeId)
        this.operations.$set(index, item)
      }
    },
    canEdit: function () {
      if (this.operations[0]) {
        return !this.operations[0].id || (this.operations[0].sessionId === this.currentSession.id)
      }
      return false
    },
    startTime: {
      get () {
        return this.service.startDatetime.format('HH:mm')
      },
      set (val) {
        this.service.startDatetime = this.moment(val, 'HH:mm')
      }
    },
    endTime: {
      get () {
        return this.service.finishDatetime.format('HH:mm')
      },
      set (val) {
        this.service.finishDatetime = this.moment(val, 'HH:mm')
      }
    }
  }
}
</script>

<style>
</style>
