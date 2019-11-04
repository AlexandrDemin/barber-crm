<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Внести расходы</h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div>
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
            <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalsalary || 0}}</div>
                <label>Начисленная заплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalpaidsalary || 0}}</div>
                <label>Выплаченая зарплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalpenalty || 0}}</div>
                <label>Штрафы, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalunpaidsalary || 0}}</div>
                <label>Невыплаченая зарплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{(employee.totalgoodsbonus || 0) + (employee.totalservicebonus || 0)}}</div>
                <label>Начисленная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalservicebonus || 0}}</div>
                <label>Премия (услуги), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalgoodsbonus || 0}}</div>
                <label>Премия (товары), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalpaidbonus || 0}}</div>
                <label>Выплаченная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.totalunpaidbonus || 0}}</div>
                <label>Невыплаченная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.estimatedworkhours || 0}}</div>
                <label>Рабочие часы в месяце</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{employee.total_time || 0}}</div>
                <label>Отработанные часы</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{((employee.meanworkload || 0) * 100).toFixed(2).toString() + '%'}}</div>
                <label>% отработанных часов</label>
              </div>
            </div>
            <div v-for="(payment, index) in employee.operations" v-bind:key="payment.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Выплата {{index + 1}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeEmployeePayment(payment, employee.operations)"
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
            <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalincome.toFixed(2) || 0}}</div>
                <label>Выручка, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.serviceincome || 0}}</div>
                <label>Выручка (услуги), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.goodsincome || 0}}</div>
                <label>Выручка (товары), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalcash || 0}}</div>
                <label>Выручка (наличка), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalcashless || 0}}</div>
                <label>Выручка (безнал), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalspend || 0}}</div>
                <label>Расходы, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalprofit.toFixed(2) || 0}}</div>
                <label>Прибыль, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.operationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Операция', 'Операции', 'Операций')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.serviceoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Услуга оказана', 'Услуги оказано', 'Услуг оказано')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.goodsoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Товар продан', 'Товара продано', 'Товаров продано')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.spendoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Расход внесен', 'Расхода внесено', 'Расходов внесено')}}</label>
              </div>
            </div>
            <div v-for="(expense, index) in office.operations" v-bind:key="expense.id">
              <label v-on:click.prevent class="grid-x">
                <span class="cell auto">Расход {{index + 1}}</span>
                <button
                  type="button" class="button clear small cell shrink no-margin"
                  @click="removeExpense(expense, office.operations)"
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
      byOfficesAndEmployees: [],
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
        'sum': sum,
        'comment': ''
      }
    },
    addEmployeePayment: function (employeeId, operations) {
      operations.push(this.getEmptyEmployeePayment(employeeId))
    },
    removeEmployeePayment: function (item, operations) {
      var index = operations.findIndex(o => o.employeePaymentTypeId === item.employeePaymentTypeId && o.sum === item.sum)
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
                    employee.operations = []
                    if (employee.totalunpaidsalary > 0) {
                      employee.operations.push(this.getEmptyEmployeePayment(employee.employeeId, 'salary', employee.totalunpaidsalary))
                    }
                    if (employee.totalunpaidbonus > 0) {
                      employee.operations.push(this.getEmptyEmployeePayment(employee.employeeId, 'bonus', employee.totalunpaidbonus))
                    }
                  }
                  this.byEmployees = byEmployees
                  this.byOfficesAndEmployees = response.data.byOfficeAndEmployee
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
      for (var j in this.byOffices) {
        var office = this.byOffices[j]
        for (var i in office.operations) {
          var operation = office.operations[i]
          var session = this.getSessionForOffice(office.officeId)
          operation.sessionId = session.id
          operation.officeId = office.officeId
          operation.datetime = this.moment.utc(session.dateOpened, 'DD.MM.YYYY HH:mm')
          operations.push(operation)
        }
      }
      for (j in this.byEmployees) {
        var employee = this.byEmployees[j]
        for (i in employee.operations) {
          operation = employee.operations[i]
          session = this.getSessionForEmployee(employee.employeeId)
          operation.sessionId = session.id
          operation.officeId = office.officeId
          operation.datetime = this.moment.utc(session.dateOpened, 'DD.MM.YYYY HH:mm')
          operations.push(operation)
        }
      }
      HTTP.post(`EditOperations/`, operations)
        .then(response => {
          this.isSaving = false
          this.load()
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    sortSessionsByDate: function (a, b) {
      var opened1 = this.moment(a.dateOpened, 'DD.MM.YYYY HH:mm')
      var opened2 = this.moment(b.dateOpened, 'DD.MM.YYYY HH:mm')
      if (opened1.isBefore(opened2)) {
        return 1
      } else {
        return -1
      }
    },
    getSessionForOffice: function (officeId) {
      var sessions = this.sessions.filter(x => x.officeId === officeId)
      if (sessions.length) {
        return sessions.sort(this.sortSessionsByDate)[0]
      }
      return this.sessions.sort(this.sortSessionsByDate)[0]
    },
    getSessionForEmployee: function (employeeId) {
      var sessions = this.sessions.filter(x => x.employees.filter(x => x.id === employeeId).length > 0)
      if (sessions.length) {
        return sessions.sort(this.sortSessionsByDate)[0]
      }
      return this.sessions.sort(this.sortSessionsByDate)[0]
    },
    inclineWord: function (num, form1, form2, form3) {
      if (num) {
        var lastDigit = num.toString()[num.toString().length - 1]
        if (['5', '6', '7', '8', '9', '0'].includes(lastDigit) || (num % 100 > 10 && num % 100 < 20)) {
          return form3
        }
        if (['2', '3', '4'].includes(lastDigit)) {
          return form2
        }
        if (lastDigit === '1') {
          return form1
        }
      }
      return form1
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
