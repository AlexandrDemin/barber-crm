<template>
  <div class="cell large-6 columns card employee-card">
    <div class="employee-card-header grid-x">
      <div class="cell small-2 medium-1">
        <img v-if="employee.pictureUrl" class="employee-card-picture" v-bind:src="employee.pictureUrl"/>
        <div v-if="!employee.pictureUrl" class="employee-card-picture employee-card-picture-placeholder">
          {{getPicturePlaceholderText()}}
        </div>
      </div>
      <div class="cell auto">
        <h4>{{employee.name}}</h4>
      </div>
      <div class="cell auto show-for-medium">
        <p>Длина смены <strong>{{employee.workHours}}</strong> ч.</p>
      </div>
    </div>
    <div v-if="employee.role === 'master'" class="employee-card-content grid-x grid-padding-x grid-padding-y">
      <div class="cell small-6">
        <input type="text" v-model="servicesSearch" placeholder="Поиск по услугам"/>
        <ul class="services-goods-list">
          <li v-for="service in filteredServices" v-bind:key="service.id">{{service.name}}</li>
        </ul>
      </div>
      <div class="cell small-6">
        <input type="text" v-model="goodsSearch" placeholder="Поиск по товарам"/>
        <ul class="services-goods-list">
          <li v-for="good in filteredGoods" v-bind:key="good.id">{{good.name}}</li>
        </ul>
      </div>
    </div>
    <div v-if="employee.role === 'officeAdmin'" class="employee-card-content grid-x grid-padding-x grid-padding-y">
      <div class="cell small-6">
        <input type="text" v-model="servicesSearch" placeholder="Поиск по услугам"/>
        <ul class="services-goods-list">
          <li v-for="service in filteredServices" v-bind:key="service.id">{{service.name}}</li>
        </ul>
      </div>
      <div class="cell small-6">
        <input type="text" v-model="goodsSearch" placeholder="Поиск по товарам"/>
        <ul class="services-goods-list">
          <li v-for="good in filteredGoods" v-bind:key="good.id">{{good.name}}</li>
        </ul>
      </div>
    </div>
    <div class="employee-card-footer grid-x grid-padding-x grid-padding-y">
      <div class="cell medium-6">
        <select v-model="selectedEmployeePayment">
          <option v-for="payment in employeePaymentTypes" v-bind:key="payment.id" v-bind:value="payment.id" v-bind:selected="payment.id === selectedEmployeePayment">
            {{payment.name}}
          </option>
        </select>
      </div>
      <div class="cell auto">
        <input v-model="paymentSum" type="number" placeholder="Сумма"/>
      </div>
      <div class="cell shrink">
        <button class="button secondary">Сохранить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmployeeCard',
  props: ['employee'],
  data () {
    return {
      selectedEmployeePayment: 1,
      paymentSum: '',
      servicesSearch: '',
      goodsSearch: ''
    }
  },
  methods: {
    getPicturePlaceholderText: function () {
      var name = this.employee.name
      var initials = ''
      name.split(' ').map(n => {
        initials += n[0].toUpperCase()
      })
      return initials
    }
  },
  computed: {
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
      return this.services.filter(service => service.name.toLowerCase().includes(this.servicesSearch.toLowerCase()))
    },
    filteredGoods: function () {
      return this.goods.filter(good => good.name.toLowerCase().includes(this.goodsSearch.toLowerCase()))
    }
  }
}
</script>

<style>
</style>
