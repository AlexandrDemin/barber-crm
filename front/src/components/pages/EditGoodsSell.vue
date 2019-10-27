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
      <h1>Продажа товаров</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Администратор</label>
          <v-select
            :clearable="false"
            v-model="adminId"
            :reduce="s => s.id"
            :value="adminId"
            label="name"
            :options="admins"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Мастер</label>
          <v-select
            :clearable="false"
            v-model="masterId"
            :reduce="s => s.id"
            :value="masterId"
            label="name"
            :options="masters"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Клиент</label>
          <v-select
            :clearable="false"
            v-model="clientId"
            :reduce="s => s.id"
            :value="clientId"
            :get-option-label="$store.getters.getClientDescription"
            :options="clients"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <div v-if="clientId === null">
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
          <div v-for="(soldItem, index) in operations" v-bind:key="soldItem.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(soldItem)"
                v-if="canEdit && index > 0"
              >
                Удалить
              </button>
            </label>
            <v-select
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
  name: 'EditGoodsSell',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    } else {
      this.operations = [this.getEmptyItem()]
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
      newClient: this.getEmptyClient(),
      operations: [],
      adminId: this.$route.query.adminId || this.admins[0].id,
      masterId: this.$route.query.masterId || this.masters[0].id,
      clientId: null
    }
  },
  methods: {
    addItem: function () {
      this.operations.push(this.getEmptyItem())
    },
    removeItem: function (item) {
      var index = this.operations.findIndex(o => o.operationType === 'goodsoperation' && o.goodsId === item.goodsId && o.id === item.id)
      this.operations.splice(index, 1)
    },
    getEmptyItem: function () {
      return {
        'operationType': 'goodsoperation',
        'id': null,
        'goodsId': this.goodsTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': this.moment(),
        'adminId': this.adminId,
        'masterId': this.masterId,
        'clientId': null,
        'amount': 1,
        'cashSum': this.goodsTypes[0].price,
        'cashlessSum': 0,
        'discountSum': 0,
        'adminBonusSum': 0,
        'masterBonusSum': 0,
        'comment': ''
      }
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetGoodsOperation/`, {'id': id})
        .then(response => {
          var operation = response.data
          operation.operationType = 'goodsoperation'
          operation.datetime = this.moment(operation.datetime, 'DD.MM.YYYY HH:mm')
          this.operations = [operation]
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
        if (operations[index].operationType === 'serviceoperation' || operations[index].operationType === 'goodsoperation') {
          operations[index].adminBonusSum = this.getAdminBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].adminId, operations[index].operationType)
          operations[index].masterBonusSum = this.getMasterBonus(operations[index].cashSum + operations[index].cashlessSum, operations[index].masterId, operations[index].operationType)
          operations[index].adminId = this.adminId
          operations[index].masterId = this.masterId
          operations[index].clientId = this.clientId
        }
      }
      this.operations = operations
      if (this.clientId === null) {
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
                this.$router.push({ path: '/' })
                this.isSaving = false
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
        var clientId = this.clientId
        operations = this.operations
        for (index in operations) {
          if ('clientId' in operations[index]) {
            operations[index].clientId = clientId
          }
        }
        this.operations = operations
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
    getAdminBonus: function (sum, adminId, operationType) {
      var admin = this.admins.filter(x => x.id === adminId)[0]
      console.log(admin)
      if (operationType === 'serviceoperation') {
        return sum * admin.servicePercent
      }
      if (operationType === 'goodsoperation') {
        return sum * admin.goodsPercent
      }
    },
    getMasterBonus: function (sum, masterId, operationType) {
      var master = this.masters.filter(x => x.id === masterId)[0]
      console.log(master)
      if (operationType === 'serviceoperation') {
        return sum * master.servicePercent
      }
      if (operationType === 'goodsoperation') {
        return sum * master.goodsPercent
      }
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
    clients: {
      get () {
        return this.$store.state.clients
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
    contactTypes: {
      get () {
        return this.$store.state.contactTypes
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
