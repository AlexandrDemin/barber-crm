<template>
  <main>
    <appMenu selected-element="reports"></appMenu>
    <div class="content">
      <h1>Финансовый отчёт</h1>
      <div class="grid-x grid-padding-x no-padding-small">
        <div class="cell large-6 small-12">
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
        <div class="cell large-6 small-12">
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
        <div v-if="!loadingError && !isLoading && summary && (!summary.operationcount || (byOffices.length && byOffices.warning))">Нет данных по выбранным фильтрам</div>
        <div v-if="!loadingError && !isLoading && summary && summary.operationcount">
          <h2>Итого</h2>
          <div class="grid-x grid-margin-x grid-margin-y margin-bottom-10px">
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalincome.toFixed(2) || 0}}</div>
              <label>Выручка, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.serviceincome || 0}}</div>
              <label>Выручка (услуги), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.goodsincome || 0}}</div>
              <label>Выручка (товары), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalcash || 0}}</div>
              <label>Выручка (наличка), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalcashless || 0}}</div>
              <label>Выручка (безнал), ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalspend.toFixed(2) || 0}}</div>
              <label>Расходы, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.totalprofit.toFixed(2) || 0}}</div>
              <label>Прибыль, ₽</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.operationcount || 0}}</div>
              <label>{{inclineWord(summary.operationcount, 'Операция', 'Операции', 'Операций')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.serviceoperationcount || 0}}</div>
              <label>{{inclineWord(summary.operationcount, 'Услуга оказана', 'Услуги оказано', 'Услуг оказано')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.goodsoperationcount || 0}}</div>
              <label>{{inclineWord(summary.operationcount, 'Товар продан', 'Товара продано', 'Товаров продано')}}</label>
            </div>
            <div class="cell small-6 medium-4 large-2">
              <div class="big-number">{{summary.spendoperationcount || 0}}</div>
              <label>{{inclineWord(summary.operationcount, 'Расход внесен', 'Расхода внесено', 'Расходов внесено')}}</label>
            </div>
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
                <div class="big-number">{{office.totalincome.toFixed(2) || 0}}</div>
                <label>Выручка, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.serviceincome || 0}}</div>
                <label>Выручка (услуги), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.goodsincome || 0}}</div>
                <label>Выручка (товары), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalcash || 0}}</div>
                <label>Выручка (наличка), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalcashless || 0}}</div>
                <label>Выручка (безнал), ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalspend.toFixed(0) || 0}}</div>
                <label>Расходы, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.totalprofit.toFixed(2) || 0}}</div>
                <label>Прибыль, ₽</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.operationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Операция', 'Операции', 'Операций')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.serviceoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Услуга оказана', 'Услуги оказано', 'Услуг оказано')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.goodsoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Товар продан', 'Товара продано', 'Товаров продано')}}</label>
              </div>
              <div class="cell small-6 medium-4 large-2">
                <div class="big-number">{{office.spendoperationcount || 0}}</div>
                <label>{{inclineWord(office.operationcount, 'Расход внесен', 'Расхода внесено', 'Расходов внесено')}}</label>
              </div>
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
  name: 'FinancialReport',
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
      officeIds: [],
      isLoading: false,
      loadingError: '',
      summary: null,
      byOffices: []
    }
  },
  methods: {
    load: function () {
      this.isLoading = true
      this.loadingError = ''
      var data = {
        period: this.moment(this.period, 'MM YYYY').format('DD.MM.YYYY')
      }
      if (this.officeIds && this.officeIds.length > 0) {
        data.officeIds = this.officeIds
      }
      HTTP.post(`GenerateFinanceReport/`, data)
        .then(response => {
          this.summary = response.data.summary[0]
          this.byOffices = response.data.byOffices
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.summary = null
          this.byOffices = []
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
    }
  },
  computed: {
    offices: {
      get () {
        return this.$store.state.offices
      }
    },
    periods () {
      var periods = []
      for (var i = 0; i <= 12; i++) {
        periods.push(this.moment().subtract(i, 'months').format('MM YYYY'))
      }
      return periods
    }
  }
}
</script>

<style>
</style>
