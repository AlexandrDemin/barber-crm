<template>
  <main class="translucent-theme-back">
    <appMenu selected-element="session" visual-style="translucent"></appMenu>
    <div class="session-content">
      <div class="grid-x grid-margin-x grid-margin-y">
        <masterCard
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-if="employee.role === 'master'"
          v-bind:master="employee"
          />
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import MasterCard from '@/components/MasterCard'

export default {
  name: 'Session',
  components: {
    appMenu: Menu,
    masterCard: MasterCard
  },
  mounted: function () {
    document.title = this.$route.meta.title
  },
  data () {
    return {
      session: {
        'id': 1,
        'dateOpened': '21.09.2019 09:30',
        'dateClosed': null,
        'employees': [
          {
            'Id': 1,
            'name': 'Алексей Луцай',
            'role': 'officeAdmin',
            'pictureUrl': '',
            'workHours': 6
          },
          {
            'Id': 2,
            'name': 'Мария Попова',
            'role': 'master',
            'pictureUrl': 'static/user_photos/мария.jpg',
            'workHours': 6
          },
          {
            'Id': 3,
            'name': 'Макс Корж',
            'role': 'master',
            'pictureUrl': 'static/user_photos/макс.jpg',
            'workHours': 6
          },
          {
            'Id': 4,
            'name': 'Прокофий Иванов',
            'role': 'master',
            'pictureUrl': '',
            'workHours': 6
          }
        ],
        'officeId': 1,
        'state': 'open',
        'Operations': [
          {
            'operationType': 'service',
            'id': 1,
            'officeId': 1,
            'type': 'Стрижка мужская',
            'started': '21.09.2019 09:30',
            'finished': '21.09.2019 10:30',
            'adminId': 1,
            'masterId': 2,
            'clientId': 1,
            'cashSum': 600,
            'cashlessSum': 0,
            'discountSum': 0,
            'score': null,
            'review': '',
            'photoUrls': [],
            'comment': ''
          },
          {
            'operationType': 'itemSell',
            'id': 2,
            'officeId': 1,
            'sessionId': 1,
            'type': [2, 44, 21],
            'datetime': '21.09.2019 09:30',
            'adminId': 1,
            'masterId': 2,
            'clientId': 1,
            'cashSum': 0,
            'cashlessSum': 2350,
            'discountSum': 0,
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
    }
  }
}
</script>

<style>
  .session-content {
    margin: 30px 30px 0 130px;
  }
</style>
