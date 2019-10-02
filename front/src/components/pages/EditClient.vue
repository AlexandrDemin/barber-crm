<template>
  <main>
    <appMenu selected-element="clients"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/Clients">Клиенты</router-link></li>
        </ul>
      </nav>
      <h1>Клиент</h1>
      <div class="grid-x">
        <form class="cell large-6">
          <label>Имя</label>
          <input type="text" v-model="client.name"/>
          <label>Фото</label>
          <input type="file" accept="image/*">
          <div v-for="(contact, index) in client.contacts" v-bind:key="contact">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Контакт {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeContact(index)"
              >
                Удалить
              </button>
            </label>
            <select v-model="contact.type">
              <option
                v-for="item in contactTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === contact.type"
              >
                {{item.name}}
              </option>
            </select>
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
          <div>
            <button class="button primary" type="button" @click="save">Сохранить</button>
            <button class="button secondary" type="button" @click="saveAndAddMore">Сохранить и добавить ещё клиента</button>
          </div>
        </form>
      </div>
      <div v-if="client.id">
        <h2>История операций по клиенту</h2>
        <table class="operations-table hover">
          <thead>
            <tr>
              <th>Дата</th>
              <th>Мастер</th>
              <th>Услуга / товар</th>
              <th>Сумма</th>
              <th>Премия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="operation in client.operations" v-bind:key="operation.id">
              <td>
                <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                  {{$store.getters.getDateTimeFromOperation(operation)}}
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
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditClient',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.client = {
        id: 1,
        name: 'Иван',
        photoUrl: '',
        contacts: [
          {
            type: 'phone',
            value: '89203342284'
          },
          {
            type: 'telegram',
            value: '89203342284'
          }
        ],
        operations: [
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
          }
        ]
      }
    }
  },
  data () {
    return {
      client: {
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
  methods: {
    addContact: function () {
      this.client.contacts.push({
        type: 'phone',
        value: ''
      })
    },
    removeContact: function (index) {
      this.client.contacts.splice(index, 1)
    },
    save: function () {},
    saveAndAddMore: function () {
      this.client = {
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
      this.$router.push('/EditClient')
    }
  },
  computed: {
    contactTypes: {
      get () {
        return this.$store.state.contactTypes
      }
    }
  }
}
</script>

<style>
</style>
