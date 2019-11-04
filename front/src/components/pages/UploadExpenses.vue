<!--
Загрузить зарплаты по сотрудникам
  зарплата
    из сотрудника
  премия
    из отчёта по сотрудникам
Загрузить расходы по офисам
  аренда
  прочие расходы
Расходы привязываются к последней смене месяца
  в каком офисе?
-->

<template>
  <main>
    <appMenu :selected-element="admin"></appMenu>
    <div class="content">
      <h1>Внести расходы</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div class="cell large-6">
          <label>Месяц</label>
          <v-select
            @input="load"
            :clearable="false"
            v-model="period"
            :value="period"
            label="name"
            :options="periods"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <h2>Выплаты сотрудникам</h2>
          <div v-for="employee in byEmployees" v-bind:key="employee.employeeId">
            <h3>{{employee.name}}</h3>
            <div v-for="(payment, index) in employee.operations" v-bind:key="payment.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Выплата сотруднику {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeEmployeePayment(payment, employee.operations)"
                  v-if="index > 0"
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
            </div>
            <div>
              <button
                class="button secondary"
                type="button"
                @click="addEmployeePayment(employee.employeeId, employee.operations)"
              >
                Добавить выплату сотруднику
              </button>
            </div>
          </div>
          <h2>Расходы по отделениям</h2>
          <div v-for="office in byOffices" v-bind:key="office.officeId">
            <h3>{{$store.getters.getOfficeName(office.officeId)}}</h3>
            <div v-for="(expense, index) in office.operations" v-bind:key="expense.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Расход {{index > 0 ? index + 1 : ''}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeExpense(expense, office.operations)"
                  v-if="index > 0"
                >
                  Удалить
                </button>
              </label>
              <v-select
                @input="updateSpendSum(expense)"
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
            </div>
            <div>
              <button class="button secondary" type="button" @click="addExpense(office.officeId, office.operations)">Добавить расход</button>
            </div>
          </div>
          <div>
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
  name: 'UploadExpenses',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    document.title = this.$route.meta.title
    this.load()
  },
  data () {
    return {
      isLoading: false,
      loadingError: false,
      isSaving: false,
      savingError: '',
      sessions: [],
      byOffices: [],
      byEmployees: [],
      period: this.moment().format('MM YYYY')
    }
  },
  methods: {
    getEmptyExpense: function (officeId) {
      return {
        'type': 'spendoperation',
        'id': null,
        'expenseTypeId': this.spendTypes[0].id,
        'sum': this.getSpendSum(this.spendTypes[0].id),
        'comment': ''
      }
    },
    getEmptyEmployeePayment: function (employeeId, type, sum) {
      return {
        'type': 'employeepayment',
        'id': null,
        'employeePaymentTypeId': type ? this.employeePaymentTypes.filter(x => x.type === type)[0].id : this.employeePaymentTypes[0].id,
        'employeeId': employeeId,
        'sum': sum || this.employeePaymentTypes[0].defaultSum,
        'comment': ''
      }
    },
    addEmployeePayment: function (employeeId, operations) {
      operations.push(this.getEmptyEmployeePayment(employeeId))
    },
    removeEmployeePayment: function (item, operations) {
      var index = operations.findIndex(o => o.type === 'employeepayment' && o.employeePaymentTypeId === item.employeePaymentTypeId && o.id === item.id)
      operations.splice(index, 1)
    },
    updateSpendSum: function (operation) {
      operation.sum = this.getSpendSum(operation.expenseTypeId)
    },
    getSpendSum: function (spendId) {
      return parseInt(this.spendTypes.filter(x => x.id === spendId)[0].defaultSum)
    },
    updateEmployeePaymentSum: function (operation) {
      operation.sum = this.employeePaymentTypes.filter(x => x.id === operation.employeePaymentTypeId)[0].defaultSum
    },
    addExpense: function (officeId, spendOperations) {
      spendOperations.push(this.getEmptyExpense(officeId))
    },
    removeExpense: function (item, spendOperations) {
      var index = spendOperations.findIndex(o => o.type === 'spendoperation' && o.type === item.type && o.id === item.id)
      spendOperations.splice(index, 1)
    },
    load: function () {
      this.isLoading = true
      this.loadingError = ''
      var dateFrom = this.moment(this.period, 'MM YYYY')
      var sessionsData = {
        dateFrom: dateFrom.format('DD.MM.YYYY'),
        dateTo: dateFrom.add(1, 'months').format('DD.MM.YYYY'),
        withOperations: false
      }
      HTTP.post(`GetSessions/`, sessionsData)
        .then(response => {
          this.sessions = response.data
          var reportData = {
            period: this.moment(this.period, 'MM YYYY').format('DD.MM.YYYY')
          }
          HTTP.post(`GenerateFinanceReport/`, reportData)
            .then(response => {
              var byOffices = response.data.byOffices
              for (var index in byOffices) {
                var office = byOffices[index]
                office.operations = [this.getEmptyExpense(office.officeId)]
              }
              this.byOffices = response.data.byOffices
              HTTP.post(`GenerateEmployeeReport/`, reportData)
                .then(response => {
                  var byEmployees = response.data.byEmployees
                  for (var i in byEmployees) {
                    var employee = byEmployees[i]
                    employee.operations = [
                      this.getEmptyEmployeePayment(employee.employeeId, 'salary', employee.totalunpaidsalary),
                      this.getEmptyEmployeePayment(employee.employeeId, 'bonus', employee.totalunpaidbonus)
                    ]
                  }
                  this.byEmployees = byEmployees
                  this.isLoading = false
                })
                .catch(e => {
                  this.loadingError = e
                  this.isLoading = false
                })
            })
            .catch(e => {
              this.loadingError = e
              this.isLoading = false
            })
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function () {
      this.savingError = ''
      this.isSaving = true
      var operations = []
      // Для каждой выплаты сотрудникам
      //   создать объекты операций для каждого офиса, где работал сотрудник. Сумма = сумма * % времени, сколько сотрудник там работал
      //   проставить officeId офиса
      //   проставить sessionId последней сесии в этом офисе
      //   добавить в общий массив операций
      // Для каждой операции по расходу
      //   проставить officeId офиса
      //   проставить sessionId последней сесии в этом офисе
      // Отправить данные в EditOperations
      HTTP.post(`EditOperations/`, operations)
        .then(response => {
          this.isSaving = false
          this.load()
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    }
  },
  computed: {
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
    periods () {
      var periods = []
      for (var i = 0; i <= 12; i++) {
        periods.push(this.moment().subtract(i, 'months').format('MM YYYY'))
      }
      return periods
    }
  }
}
</script>

<style>
</style>
