<template>
  <main>
    <appMenu selected-element="history"></appMenu>
    <div class="content">
      <h1>История смен и операций</h1>
      <div class="grid-x grid-padding-x no-padding-small">
        <div class="cell large-4 small-12">
          <label>Дата от</label>
          <input type="date" v-model="dateFrom">
        </div>
        <div class="cell large-4 small-12">
          <label>Дата до</label>
          <input type="date" v-model="dateTo">
        </div>
        <div class="cell large-4 small-12">
          <label>Типы операций</label>
          <v-select
            multiple
            v-model="selectedOperationTypes"
            :reduce="s => s.id"
            :value="selectedOperationTypes"
            label="name"
            :options="operationTypes"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
        </div>
        <div class="cell large-4 small-12">
          <label>Отделения</label>
          <v-select
            multiple
            v-model="officeIds"
            :reduce="s => s.id"
            :value="officeIds"
            label="name"
            :options="offices"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
        </div>
        <div class="cell large-4 small-12">
          <label>Клиенты</label>
          <v-select
            multiple
            v-model="clientIds"
            :reduce="s => s.id"
            :value="clientIds"
            :get-option-label="$store.getters.getClientDescription"
            :options="clients"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
        </div>
        <div class="cell large-4 small-12">
          <label>Сотрудники</label>
          <v-select
            multiple
            v-model="employeeIds"
            :reduce="s => s.id"
            :value="employeeIds"
            label="name"
            :options="employees"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
        </div>
        <div class="cell small-12">
          <button class="button primary" type="button" @click="load">Показать</button>
          <button class="button secondary" type="button" @click="exportToExcel">Выгрузить в .xlsx</button>
        </div>
      </div>
      <div
        v-if="sessions.length > 0"
        v-for="session in sessions"
        v-bind:key="session.id"
      >
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <h3>Смена {{session.dateOpened}} {{$store.getters.getOfficeName(session.officeId)}}</h3>
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
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'SessionsHistory',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
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
      isLoading: false,
      error: '',
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
    load: function () {},
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
