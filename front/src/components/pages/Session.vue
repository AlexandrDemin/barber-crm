<template>
  <main class="background">
    <appMenu selected-element="session"></appMenu>
    <div v-if="!Object.keys(session).length" class="grid-x align-center-middle content">
      <div class="card cell shrink text-center greeting-card">
        <h1>{{getGreeting()}}<br>{{getGreetingEmojis()}}</h1>
        <label>Отделение</label>
        <v-select
          v-on:input="getCurrentSession"
          :disabled="isCurrentSessionLoading"
          :clearable="false"
          v-model="currentOfficeId"
          :reduce="s => s.id"
          :value="currentOfficeId"
          label="name"
          :options="offices"
        >
          <div slot="no-options">Ничего не найдено</div>
        </v-select>
        <div class="position-relative">
          <vue-element-loading :active="isCurrentSessionLoading" color="#1C457D"/>
          <router-link v-if="!Object.keys(session).length && currentOfficeId" to="/EditSession" class="button primary">Открыть смену</router-link>
        </div>
      </div>
    </div>
    <div v-if="Object.keys(session).length" class="session-info grid-x align-middle">
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{time}}</span>
        <label>{{date}}</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{servicesCount}}</span>
        <label>Услуг оказано</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{goodsCount}}</span>
        <label>Товаров продано</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{revenue}}</span>
        <label>Выручка, ₽</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{costs}}</span>
        <label>Расход, ₽</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="big-number">{{bonus}}</span>
        <label>Премия, ₽</label>
      </div>
      <div class="session-info-block cell medium-2 small-12">
        <router-link v-bind:to="'/EditSession/' + session.id.toString()" class="button primary small">Изменить/закрыть смену</router-link>
      </div>
    </div>
    <div v-if="Object.keys(session).length" class="session-content">
      <div class="grid-x grid-margin-x grid-margin-y">
        <employeeCard
          v-if="employee.role === 'master'"
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-bind:employee="employee"
          />
        <employeeCard
          v-if="employee.role === 'officeAdmin'"
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-bind:employee="employee"
          />
        <div class="cell large-6 columns card employee-card">
          <div class="employee-card-footer grid-x grid-padding-x grid-padding-y">
            <vue-element-loading :active="isExpenseSaving" color="#1C457D"/>
            <h4 class="cell small-12">Внести расход</h4>
            <div class="cell medium-6">
              <v-select
                @input="updateSpendSum"
                :clearable="false"
                v-model="selectedSpendType"
                :reduce="s => s.id"
                :value="selectedSpendType"
                label="name"
                :options="spendTypes"
              >
                <div slot="no-options">Ничего не найдено</div>
              </v-select>
            </div>
            <div class="cell auto">
              <input v-model.number="spendSum" type="number" placeholder="Сумма"/>
            </div>
            <div class="cell shrink">
              <button class="button secondary" @click="saveExpense">Сохранить</button>
            </div>
          </div>
        </div>
        <div class="cell small-12 columns card" v-if="session.operations">
          <div class="table-container">
            <table class="operations-table hover">
              <thead>
                <tr>
                  <th class="sticky-header">Время</th>
                  <th class="sticky-header">Операция</th>
                  <th class="sticky-header">Сотрудник</th>
                  <th class="sticky-header">Сумма</th>
                  <th class="sticky-header">Премия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="operation in session.operations" v-bind:key="operation.id">
                  <td>
                    <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                      {{$store.getters.getTimeFromOperation(operation)}}
                    </router-link>
                  </td>
                  <td>
                    <router-link
                      v-bind:to="$store.getters.getOperationLink(operation)"
                      class="table-link"
                      v-html="$store.getters.getOperationContent(operation)"
                    ></router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                      {{$store.getters.getEmployeeNameFromOperation(operation)}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                      {{$store.getters.getOperationSum(operation)}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                      {{$store.getters.getOperationBonus(operation)}}
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="cell large-6 columns">
          <button class="button secondary" @click="changeOffice">Изменить отделение</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import EmployeeCard from '@/components/EmployeeCard'
import { HTTP } from '../../api/api.js'
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'Session',
  components: {
    appMenu: Menu,
    employeeCard: EmployeeCard,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    document.title = this.$route.meta.title
    setInterval(() => {
      this.time = this.getTime()
      this.date = this.getDate()
    }, 1000)
    this.$store.state.refreshCurrentSession = setInterval(() => {
      this.getCurrentSession()
    }, 30000)
    if (this.spendTypes.length) {
      this.selectedSpendType = this.spendTypes[0].id
      this.spendSum = this.getSpendSum(this.spendTypes[0].id)
    }
  },
  beforeRouteLeave (to, from, next) {
    if (this.$store.state.refreshCurrentSession) {
      clearInterval(this.$store.state.refreshCurrentSession)
    }
    next()
  },
  data () {
    return {
      selectedSpendType: null,
      spendSum: 0,
      isExpenseSaving: false,
      expenseSavingError: '',
      time: this.getTime(),
      date: this.getDate()
    }
  },
  methods: {
    saveExpense: function () {
      this.expenseSavingError = ''
      this.isExpenseSaving = true
      var expense = {
        'type': 'spendoperation',
        'id': null,
        'expenseTypeId': this.selectedSpendType,
        'sessionId': this.session.id,
        'officeId': this.session.officeId,
        'datetime': this.moment().utc(),
        'sum': this.spendSum,
        'comment': ''
      }
      HTTP.post(`EditOperations/`, [expense])
        .then(response => {
          this.$store.dispatch('getCurrentSession')
          this.updateSpendSum()
          this.isExpenseSaving = false
        })
        .catch(e => {
          this.expenseSavingError = e
          this.isExpenseSaving = false
        })
    },
    updateSpendSum: function () {
      this.spendSum = this.getSpendSum(this.selectedSpendType)
    },
    getSpendSum: function (spendId) {
      return parseInt(this.spendTypes.filter(x => x.id === spendId)[0].defaultSum)
    },
    getGreeting: function () {
      var date = new Date()
      var hour = date.getHours()
      if (hour <= 12) {
        return 'Доброе утро!'
      }
      if (hour > 12 && hour < 17) {
        return 'Добрый день!'
      }
      if (hour >= 17) {
        return 'Добрый вечер!'
      }
    },
    getGreetingEmojis: function () {
      var emojis = ['✂️', '😀', '💪', '👋', '😎', '👏', '🦄', '🌄', '🌅', '❤️', '🍒', '🌈', '😄', '✌️', '😉', '🙂', '✂️']
      var i = 0
      var res = ''
      while (i < 3) {
        var rnd = Math.ceil(Math.random() * emojis.length - 1)
        if (rnd < 0) {
          rnd = 0
        }
        if (rnd > emojis.length) {
          rnd = emojis.length - 1
        }
        res += emojis[rnd]
        i++
      }
      return res
    },
    getTime: function () {
      return this.moment().format('HH : mm')
    },
    getDate: function () {
      return this.moment().format('DD.MM.YY')
    },
    getCurrentSession: function () {
      this.$store.dispatch('getCurrentSession')
    },
    changeOffice: function () {
      this.$store.commit('updateStore', {
        name: 'currentOfficeId',
        value: null
      })
      this.$store.commit('updateStore', {
        name: 'currentSession',
        value: {}
      })
      if (this.$store.state.refreshCurrentSession) {
        clearInterval(this.$store.state.refreshCurrentSession)
      }
    }
  },
  computed: {
    session: {
      get () {
        return this.$store.state.currentSession
      }
    },
    currentOfficeId: {
      get () {
        return this.$store.state.currentOfficeId
      },
      set (value) {
        this.$store.commit('updateStore', {
          'name': 'currentOfficeId',
          'value': value
        })
      }
    },
    isCurrentSessionLoading: {
      get () {
        return this.$store.state.isCurrentSessionLoading
      }
    },
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    },
    offices: {
      get () {
        return this.$store.state.offices
      }
    },
    servicesCount: function () {
      if (Object.keys(this.session).length && this.session.operations) {
        return this.session.operations.filter(operation => operation.type === 'serviceoperation').length
      }
      return 0
    },
    goodsCount: function () {
      if (Object.keys(this.session).length && this.session.operations) {
        return this.session.operations.filter(operation => operation.type === 'goodsoperation').length
      }
      return 0
    },
    revenue: function () {
      if (Object.keys(this.session).length && this.session.operations) {
        var revenue = 0
        var services = this.session.operations.filter(operation => operation.type === 'serviceoperation')
        var goods = this.session.operations.filter(operation => operation.type === 'goodsoperation')
        services.map(s => {
          revenue += s.cashSum + s.cashlessSum - s.discountSum
        })
        goods.map(g => {
          revenue += g.cashSum + g.cashlessSum - g.discountSum
        })
        return revenue
      }
      return 0
    },
    costs: function () {
      if (Object.keys(this.session).length && this.session.operations) {
        var costs = 0
        var spends = this.session.operations.filter(operation => operation.type === 'spendoperation')
        var employeePayments = this.session.operations.filter(operation => operation.type === 'employeepayment')
        spends.map(s => {
          costs += s.sum
        })
        employeePayments.map(e => {
          costs += e.sum
        })
        return costs
      }
      return 0
    },
    bonus: function () {
      if (Object.keys(this.session).length && this.session.operations) {
        var bonus = 0
        var services = this.session.operations.filter(operation => operation.type === 'serviceoperation')
        var goods = this.session.operations.filter(operation => operation.type === 'goodsoperation')
        services.map(s => {
          bonus += this.$store.getters.getOperationBonus(s)
        })
        goods.map(g => {
          bonus += this.$store.getters.getOperationBonus(g)
        })
        return bonus
      }
      return 0
    }
  }
}
</script>

<style>
</style>
