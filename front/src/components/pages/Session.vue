<template>
  <main class="translucent-theme background">
    <appMenu selected-element="session"></appMenu>
    <div v-if="!Object.keys(session).length" class="grid-x align-center-middle content">
      <div class="card cell shrink text-center greeting-card">
        <h1>{{getGreeting()}}<br>{{getGreetingEmojis()}}</h1>
        <div><router-link to="/EditSession" class="button primary">Открыть смену</router-link></div>
      </div>
    </div>
    <div v-if="Object.keys(session).length" class="session-info grid-x align-middle">
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{time}}</span>
        <label class="session-info-big-label">{{date}}</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{servicesCount}}</span>
        <label class="session-info-big-label">Услуг оказано</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{goodsCount}}</span>
        <label class="session-info-big-label">Товаров продано</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{revenue}}</span>
        <label class="session-info-big-label">Выручка, ₽</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{costs}}</span>
        <label class="session-info-big-label">Расход, ₽</label>
      </div>
      <div class="session-info-block cell medium-auto small-6">
        <span class="session-info-big-number">{{bonus}}</span>
        <label class="session-info-big-label">Премия, ₽</label>
      </div>
      <div class="session-info-block cell medium-2 small-12">
        <router-link v-bind:to="'/EditSession/' + session.id.toString()" class="button secondary small">Изменить/закрыть смену</router-link>
      </div>
    </div>
    <div v-if="Object.keys(session).length" class="session-content">
      <div class="grid-x grid-margin-x grid-margin-y">
        <employeeCard
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-bind:employee="employee"
          v-if="employee.role === 'master'"
          />
        <employeeCard
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-bind:employee="employee"
          v-if="employee.role === 'officeAdmin'"
          />
        <div class="cell large-6 columns card employee-card">
          <div class="employee-card-footer grid-x grid-padding-x grid-padding-y">
            <h4 class="cell small-12">Внести расход</h4>
            <div class="cell medium-6">
              <select v-model="selectedSpendType">
                <option v-for="spend in spendTypes" v-bind:key="spend.id" v-bind:value="spend.id" v-bind:selected="spend.id === selectedSpendType">
                  {{spend.name}}
                </option>
              </select>
            </div>
            <div class="cell auto">
              <input v-model="spendSum" type="number" placeholder="Сумма"/>
            </div>
            <div class="cell shrink">
              <button class="button secondary">Сохранить</button>
            </div>
          </div>
        </div>
        <div class="cell small-12 columns card">
          <table class="unstriped operations-table">
            <thead>
              <tr>
                <th>Время</th>
                <th>Сотрудник</th>
                <th>Операция</th>
                <th>Сумма</th>
                <th>Премия</th>
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
                  <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                    {{$store.getters.getEmployeeNameFromOperation(operation)}}
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
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import EmployeeCard from '@/components/EmployeeCard'

export default {
  name: 'Session',
  components: {
    appMenu: Menu,
    employeeCard: EmployeeCard
  },
  mounted: function () {
    document.title = this.$route.meta.title
    setInterval(() => {
      this.time = this.getTime()
      this.date = this.getDate()
    }, 1000)
  },
  data () {
    return {
      session1: {},
      selectedSpendType: 1,
      spendSum: '',
      time: this.getTime(),
      date: this.getDate()
    }
  },
  methods: {
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
      var date = new Date()
      var hours = date.getHours()
      var minutes = date.getMinutes()
      return this.$store.getters.getZeroPaddedNumber(hours, 2) + ' : ' + this.$store.getters.getZeroPaddedNumber(minutes, 2)
    },
    getDate: function () {
      var date = new Date()
      return date.toLocaleDateString('ru')
    }
  },
  computed: {
    session: {
      get () {
        return this.$store.state.currentSession
      }
    },
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    },
    servicesCount: function () {
      if (Object.keys(this.session).length) {
        return this.session.operations.filter(operation => operation.operationType === 'service').length
      }
      return 0
    },
    goodsCount: function () {
      if (Object.keys(this.session).length) {
        return this.session.operations.filter(operation => operation.operationType === 'goodSell').length
      }
      return 0
    },
    revenue: function () {
      if (Object.keys(this.session).length) {
        var revenue = 0
        var services = this.session.operations.filter(operation => operation.operationType === 'service')
        var goods = this.session.operations.filter(operation => operation.operationType === 'goodSell')
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
      if (Object.keys(this.session).length) {
        var costs = 0
        var spends = this.session.operations.filter(operation => operation.operationType === 'spend')
        var employeePayments = this.session.operations.filter(operation => operation.operationType === 'employeePayment')
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
      if (Object.keys(this.session).length) {
        var bonus = 0
        var services = this.session.operations.filter(operation => operation.operationType === 'service')
        var goods = this.session.operations.filter(operation => operation.operationType === 'goodSell')
        services.map(s => {
          bonus += s.adminBonus + s.masterBonus
        })
        goods.map(g => {
          bonus += g.adminBonus + g.masterBonus
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
