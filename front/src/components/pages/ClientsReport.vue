<template>
  <main>
    <appMenu selected-element="reports"></appMenu>
    <div class="content">
      <h1>Отчёт по клиентам</h1>
      <div class="grid-x grid-padding-x no-padding-small">
        <div class="cell large-4 small-12">
          <label>Месяц</label>
          <v-select
            :clearable="false"
            v-model="period"
            :value="period"
            label="name"
            :options="periods"
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
        <div class="cell small-12">
          <button class="button primary" type="button" @click="load">Показать</button>
        </div>
      </div>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div v-if="!loadingError && !isLoading && summary && (!summary.totalvisitsduringperiod || (byOffices.length && byOffices.warning))">Нет данных по выбранным фильтрам</div>
        <div v-if="!loadingError && !isLoading && summary && summary.totalvisitsduringperiod">
          <h2>Итого</h2>
          <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{uniqueClientsCount || 0}}</div>
              <label>{{inclineWord(uniqueClientsCount, 'Клиент', 'Клиента', 'Клиентов')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalvisitsduringperiod || 0}}</div>
              <label>{{inclineWord(summary.totalvisitsduringperiod, 'Посещение', 'Посещения', 'Посещений')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalsum || 0}}</div>
              <label>Выручка, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalservicesum || 0}}</div>
              <label>Выручка от&nbsp;услуг, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalgoodssum || 0}}</div>
              <label>Выручка от&nbsp;продажи товаров, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalcash || 0}}</div>
              <label>Наличка, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totalcashless || 0}}</div>
              <label>Безнал, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-auto">
              <div class="big-number">{{summary.totaldiscount || 0}}</div>
              <label>Скидки, ₽</label>
            </div>
          </div>
          <div class="table-container margin-bottom-30px">
            <table class="hover">
              <thead>
                <tr>
                  <th class="sticky-header">Клиент</th>
                  <th class="sticky-header">Выручка</th>
                  <th class="sticky-header">Выручка от&nbsp;услуг</th>
                  <th class="sticky-header">Выручка от&nbsp;продажи товаров</th>
                  <th class="sticky-header">Наличка</th>
                  <th class="sticky-header">Безнал</th>
                  <th class="sticky-header">Скидки</th>
                  <th class="sticky-header">Посещения&nbsp;за выбранный период</th>
                  <th class="sticky-header">Посещения мастеров за&nbsp;всё время</th>
                  <th class="sticky-header">Посещения всего</th>
                  <th class="sticky-header">Посещения&nbsp;за последние 6&nbsp;мес.</th>
                  <th class="sticky-header">Предыдущее посещение</th>
                  <th class="sticky-header">Новый клиент</th>
                  <th class="sticky-header">Лояльность</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="client in byClients" v-bind:key="client.clientId">
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.name || 'Неизвестно'}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalsum || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalservicesum || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalgoodssum || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalcash || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalcashless || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totaldiscount || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalvisitsduringperiod}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      <div v-for="visit in client.mastervisits" v-bind:key="visit">
                        <div><router-link :to="'/EditEmployee/' + visit.masterId.toString()">{{visit.name}}</router-link></div>
                        <div class="margin-bottom-10px">{{visit.count || 0}} {{inclineWord(visit.count, 'раз', 'раза', 'раз')}}</div>
                      </div>
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.totalvisits}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.lastndaysvisitscount || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.lastvisitdatetime || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                      {{client.newclient ? 'Да' : 'Нет'}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link" v-html="getLoyalityDescription(client.loyalty)"></router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-if="!loadingError && !isLoading && byOffices && byOffices.length && !byOffices.warning">
          <h2>По отделениям</h2>
          <div
            v-if="!isLoading"
            v-for="office in byOffices"
            v-bind:key="office.id"
          >
            <h3>{{$store.getters.getOfficeName(office.officeId)}}</h3>
            <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.uniqueClientsCount || 0}}</div>
                <label>{{inclineWord(office.uniqueClientsCount, 'Клиент', 'Клиента', 'Клиентов')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalvisitsduringperiod || 0}}</div>
                <label>{{inclineWord(office.totalvisitsduringperiod, 'Посещение', 'Посещения', 'Посещений')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalsum || 0}}</div>
                <label>Выручка, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalservicesum || 0}}</div>
                <label>Выручка от&nbsp;услуг, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalgoodssum || 0}}</div>
                <label>Выручка от&nbsp;продажи товаров, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalcash || 0}}</div>
                <label>Наличка, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totalcashless || 0}}</div>
                <label>Безнал, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-auto">
                <div class="big-number">{{office.totaldiscount || 0}}</div>
                <label>Скидки, ₽</label>
              </div>
            </div>
            <div>
              <button class="button secondary small" @click="showOfficeDetails(office)">
                {{office.detailsShown ? 'Скрыть' : 'Показать' + ' детализацию по клиентам отделения'}}
              </button>
            </div>
            <div class="table-container margin-bottom-30px" v-if="office.detailsShown">
              <table class="hover">
                <thead>
                  <tr>
                    <th class="sticky-header">Клиент</th>
                    <th class="sticky-header">Выручка</th>
                    <th class="sticky-header">Выручка от&nbsp;услуг</th>
                    <th class="sticky-header">Выручка от&nbsp;продажи товаров</th>
                    <th class="sticky-header">Наличка</th>
                    <th class="sticky-header">Безнал</th>
                    <th class="sticky-header">Скидки</th>
                    <th class="sticky-header">Посещения&nbsp;за выбранный период</th>
                    <th class="sticky-header">Посещения мастеров за&nbsp;всё время</th>
                    <th class="sticky-header">Посещения всего</th>
                    <th class="sticky-header">Посещения&nbsp;за последние 6&nbsp;мес.</th>
                    <th class="sticky-header">Предыдущее посещение</th>
                    <th class="sticky-header">Новый клиент</th>
                    <th class="sticky-header">Лояльность</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="client in office.clients" v-bind:key="client.clientId">
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.name || 'Неизвестно'}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalsum || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalservicesum || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalgoodssum || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalcash || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalcashless || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totaldiscount || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalvisitsduringperiod}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        <div v-for="visit in client.mastervisits" v-bind:key="visit">
                          <div><router-link :to="'/EditEmployee/' + visit.masterId.toString()">{{visit.name}}</router-link></div>
                          <div class="margin-bottom-10px">{{visit.count || 0}} {{inclineWord(visit.count, 'раз', 'раза', 'раз')}}</div>
                        </div>
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.totalvisits}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.lastndaysvisitscount || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.lastvisitdatetime || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link">
                        {{client.newclient ? 'Да' : 'Нет'}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditClient/ + parseInt(client.clientId)" class="table-link" v-html="getLoyalityDescription(client.loyalty)"></router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
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
  name: 'ClientsReport',
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
      period: this.moment().format('MM YYYY'),
      clientIds: [],
      officeIds: [],
      isLoading: false,
      loadingError: '',
      summary: null,
      byOffices: [],
      byClients: [],
      byOfficesAndClients: []
    }
  },
  methods: {
    load: function () {
      this.isLoading = true
      this.loadingError = ''
      var data = {
        period: this.moment(this.period, 'MM YYYY').format('DD.MM.YYYY')
      }
      if (this.clientIds && this.clientIds.length > 0) {
        data.clientIds = this.clientIds
      }
      if (this.officeIds && this.officeIds.length > 0) {
        data.officeIds = this.officeIds
      }
      HTTP.post(`GenerateClientReport/`, data)
        .then(response => {
          this.summary = response.data.summary[0]
          if (!response.data.byOfficeAndClient.warning) {
            for (var index in response.data.byOffices) {
              var office = response.data.byOffices[index]
              office.clients = response.data.byOfficeAndClient.filter(x => x.officeId === office.officeId)
              office.detailsShown = false
              office.uniqueClientsCount = new Set(office.clients.map(x => x.clientId)).size
            }
          }
          this.byOffices = response.data.byOffices
          this.byClients = response.data.byClients
          this.byOfficesAndClients = response.data.byOfficeAndClient
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.summary = null
          this.byOffices = []
          this.byClients = []
          this.byOfficesAndClients = []
          this.isLoading = false
        })
    },
    inclineWord: function (num, form1, form2, form3) {
      if (num) {
        var lastDigit = num.toString()[num.toString().length - 1]
        if (['5', '6', '7', '8', '9', '0'].includes(lastDigit) || (num % 100 > 10 && num % 100 < 20)) {
          return form3
        }
        if (['2', '3', '4'].includes(lastDigit)) {
          return form2
        }
        if (lastDigit === '1') {
          return form1
        }
      }
      return form1
    },
    showOfficeDetails: function (office) {
      office.detailsShown = !office.detailsShown
    },
    getLoyalityDescription: function (loyality) {
      switch (loyality) {
        case 'lost':
          return '<span title="Не посещал 3 месяца">Потерян</span>'
        case 'likely lost':
          return '<span title="Не посещал более 40 дней">Вероятно потерян</span>'
        case 'loyal':
          return '<span title="Более 2 посещений за 3 месяца, последнее не более 40 дней назад">Лоялен</span>'
        case 'likely loyal':
          return '<span title="Более 1 посещения за 3 месяца, последнее не более 40 дней назад">Вероятно лоялен</span>'
        case 'ambivalent':
          return 'Пока не ясно'
      }
      return loyality
    }
  },
  computed: {
    offices: {
      get () {
        return this.$store.state.offices
      }
    },
    clients: {
      get () {
        return this.$store.state.clients
      }
    },
    periods () {
      var periods = []
      for (var i = 0; i <= 12; i++) {
        periods.push(this.moment().subtract(i, 'months').format('MM YYYY'))
      }
      return periods
    },
    uniqueClientsCount () {
      if (this.byClients && this.byClients.length && !this.byClients.warning && !this.byClients.error) {
        return new Set(this.byClients.map(x => x.clientId)).size
      }
    }
  }
}
</script>

<style>
</style>
