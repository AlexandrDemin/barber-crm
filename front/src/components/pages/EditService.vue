<template>
  <main>
    <appMenu v-bind:selected-element="$route.query.sessionId || 'session'"></appMenu>
    <div class="content">
      <h1>Услуга</h1>
      <div class="grid-x">
        <form class="cell large-6">
          <label>Услуга</label>
          <select v-model="service.type">
            <option
              v-for="serviceType in serviceTypes"
              v-bind:key="serviceType.id"
              v-bind:value="serviceType.id"
              v-bind:selected="serviceType.id === service.type"
            >
              {{serviceType.name}}
            </option>
          </select>
          <label>Время начала</label>
          <input type="time" v-model="service.startDatetime"/>
          <label>Время завершения</label>
          <input type="time" v-model="service.finishDatetime"/>
          <label>Администратор</label>
          <select v-model="service.adminId">
            <option
              v-for="employee in admins"
              v-bind:key="employee.id"
              v-bind:value="employee.id"
              v-bind:selected="employee.id === service.adminId"
            >
              {{employee.name}}
            </option>
          </select>
          <label>Мастер</label>
          <select v-model="service.masterId">
            <option
              v-for="employee in masters"
              v-bind:key="employee.id"
              v-bind:value="employee.id"
              v-bind:selected="employee.id === service.masterId"
            >
              {{employee.name}}
            </option>
          </select>
          <label>Клиент</label>
          <select v-model="service.clientId">
            <option
              v-for="client in clients"
              v-bind:key="client.id"
              v-bind:value="client.id"
              v-bind:selected="client.id === service.clientId"
            >
              {{$store.getters.getClientDescription(client.id) || 'Новый клиент'}}
            </option>
          </select>
          <label>Сумма (наличка)</label>
          <input type="number" v-model="service.cashSum"/>
          <label>Сумма (безнал)</label>
          <input type="number" v-model="service.cashlessSum"/>
          <label>Скидка, руб.</label>
          <input type="number" v-model="service.discountSum"/>
          <label>Оценка от клиента от 1 до 10</label>
          <input type="number" v-model="service.score"/>
          <label>Отзыв клиента</label>
          <textarea rows="2" v-model="service.review"></textarea>
          <label>Фотографии</label>
          <input ref="images" type="file" multiple="multiple" accept="image/*">
          <label>Комментарий</label>
          <textarea rows="2" v-model="service.comment"></textarea>
          <h2>Проданные товары</h2>
          <div v-for="(soldItem, index) in soldGoods" v-bind:key="soldItem.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(soldItem)"
                v-if="session.state === 'open'"
              >
                Удалить
              </button>
            </label>
            <select v-model="soldItem.type">
              <option
                v-for="item in goodsTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === soldItem.type"
              >
                {{item.name}}
              </option>
            </select>
            <label>Количество</label>
            <input type="number" v-model="soldItem.amount">
            <label>Сумма (наличка)</label>
            <input type="number" v-model="soldItem.cashSum">
            <label>Сумма (безнал)</label>
            <input type="number" v-model="soldItem.cashlessSum">
            <label>Скидка, руб.</label>
            <input type="number" v-model="soldItem.discountSum">
            <label>Комментарий</label>
          <textarea rows="2" v-model="soldItem.comment"></textarea>
          </div>
          <div>
            <button
              class="button secondary"
              type="button"
              @click="addItem"
              v-if="session.state === 'open'"
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
                v-if="session.state === 'open'"
              >
                Удалить
              </button>
            </label>
            <select v-model="expense.type">
              <option
                v-for="item in spendTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === expense.type"
              >
                {{item.name}}
              </option>
            </select>
            <label>Сумма</label>
            <input type="number" v-model="expense.sum">
            <label>Комментарий</label>
          <textarea rows="2" v-model="expense.comment"></textarea>
          </div>
          <div>
            <button class="button secondary" type="button" @click="addExpense">Добавить расход</button>
          </div>
          <h2>Выплаты мастеру</h2>
          <div v-for="(payment, index) in employeePayments" v-bind:key="payment.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Выплата мастеру {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeEmployeePayment(payment)"
                v-if="session.state === 'open'"
              >
                Удалить
              </button>
            </label>
            <select v-model="payment.type">
              <option
                v-for="item in employeePaymentTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === payment.type"
              >
                {{item.name}}
              </option>
            </select>
            <label>Сумма</label>
            <input type="number" v-model="payment.sum">
            <label>Комментарий</label>
          <textarea rows="2" v-model="payment.comment"></textarea>
          </div>
          <div>
            <button
              class="button secondary"
              type="button"
              @click="addEmployeePayment"
              v-if="session.state === 'open'"
            >
              Добавить выплату мастеру
            </button>
          </div>
          <div v-if="session.state === 'open'" class="grid-x align-justify">
            <button class="button primary cell shrink" type="button" @click="save">Сохранить</button>
            <button class="button alert cell shrink" type="button" @click="deleteOperation">Удалить</button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditService',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.session = {
        'state': 'open'
      }
      this.operations = [
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
          'id': 7,
          'officeId': 1,
          'sessionId': 1,
          'type': 2,
          'datetime': '21.09.2019 12:44',
          'sum': 600,
          'comment': ''
        },
        {
          'operationType': 'employeePayment',
          'id': 8,
          'officeId': 1,
          'sessionId': 1,
          'employeeId': 4,
          'type': 2,
          'datetime': '21.09.2019 18:22',
          'sum': 600,
          'comment': ''
        }
      ]
    }
  },
  data () {
    return {
      session: {
        'state': this.$route.query.sessionState || 'open'
      },
      operations: [
        {
          'operationType': 'service',
          'sessionId': this.$route.query.sessionId,
          'id': null,
          'officeId': this.$route.query.officeId,
          'type': this.$route.query.serviceTypeId,
          'startDatetime': this.$store.getters.getDateTimeNow,
          'finishDatetime': null,
          'adminId': this.$route.query.adminId,
          'masterId': this.$route.query.masterId,
          'clientId': null,
          'cashSum': 0,
          'cashlessSum': 0,
          'discountSum': 0,
          'adminBonus': 0,
          'masterBonus': 0,
          'score': null,
          'review': '',
          'photoUrls': [],
          'comment': ''
        }
      ]
    }
  },
  methods: {
    addItem: function () {
      this.operations.push({
        'operationType': 'goodSell',
        'id': null,
        'type': 1,
        'sessionId': this.$route.query.sessionId,
        'officeId': this.$route.query.officeId,
        'datetime': this.$store.getters.getDateTimeNow,
        'adminId': this.$route.query.adminId,
        'masterId': this.$route.query.masterId,
        'clientId': 1,
        'amount': 1,
        'cashSum': 0,
        'cashlessSum': 0,
        'discountSum': 0,
        'adminBonus': 0,
        'masterBonus': 0,
        'comment': ''
      })
    },
    removeItem: function (item) {
      var index = this.operations.findIndex(o => o.operationType === 'goodSell' && o.type === item.type && o.id === item.id)
      this.operations.splice(index, 1)
    },
    addExpense: function () {
      this.operations.push({
        'operationType': 'spend',
        'id': null,
        'type': 1,
        'sessionId': this.$route.query.sessionId,
        'officeId': this.$route.query.officeId,
        'datetime': this.$store.getters.getDateTimeNow,
        'sum': 500,
        'comment': ''
      })
    },
    removeExpense: function (item) {
      var index = this.operations.findIndex(o => o.operationType === 'spend' && o.type === item.type && o.id === item.id)
      this.operations.splice(index, 1)
    },
    addEmployeePayment: function () {
      this.operations.push({
        'operationType': 'employeePayment',
        'id': null,
        'type': 1,
        'sessionId': this.$route.query.sessionId,
        'officeId': this.$route.query.officeId,
        'datetime': this.$store.getters.getDateTimeNow,
        'employeeId': 4,
        'sum': 500,
        'comment': ''
      })
    },
    removeEmployeePayment: function (item) {
      var index = this.operations.findIndex(o => o.operationType === 'employeePayment' && o.type === item.type && o.id === item.id)
      this.operations.splice(index, 1)
    },
    save: function () {},
    deleteOperation: function () {}
  },
  computed: {
    serviceTypes: {
      get () {
        return this.$store.state.serviceTypes
      }
    },
    clients: {
      get () {
        var clientsCopy = [...this.$store.state.clients]
        clientsCopy.unshift({
          id: null,
          name: '',
          photoUrl: '',
          contacts: [
            {
              type: 'phone',
              value: ''
            }
          ]
        })
        return clientsCopy
      }
    },
    admins: {
      get () {
        return this.$store.state.employees.filter(e => e.roles.includes('officeAdmin'))
      }
    },
    masters: {
      get () {
        return this.$store.state.employees.filter(e => e.roles.includes('master'))
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
    service: {
      get () {
        return this.operations.filter(o => o.operationType === 'service')[0]
      },
      set (item) {
        var index = this.operations.findIndex(o => o.operationType === 'service')
        this.operations.$set(index, item)
      }
    },
    soldGoods: {
      get () {
        return this.operations.filter(o => o.operationType === 'goodSell')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.operationType === 'goodSell' && o.type === item.type && o.id === item.id)
        this.operations.$set(index, item)
      }
    },
    expenses: {
      get () {
        return this.operations.filter(o => o.operationType === 'spend')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.operationType === 'spend' && o.type === item.type && o.id === item.id)
        this.operations.$set(index, item)
      }
    },
    employeePayments: {
      get () {
        return this.operations.filter(o => o.operationType === 'employeePayment')
      },
      set (item) {
        var index = this.operations.findIndex(o => o.operationType === 'employeePayment' && o.type === item.type && o.id === item.id && o.employeeId === item.employeeId)
        this.operations.$set(index, item)
      }
    }
  }
}
</script>

<style>
</style>
