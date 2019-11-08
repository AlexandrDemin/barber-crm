<template>
  <main>
    <appMenu selected-element="reports"></appMenu>
    <div class="content">
      <h1>Отчёт по сотрудникам</h1>
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
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div v-if="!loadingError && !isLoading && summary && (!summary.totalsalary || (byOffices.length && byOffices.warning))">Нет данных по выбранным фильтрам</div>
        <div v-if="!loadingError && !isLoading && summary && summary.totalsalary">
          <h2>Итого</h2>
          <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{uniqueEmployeesCount || 0}}</div>
              <label>{{inclineWord(uniqueEmployeesCount, 'Сотрудник', 'Сотрудника', 'Сотрудников')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalsalary || 0}}</div>
              <label>Начисленная заплата, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalpaidsalary || 0}}</div>
              <label>Выплаченая зарплата, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalpenalty || 0}}</div>
              <label>Штрафы, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalunpaidsalary || 0}}</div>
              <label>Невыплаченая зарплата, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{(summary.totalgoodsbonus || 0) + (summary.totalservicebonus || 0)}}</div>
              <label>Начисленная премия, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalservicebonus || 0}}</div>
              <label>Премия (услуги), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalgoodsbonus || 0}}</div>
              <label>Премия (товары), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalpaidbonus || 0}}</div>
              <label>Выплаченная премия, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalunpaidbonus || 0}}</div>
              <label>Невыплаченная премия, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.estimatedworkhours || 0}}</div>
              <label>Рабочие часы в месяце</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.total_time || 0}}</div>
              <label>Отработанные часы</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{((summary.meanworkload || 0) * 100).toFixed(2).toString() + '%'}}</div>
              <label>% отработанных часов</label>
            </div>
          </div>
          <div class="table-container margin-bottom-30px">
            <table class="hover">
              <thead>
                <tr>
                  <th class="sticky-header">Сотрудник</th>
                  <th class="sticky-header">Начисленная заплата</th>
                  <th class="sticky-header">Штрафы</th>
                  <th class="sticky-header">Выплаченая зарплата</th>
                  <th class="sticky-header">Невыплаченая зарплата</th>
                  <th class="sticky-header">Начисленная премия</th>
                  <th class="sticky-header">Премия (услуги)</th>
                  <th class="sticky-header">Премия (товары)</th>
                  <th class="sticky-header">Выплаченная премия</th>
                  <th class="sticky-header">Невыплаченная премия</th>
                  <th class="sticky-header">Рабочие часы в месяце</th>
                  <th class="sticky-header">Отработанные часы</th>
                  <th class="sticky-header">% отработанных часов</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="employee in byEmployees" v-bind:key="employee.employeeId">
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.employeeName || 'Неизвестно'}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalsalary || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalpenalty || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalpaidsalary || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalunpaidsalary || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{(employee.totalgoodsbonus || 0) + (employee.totalservicebonus || 0) || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalservicebonus || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalgoodsbonus || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalpaidbonus || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.totalunpaidbonus || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.estimatedworkhours || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{employee.total_time || 0}}
                    </router-link>
                  </td>
                  <td>
                    <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                      {{((employee.meanworkload || 0) * 100).toFixed(2).toString() + '%'}}
                    </router-link>
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
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.uniqueEmployeesCount || 0}}</div>
                <label>{{inclineWord(office.uniqueEmployeesCount, 'Сотрудник', 'Сотрудника', 'Сотрудников')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalsalary || 0}}</div>
                <label>Начисленная заплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalpaidsalary || 0}}</div>
                <label>Выплаченая зарплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalpenalty || 0}}</div>
                <label>Штрафы, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalunpaidsalary || 0}}</div>
                <label>Невыплаченая зарплата, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{(office.totalgoodsbonus || 0) + (office.totalservicebonus || 0) || 0}}</div>
                <label>Начисленная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalservicebonus || 0}}</div>
                <label>Премия (услуги), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalgoodsbonus || 0}}</div>
                <label>Премия (товары), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalpaidbonus || 0}}</div>
                <label>Выплаченная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalunpaidbonus || 0}}</div>
                <label>Невыплаченная премия, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.estimatedworkhours || 0}}</div>
                <label>Рабочие часы в месяце</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.total_time || 0}}</div>
                <label>Отработанные часы</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{((office.meanworkload || 0) * 100).toFixed(2).toString() + '%'}}</div>
                <label>% отработанных часов</label>
              </div>
            </div>
            <div>
              <button class="button secondary small" @click="showOfficeDetails(office)">
                {{office.detailsShown ? 'Скрыть' : 'Показать детализацию по сотрудникам отделения'}}
              </button>
            </div>
            <div class="table-container margin-bottom-30px" v-if="office.detailsShown">
              <table class="hover">
                <thead>
                  <tr>
                    <th class="sticky-header">Сотрудник</th>
                    <th class="sticky-header">Начисленная заплата</th>
                    <th class="sticky-header">Штрафы</th>
                    <th class="sticky-header">Выплаченая зарплата</th>
                    <th class="sticky-header">Невыплаченая зарплата</th>
                    <th class="sticky-header">Начисленная премия</th>
                    <th class="sticky-header">Премия (услуги)</th>
                    <th class="sticky-header">Премия (товары)</th>
                    <th class="sticky-header">Выплаченная премия</th>
                    <th class="sticky-header">Невыплаченная премия</th>
                    <th class="sticky-header">Рабочие часы в месяце</th>
                    <th class="sticky-header">Отработанные часы</th>
                    <th class="sticky-header">% отработанных часов</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="employee in office.employees" v-bind:key="employee.employeeId">
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.employeeName || 'Неизвестно'}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.salary || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.penalty || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.paidsalary || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.unpaidsalary || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{(employee.goodsbonus || 0) + (employee.servicebonus || 0) || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.servicebonus || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.goodsbonus || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.paidbonus || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.unpaidbonus || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee.estimatedworkhours || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{employee._time || 0}}
                      </router-link>
                    </td>
                    <td>
                      <router-link v-bind:to="/EditEmployee/ + parseInt(employee.employeeId)" class="table-link">
                        {{((employee.meanworkload || 0) * 100).toFixed(2).toString() + '%'}}
                      </router-link>
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
  name: 'EmployeesReport',
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
      employeeIds: [],
      officeIds: [],
      isLoading: false,
      loadingError: '',
      summary: null,
      byOffices: [],
      byEmployees: [],
      byOfficesAndEmployees: []
    }
  },
  methods: {
    load: function () {
      this.isLoading = true
      this.loadingError = ''
      var data = {
        period: this.moment(this.period, 'MM YYYY').format('DD.MM.YYYY')
      }
      if (this.employeeIds && this.employeeIds.length > 0) {
        data.employeeIds = this.employeeIds
      }
      if (this.officeIds && this.officeIds.length > 0) {
        data.officeIds = this.officeIds
      }
      HTTP.post(`GenerateEmployeeReport/`, data)
        .then(response => {
          this.summary = response.data.summary[0]
          if (!response.data.byOfficeAndEmployee.warning) {
            for (var index in response.data.byOffices) {
              var office = response.data.byOffices[index]
              office.employees = response.data.byOfficeAndEmployee.filter(x => x.officeId === office.officeId)
              office.detailsShown = false
              office.uniqueEmployeesCount = new Set(office.employees.map(x => x.employeeId)).size
            }
          }
          this.byOffices = response.data.byOffices
          this.byEmployees = response.data.byEmployees
          this.byOfficesAndEmployees = response.data.byOfficeAndEmployee
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.summary = null
          this.byOffices = []
          this.byEmployees = []
          this.byOfficesAndEmployees = []
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
    }
  },
  computed: {
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
    periods () {
      var periods = []
      for (var i = 0; i <= 12; i++) {
        periods.push(this.moment().subtract(i, 'months').format('MM YYYY'))
      }
      return periods
    },
    uniqueEmployeesCount () {
      if (this.byEmployees && this.byEmployees.length && !this.byEmployees.warning && !this.byEmployees.error) {
        return new Set(this.byEmployees.map(x => x.employeeId)).size
      }
    }
  }
}
</script>

<style>
</style>
