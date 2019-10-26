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
          <div v-if="service.clientId === null">
            <label>Имя</label>
            <input type="text" v-model="newClient.name" autofocus/>
            <label>Фото</label>
            <button type="button" class="button secondary">Выбрать</button>
            <input type="file" accept="image/*" style="display:none" ref="photoSelector">
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
            <label>Комментарий</label>
            <textarea rows="3" v-model="newClient.comment"></textarea>
            <div v-if="savingError" class="callout alert">
              <h5>Произошла ошибка при сохранении клиента</h5>
              <p>{{savingError}}</p>
            </div>
          </div>
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
                v-if="canEdit"
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
          <div v-if="canEdit">
            <button
              class="button secondary"
              type="button"
              @click="addEmployeePayment"
            >
              Добавить выплату мастеру
            </button>
          </div>
          <div v-if="canEdit">
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
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    } else {
      this.operations = this.getEmptyItem()
    }
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
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetServiceOperation/`, {'id': id})
        .then(response => {
          var service = response.data
          this.service = service
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
      HTTP.post(`EditOperations/`, this.operations)
        .then(response => {
          this.$store.dispatch('getCurrentSession')
          this.$router.push({ path: '/' })
          this.isSaving = false
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    getEmptyItem: function () {
      return [
        {
          'operationType': 'service',
          'sessionId': this.$store.state.currentSession.id,
          'id': null,
          'officeId': this.$store.state.currentSession.officeId,
          'type': this.$route.query.serviceTypeId,
          'startDatetime': this.moment().subtract(1, 'hours'),
          'finishDatetime': this.moment(),
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
          'photoUrls': null,
          'comment': ''
        }
      ]
    },
    getEmptyClient: function () {
      return {
        id: null,
        name: '',
        photoUrl: '',
        contacts: [
          {
            type: 'phone',
            value: ''
          }
        ]
      }
    }
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
        clientsCopy.unshift(this.getEmptyClient())
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
    },
    canEdit: function () {
      if (this.operations[0]) {
        return !this.operations[0].id || (this.operations[0].sessionId === this.$store.state.currentSession.id)
      }
      return false
    }
  }
}
</script>

<style>
</style>
