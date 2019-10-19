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
      <h1>Выплата сотруднику</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <div v-for="(payment, index) in operations" v-bind:key="payment.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Выплата сотруднику {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeEmployeePayment(payment)"
                v-if="operations[0].sessionId === $store.state.currentSession.id && index > 0"
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
            <label>Время</label>
            <input type="text" v-model="payment.datetime"/>
            <label>Сотрудник</label>
            <v-select
              :clearable="false"
              v-model="payment.employeeId"
              :reduce="s => s.id"
              :value="payment.employeeId"
              label="name"
              :options="employees"
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
              Добавить выплату сотруднику
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
  name: 'EditEmployeePayment',
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
          'operationType': 'employeePayment',
          'id': null,
          'type': 1,
          'sessionId': this.$route.query.sessionId,
          'officeId': this.$route.query.officeId,
          'datetime': this.$store.getters.getDateTimeNow,
          'employeeId': 4,
          'sum': 500,
          'comment': ''
        }
      ]
    }
  },
  methods: {
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
    employees: {
      get () {
        return this.$store.state.employees
      }
    },
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      }
    }
  }
}
</script>

<style>
</style>
