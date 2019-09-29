<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content">
      <h1>Продажа товаров</h1>
      <div class="grid-x">
        <form class="cell small-6">
          <div v-for="(soldItem, index) in operations" v-bind:key="soldItem.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Товар {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeItem(soldItem)"
                v-if="session.state === 'open' && index > 0"
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
            <label>Время</label>
            <input type="text" v-model="soldItem.datetime"/>
            <label>Администратор</label>
            <select v-model="soldItem.adminId">
              <option
                v-for="employee in admins"
                v-bind:key="employee.id"
                v-bind:value="employee.id"
                v-bind:selected="employee.id === soldItem.adminId"
              >
                {{employee.name}}
              </option>
            </select>
            <label>Мастер</label>
            <select v-model="soldItem.masterId">
              <option
                v-for="employee in masters"
                v-bind:key="employee.id"
                v-bind:value="employee.id"
                v-bind:selected="employee.id === soldItem.masterId"
              >
                {{employee.name}}
              </option>
            </select>
            <label>Клиент</label>
            <select v-model="soldItem.clientId">
              <option
                v-for="client in clients"
                v-bind:key="client.id"
                v-bind:value="client.id"
                v-bind:selected="client.id === soldItem.clientId"
              >
                {{$store.getters.getClientDescription(client.id)}}
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
  name: 'EditGoodsSell',
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
      session: {
        'state': this.$route.query.sessionState || 'open'
      },
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
