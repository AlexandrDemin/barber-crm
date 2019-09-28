<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">Услуга</h1>
      <form class="cell small-6">
        <label>Услуга</label>
        <select v-model="service.type">
          <option
            v-for="serviceType in serviceTypes"
            v-bind:key="serviceType.id"
            v-bind:value="serviceType.id"
            v-bind:selected="serviceType.id === service.type"
          >
            {{serviceType.name}}
          </option>
        </select>
        <label>Время начала</label>
        <input type="text" v-model="service.startDatetime"/>
        <label>Время завершения</label>
        <input type="text" v-model="service.finishDatetime"/>
        <label>Администратор</label>
        <select v-model="service.adminId">
          <option
            v-for="employee in admins"
            v-bind:key="employee.id"
            v-bind:value="employee.id"
            v-bind:selected="employee.id === service.adminId"
          >
            {{employee.name}}
          </option>
        </select>
        <label>Мастер</label>
        <select v-model="service.masterId">
          <option
            v-for="employee in masters"
            v-bind:key="employee.id"
            v-bind:value="employee.id"
            v-bind:selected="employee.id === service.masterId"
          >
            {{employee.name}}
          </option>
        </select>
        <label>Клиент</label>
        <select v-model="service.clientId">
          <option
            v-for="client in clients"
            v-bind:key="client.id"
            v-bind:value="client.id"
            v-bind:selected="client.id === service.clientId"
          >
            {{$store.getters.getClientDescription(client.id)}}
          </option>
        </select>
        <label>Сумма (наличка)</label>
        <input type="number" v-model="service.cashSum"/>
        <label>Сумма (безнал)</label>
        <input type="number" v-model="service.cashlessSum"/>
        <label>Скидка</label>
        <input type="number" v-model="service.discountSum"/>
        <label>Оценка от клиента от 1 до 10</label>
        <input type="number" v-model="service.score"/>
        <label>Отзыв клиента</label>
        <textarea rows="4" v-model="service.review"></textarea>
        <label>Фотографии</label>
        <input ref="images" type="file" multiple="multiple" accept="image/*">
        <label>Комментарий</label>
        <textarea rows="4" v-model="service.comment"></textarea>
      </form>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditService',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.operations = [
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
          'goodsIds': [1, 2, 3, 4, 5],
          'datetime': '21.09.2019 09:30',
          'adminId': 1,
          'masterId': 3,
          'clientId': 1,
          'cashSum': 0,
          'cashlessSum': 2350,
          'discountSum': 0,
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
  },
  data () {
    return {
      operations: [
        {
          'operationType': 'service',
          'sessionId': this.$route.query.sessionId,
          'id': null,
          'officeId': this.$route.query.sessionId,
          'type': this.$route.query.typeId,
          'startDatetime': this.$store.getters.getDateTimeNow,
          'finishDatetime': null,
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
          'photoUrls': [],
          'comment': ''
        }
      ]
    }
  },
  methods: {},
  computed: {
    serviceTypes: {
      get () {
        return this.$store.state.serviceTypes
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
    service: {
      get () {
        return this.operations.filter(o => o.operationType === 'service')[0]
      },
      set (item) {
        var index = this.operations.findIndex(o => o.operationType === 'service')
        this.operations.$set(index, item)
      }
    }
  }
}
</script>

<style>
</style>
