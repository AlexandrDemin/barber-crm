<template>
  <div class="cell large-6 columns card employee-card">
    <div class="employee-card-header grid-x grid-padding-x align-middle">
      <!-- <div class="cell small-2 medium-1">
        <img v-if="employee.pictureUrl" class="employee-card-picture" v-bind:src="employee.pictureUrl"/>
        <div v-if="!employee.pictureUrl" class="employee-card-picture employee-card-picture-placeholder">
          {{$store.getters.getUserPicturePlaceholderText(employeeName)}}
        </div>
      </div> -->
      <div class="cell auto">
        <h5>{{employee.name}}</h5>
      </div>
      <div class="cell auto show-for-medium">
        Длина смены <strong>{{employee.workHours}}</strong> ч.
      </div>
    </div>
    <div class="employee-card-content grid-x grid-padding-x grid-padding-y">
      <div class="cell small-6" v-if="employee.role === 'master'">
        <input type="text" v-model="servicesSearch" placeholder="Поиск по услугам"/>
        <ul class="services-goods-list">
          <li v-for="service in filteredServices" v-bind:key="service.id">
            <router-link :to="{path:'/EditService/', query: {serviceTypeId: service.id, masterId: employee.id, adminId: adminId}}">{{service.name}}</router-link>
          </li>
        </ul>
      </div>
      <div class="cell small-6">
        <input type="text" v-model="goodsSearch" placeholder="Поиск по товарам"/>
        <ul class="services-goods-list">
          <li v-for="good in filteredGoods" v-bind:key="good.id">
            <router-link :to="{path:'/EditGoodsSell/', query: {goodTypeId: good.id, employeeId: employee.id === adminId ? null : employee.id, adminId: adminId}}">{{good.name}}</router-link>
          </li>
        </ul>
      </div>
    </div>
    <div class="employee-card-footer grid-x grid-padding-x grid-padding-y">
      <vue-element-loading :active="isSaving" color="#1C457D"/>
      <label class="cell small-12 no-padding-top-bottom">Выплата сотруднику</label>
      <div class="cell medium-6">
        <v-select
          @input="updateSum"
          :clearable="false"
          v-model="selectedEmployeePayment"
          :reduce="s => s.id"
          :value="selectedEmployeePayment"
          label="name"
          :options="employeePaymentTypes"
        >
          <div slot="no-options">Ничего не найдено</div>
        </v-select>
      </div>
      <div class="cell auto">
        <input v-model="paymentSum" type="number" placeholder="Сумма"/>
      </div>
      <div class="cell shrink">
        <button class="button secondary" @click="save">Сохранить</button>
      </div>
      <div class="cell small-12 callout alert" v-if="savingError">
        <h5>Произошла ошибка при сохранении данных</h5>
        <p>{{savingError}}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { HTTP } from '../api/api.js'
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'EmployeeCard',
  components: {
    VueElementLoading,
    'v-select': vSelect
  },
  props: ['employee'],
  created: function () {
    this.selectedEmployeePayment = this.employeePaymentTypes[0].id
    this.paymentSum = this.employeePaymentTypes[0].defaultSum
  },
  data () {
    return {
      selectedEmployeePayment: null,
      paymentSum: 0,
      servicesSearch: '',
      goodsSearch: '',
      isSaving: false,
      savingError: ''
    }
  },
  methods: {
    updateSum: function () {
      this.paymentSum = this.employeePaymentTypes.filter(x => x.id === this.selectedEmployeePayment)[0].defaultSum
    },
    save: function () {
      this.isSaving = true
      this.savingError = ''
      var operation = {
        'type': 'employeepayment',
        'id': null,
        'employeePaymentTypeId': this.selectedEmployeePayment,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': this.moment().utc(),
        'employeeId': this.employee.id,
        'sum': this.paymentSum,
        'comment': ''
      }
      HTTP.post(`EditOperations/`, [operation])
        .then(response => {
          this.$store.dispatch('getCurrentSession')
          this.isSaving = false
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    }
  },
  computed: {
    currentSession: {
      get () {
        return this.$store.state.currentSession
      }
    },
    services: {
      get () {
        return this.$store.state.serviceTypes
      }
    },
    goods: {
      get () {
        return this.$store.state.goodsTypes
      }
    },
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      }
    },
    filteredServices: function () {
      return this.services.filter(service => service.name.toLowerCase().includes(this.servicesSearch.toLowerCase()) && service.state === 'active')
    },
    filteredGoods: function () {
      return this.goods.filter(good => good.name.toLowerCase().includes(this.goodsSearch.toLowerCase()) && good.state === 'active')
    },
    adminId: function () {
      return this.$store.state.currentSession.employees.filter(e => e.role === 'officeAdmin')[0].id
    }
  }
}
</script>

<style>
</style>
