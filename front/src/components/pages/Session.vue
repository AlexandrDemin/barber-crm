<template>
  <main class="translucent-theme background">
    <appMenu selected-element="session"></appMenu>
    <div class="session-info grid-x align-middle">
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
        <button class="button secondary small">Изменить/закрыть смену</button>
      </div>
    </div>
    <div class="session-content">
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
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="operation in session.operations" v-if="operation.operationType === 'service'" v-bind:key="operation.id">
                <td>{{getTimeFromApiData(operation.startDatetime)}}</td>
                <td>Сотрудник</td>
                <td>Операция</td>
                <td>Сумма</td>
                <td>Премия</td>
                <td><button type="button" class="button secondary">Редактировать/удалить</button></td>
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
      session: {
        'id': 1,
        'dateOpened': '21.09.2019 09:30',
        'dateClosed': null,
        'employees': [
          {
            'Id': 1,
            'name': 'Алексей Луцай',
            'role': 'officeAdmin',
            'pictureUrl': '',
            'workHours': 6
          },
          {
            'Id': 2,
            'name': 'Мария Попова',
            'role': 'master',
            'pictureUrl': 'static/user_photos/мария.jpg',
            'workHours': 6
          },
          {
            'Id': 3,
            'name': 'Макс Корж',
            'role': 'master',
            'pictureUrl': 'static/user_photos/макс.jpg',
            'workHours': 6
          },
          {
            'Id': 4,
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
            'id': 1,
            'officeId': 1,
            'type': 'Стрижка мужская',
            'startDatetime': '21.09.2019 09:30',
            'finishDatetime': '21.09.2019 10:30',
            'adminId': 1,
            'masterId': 2,
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
            'type': [2, 44, 21],
            'datetime': '21.09.2019 09:30',
            'adminId': 1,
            'masterId': 2,
            'clientId': 1,
            'cashSum': 0,
            'cashlessSum': 2350,
            'discountSum': 0,
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
      selectedSpendType: 1,
      spendSum: '',
      time: this.getTime(),
      date: this.getDate()
    }
  },
  methods: {
    getZeroPaddedNumber: function (number, len) {
      var strNum = number.toString()
      while (strNum.length < len) {
        strNum = '0' + strNum
      }
      return strNum
    },
    getTime: function () {
      var date = new Date()
      var hours = date.getHours()
      var minutes = date.getMinutes()
      return this.getZeroPaddedNumber(hours, 2) + ' : ' + this.getZeroPaddedNumber(minutes, 2)
    },
    getDate: function () {
      var date = new Date()
      return date.toLocaleDateString('ru')
    },
    getTimeFromApiData: function (datetimestr) {
      var len = datetimestr.length
      return datetimestr.slice(len - 5, len)
    }
  },
  computed: {
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    },
    servicesCount: function () {
      return this.session.operations.filter(operation => operation.operationType === 'service').length
    },
    goodsCount: function () {
      return this.session.operations.filter(operation => operation.operationType === 'goodSell').length
    },
    revenue: function () {
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
    },
    costs: function () {
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
    },
    bonus: function () {
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
  }
}
</script>

<style>
</style>
