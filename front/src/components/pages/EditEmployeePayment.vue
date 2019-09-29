<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content">
      <h1>Выплата сотруднику</h1>
      <div class="grid-x">
        <form class="cell large-6">
          <div v-for="(payment, index) in operations" v-bind:key="payment.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Выплата сотруднику {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeEmployeePayment(payment)"
                v-if="session.state === 'open' && index > 0"
              >
                Удалить
              </button>
            </label>
            <select v-model="payment.type">
              <option
                v-for="item in employeePaymentTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === payment.type"
              >
                {{item.name}}
              </option>
            </select>
            <label>Время</label>
            <input type="text" v-model="payment.datetime"/>
            <label>Сотрудник</label>
            <select v-model="payment.employeeId">
              <option
                v-for="employee in employees"
                v-bind:key="employee.id"
                v-bind:value="employee.id"
                v-bind:selected="employee.id === payment.employeeId"
              >
                {{employee.name}}
              </option>
            </select>
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
              v-if="session.state === 'open'"
            >
              Добавить выплату сотруднику
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
  name: 'EditEmployeePayment',
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
      session: {
        'state': this.$route.query.sessionState || 'open'
      },
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
