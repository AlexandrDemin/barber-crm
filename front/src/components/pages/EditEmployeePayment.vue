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
      <h1>Выплата сотруднику</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div class="cell large-6" v-if="operations.length">
          <label>Время</label>
          <input type="time" v-model="time"/>
          <div v-for="(payment, index) in operations" v-bind:key="payment.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Выплата сотруднику {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(payment)"
                v-if="canEdit && index > 0"
              >
                Удалить
              </button>
            </label>
            <v-select
              @input="updateSum(payment)"
              :clearable="false"
              v-model="payment.employeePaymentTypeId"
              :reduce="s => s.id"
              :value="payment.employeePaymentTypeId"
              label="name"
              :options="employeePaymentTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Сотрудник</label>
            <v-select
              v-model="payment.employeeId"
              :reduce="s => s.id"
              :value="payment.employeeId"
              label="name"
              :options="employees"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Сумма</label>
            <input type="number" v-model.number="payment.sum">
            <label>Комментарий</label>
            <textarea rows="2" v-model="payment.comment"></textarea>
          </div>
          <div>
            <button
              class="button secondary"
              type="button"
              @click="addItem"
              v-if="canEdit"
            >
              Добавить выплату сотруднику
            </button>
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
  name: 'EditEmployeePayment',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    this.operations = [this.getEmptyItem()]
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    }
    document.title = this.$route.meta.title
  },
  data () {
    return {
      isLoading: false,
      isSaving: false,
      loadingError: '',
      savingError: '',
      operations: [],
      time: this.moment().format('HH:mm')
    }
  },
  methods: {
    addItem: function () {
      this.operations.push(this.getEmptyItem())
    },
    removeItem: function (item) {
      var index = this.operations.findIndex(o => o.type === 'employeepayment' && o.employeePaymentTypeId === item.employeePaymentTypeId && o.id === item.id)
      this.operations.splice(index, 1)
    },
    getEmptyItem: function () {
      return {
        'type': 'employeepayment',
        'id': null,
        'employeePaymentTypeId': this.$route.query.employeePaymentTypeId || this.employeePaymentTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': null,
        'employeeId': this.employees[0].id,
        'sum': this.employeePaymentTypes[0].defaultSum,
        'comment': ''
      }
    },
    updateSum: function (operation) {
      operation.sum = this.employeePaymentTypes.filter(x => x.id === operation.employeePaymentTypeId)[0].defaultSum
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetEmployeePaymentOperation/`, {'id': id})
        .then(response => {
          var operation = response.data
          operation.type = 'employeepayment'
          operation.datetime = this.moment.utc(operation.datetime, 'DD.MM.YYYY HH:mm').local()
          this.operations = [operation]
          this.time = operation.datetime.format('HH:mm')
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
        operations[index].datetime = this.moment(this.time, 'HH:mm').utc()
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
    }
  },
  computed: {
    currentSession: {
      get () {
        return this.$store.state.currentSession
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
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      }
    },
    canEdit: function () {
      if (this.operations[0]) {
        return !this.operations[0].id || (this.operations[0].sessionId === this.currentSession.id)
      }
      return false
    }
  }
}
</script>

<style>
</style>
