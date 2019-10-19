<template>
  <main>
    <appMenu :selected-element="operations[0].sessionId === $store.state.currentSession.id ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="operations[0].sessionId === $store.state.currentSession.id"><router-link to="/Session">Смена</router-link></li>
          <li v-else><router-link to="/SessionsHistory">История смен и операций</router-link></li>
        </ul>
      </nav>
      <h1>Продажа товаров</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <div v-for="(soldItem, index) in operations" v-bind:key="soldItem.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(soldItem)"
                v-if="operations[0].sessionId === $store.state.currentSession.id && index > 0"
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
            <label>Время продажи</label>
            <input type="text" v-model="soldItem.datetime"/>
            <label>Администратор</label>
            <v-select
              :clearable="false"
              v-model="soldItem.adminId"
              :reduce="s => s.id"
              :value="soldItem.adminId"
              label="name"
              :options="admins"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Мастер</label>
            <v-select
              :clearable="false"
              v-model="soldItem.masterId"
              :reduce="s => s.id"
              :value="soldItem.masterId"
              label="name"
              :options="masters"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Клиент</label>
            <v-select
              :clearable="false"
              v-model="soldItem.clientId"
              :reduce="s => s.id"
              :value="soldItem.clientId"
              :get-option-label="$store.getters.getClientDescription"
              :options="clients"
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
  name: 'EditGoodsSell',
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
    save: function () {},
    deleteOperation: function () {}
  },
  computed: {
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
    }
  }
}
</script>

<style>
</style>
