<template>
  <main>
    <appMenu v-bind:selected-element="service.sessionId === $store.state.currentSession.id ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="service.sessionId === $store.state.currentSession.id"><router-link to="/Session">Смена</router-link></li>
          <li v-else><router-link to="/SessionsHistory">История смен и операций</router-link></li>
        </ul>
      </nav>
      <h1>Услуга</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Услуга</label>
          <v-select
            :clearable="false"
            v-model="service.type"
            :reduce="s => s.id"
            :value="service.type"
            label="name"
            :options="serviceTypes"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <div class="grid-x grid-margin-x">
            <div class="cell medium-6">
              <label>Время начала</label>
              <input type="time" v-model="service.startDatetime"/>
            </div>
            <div class="cell medium-6">
              <label>Время завершения</label>
              <input type="time" v-model="service.finishDatetime"/>
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
          <button class="button secondary">Загрузить фотографии</button>
          <input ref="images" type="file" style="display:none" multiple="multiple" accept="image/*">
          <label>Комментарий</label>
          <textarea rows="2" v-model="service.comment"></textarea>
          <h2>Проданные товары</h2>
          <div v-for="(soldItem, index) in soldGoods" v-bind:key="soldItem.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(soldItem)"
                v-if="operations[0].sessionId === $store.state.currentSession.id"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              v-model="soldItem.type"
              :reduce="s => s.id"
              :value="soldItem.type"
              label="name"
              :options="goodsTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
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
              v-if="operations[0].sessionId === $store.state.currentSession.id"
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
                v-if="operations[0].sessionId === $store.state.currentSession.id"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              v-model="expense.type"
              :reduce="s => s.id"
              :value="expense.type"
              label="name"
              :options="spendTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
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
                v-if="operations[0].sessionId === $store.state.currentSession.id"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              v-model="payment.type"
              :reduce="s => s.id"
              :value="payment.type"
              label="name"
              :options="employeePaymentTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
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
              v-if="operations[0].sessionId === $store.state.currentSession.id"
            >
              Добавить выплату мастеру
            </button>
          </div>
          <div v-if="operations[0].sessionId === $store.state.currentSession.id">
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary" type="button" @click="save">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'EditService',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
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
      isLoading: false,
      isSaving: false,
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
