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
        </div>
      </div>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div v-if="noSessions">Не найдено данных, подходящих под заданные фильтры</div>
      <div v-if="isLoading">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
      </div>
      <div
        v-if="!noSessions && !isLoading"
        v-for="session in sessions"
        v-bind:key="session.id"
      >
        <h4><router-link :to="'/EditSession/' + session.id.toString()">Смена {{moment.utc(session.dateOpened, 'DD.MM.YYYY HH:mm').local().format('DD.MM.YY')}} {{$store.getters.getOfficeName(session.officeId)}}</router-link></h4>
        <div class="table-container margin-bottom-30px">
          <table class="operations-table hover">
            <thead>
              <tr>
                <th class="sticky-header">Время</th>
                <th class="sticky-header">Сотрудник</th>
                <th class="sticky-header">Операция</th>
                <th class="sticky-header">Сумма</th>
                <th class="sticky-header">Премия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="operation in session.operations" v-bind:key="operation">
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
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import { HTTP } from '../../api/api.js'
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
    this.load()
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
      loadingError: '',
      noSessions: false,
      sessions: []
    }
  },
  methods: {
    load: function () {
      this.isLoading = true
      this.noSessions = false
      var data = {
        withOperations: true
      }
      if (this.dateFrom) {
        data.dateFrom = this.moment(this.dateFrom).format('DD.MM.YYYY')
      }
      if (this.dateTo) {
        data.dateTo = this.moment(this.dateTo).format('DD.MM.YYYY')
      }
      if (this.selectedOperationTypes && this.selectedOperationTypes.length > 0) {
        data.operationType = this.selectedOperationTypes
      }
      if (this.employeeIds && this.employeeIds.length > 0) {
        data.employeeIds = this.employeeIds
      }
      if (this.clientIds && this.clientIds.length > 0) {
        data.clientIds = this.clientIds
      }
      if (this.officeIds && this.officeIds.length > 0) {
        data.officeIds = this.officeIds
      }
      HTTP.post(`GetSessions/`, data)
        .then(response => {
          this.sessions = response.data
          if (!Array.isArray(this.sessions)) {
            this.noSessions = true
          }
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    }
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
