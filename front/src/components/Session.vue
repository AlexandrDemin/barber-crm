<template>
  <main class="translucent-theme-back">
    <appMenu selected-element="session" visual-style="translucent"></appMenu>
    <div class="session-content">
      <div class="grid-x grid-margin-x grid-margin-y">
        <div
          v-for="employee in session.employees"
          v-bind:key="employee.id"
          v-if="employee.role === 'master'"
          class="cell large-6 columns translucent-theme-block master-card">
          <div class="master-card-header grid-x">
            <div class="cell small-1">
              <img class="master-card-picture" v-bind:src="employee.pictureUrl"/>
            </div>
            <div class="cell small-5">
              <h4>{{employee.name}}</h4>
            </div>
            <div class="cell small-6 text-right">
              <p>Длина смены <strong>{{employee.workHours}}</strong> ч.</p>
            </div>
          </div>
          <div class="master-card-content">
          </div>
          <div class="master-card-footer grid-x grid-padding-x grid-padding-y">
            <div class="cell medium-6">
              <select>
                <option>Штраф</option>
              </select>
            </div>
            <div class="cell medium-2">
              <input type="text" placeholder="Сумма"/>
            </div>
            <div class="cell medium-4">
              <button class="button secondary">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'Session',
  components: {
    appMenu: Menu
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
  .master-card-header {
    background: #FFFFFF;
    border-radius: 5px 5px 0 0;
  }
  .master-card-picture {
    border-radius: 5px 0 0 0;
  }
  .master-card-footer .cell select,
  .master-card-footer .cell input,
  .master-card-footer .cell button {
    margin: 0;
  }
</style>
