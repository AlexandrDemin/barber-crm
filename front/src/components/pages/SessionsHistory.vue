<template>
  <main>
    <appMenu selected-element="history"></appMenu>
    <div class="content">
      <h1>История смен и операций</h1>
      <form class="grid-x grid-padding-x no-padding-small">
        <div class="cell large-shrink small-12">
          <label>Дата от</label>
          <input type="date" v-model="dateFrom">
        </div>
        <div class="cell large-shrink small-12">
          <label>Дата до</label>
          <input type="date" v-model="dateTo">
        </div>
        <div class="cell large-shrink small-12">
          <label>Типы операций</label>
          <select v-model="selectedOperationTypes" multiple="multiple">
            <option
              v-for="type in operationTypes"
              v-bind:key="type.id"
              v-bind:value="type.id"
              v-bind:selected="selectedOperationTypes.filter(s => s.id === type.id).length > 0"
            >
              {{type.name}}
            </option>
          </select>
        </div>
        <div class="cell large-shrink small-12">
          <label>Отделения</label>
          <select v-model="officeIds" multiple="multiple">
            <option
              v-for="office in offices"
              v-bind:key="office.id"
              v-bind:value="office.id"
              v-bind:selected="officeIds.filter(s => s.id === office.id).length > 0"
            >
              {{office.name}}
            </option>
          </select>
        </div>
        <div class="cell large-shrink small-12">
          <label>Клиенты</label>
          <select v-model="clientIds" multiple="multiple">
            <option
              v-for="client in clients"
              v-bind:key="client.id"
              v-bind:value="client.id"
              v-bind:selected="clientIds.filter(s => s.id === client.id).length > 0"
            >
              {{client.name}}
            </option>
          </select>
        </div>
        <div class="cell large-shrink small-12">
          <label>Сотрудники</label>
          <select v-model="employeeIds" multiple="multiple">
            <option
              v-for="employee in employees"
              v-bind:key="employee.id"
              v-bind:value="employee.id"
              v-bind:selected="employeeIds.filter(s => s.id === employee.id).length > 0"
            >
              {{employee.name}}
            </option>
          </select>
        </div>
        <div class="cell large-shrink small-12">
          <button class="button primary" type="button" @click="showSessions">Показать</button>
          <button class="button secondary" type="button" @click="exportToExcel">Выгрузить в .xlsx</button>
        </div>
      </form>
      <div
        v-if="sessions.length > 0"
        v-for="session in sessions"
        v-bind:key="session.id"
      >
        <h3>Смена {{session.dateOpened}}</h3>
        <table class="operations-table hover">
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
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'SessionsHistory',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
  },
  data () {
    return {
      dateFrom: null,
      dateTo: null,
      selectedOperationTypes: [],
      employeeIds: [],
      clientIds: [],
      officeIds: [],
      sessions: [
        {
          'id': 1,
          'dateOpened': '21.09.2019 09:30',
          'dateClosed': '21.09.2019 18:30',
          'employees': [
            {
              'id': 1,
              'name': 'Алексей Луцай',
              'role': 'officeAdmin',
              'pictureUrl': '',
              'workHours': 6
            },
            {
              'id': 2,
              'name': 'Мария Попова',
              'role': 'master',
              'pictureUrl': 'static/user_photos/мария.jpg',
              'workHours': 6
            },
            {
              'id': 3,
              'name': 'Макс Корж',
              'role': 'master',
              'pictureUrl': 'static/user_photos/макс.jpg',
              'workHours': 6
            },
            {
              'id': 4,
              'name': 'Прокофий Иванов',
              'role': 'master',
              'pictureUrl': '',
              'workHours': 6
            }
          ],
          'officeId': 1,
          'state': 'closed',
          'operations': [
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
        {
          'id': 2,
          'dateOpened': '22.09.2019 09:25',
          'dateClosed': '22.09.2019 19:25',
          'employees': [
            {
              'id': 1,
              'name': 'Алексей Луцай',
              'role': 'officeAdmin',
              'pictureUrl': '',
              'workHours': 6
            },
            {
              'id': 2,
              'name': 'Мария Попова',
              'role': 'master',
              'pictureUrl': 'static/user_photos/мария.jpg',
              'workHours': 6
            },
            {
              'id': 3,
              'name': 'Макс Корж',
              'role': 'master',
              'pictureUrl': 'static/user_photos/макс.jpg',
              'workHours': 6
            },
            {
              'id': 4,
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
        }
      ]
    }
  },
  methods: {
    showSessions: function () {},
    exportToExcel: function () {}
  },
  computed: {
    operationTypes: {
      get () {
        return this.$store.state.operationTypes
      }
    },
    offices: {
      get () {
        return this.$store.state.offices
      }
    },
    employees: {
      get () {
        return this.$store.state.employees
      }
    },
    clients: {
      get () {
        return this.$store.state.clients
      }
    }
  }
}
</script>

<style>
</style>
