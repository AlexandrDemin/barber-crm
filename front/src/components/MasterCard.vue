<template>
  <div class="cell large-6 columns translucent-theme-block master-card">
    <div class="master-card-header grid-x">
      <div class="cell small-2 medium-1">
        <img class="master-card-picture" v-bind:src="master.pictureUrl"/>
      </div>
      <div class="cell small-10 medium-5">
        <h4>{{master.name}}</h4>
      </div>
      <div class="cell small-12 medium-6">
        <p>Длина смены <strong>{{master.workHours}}</strong> ч.</p>
      </div>
    </div>
    <div class="master-card-content grid-x grid-padding-x grid-padding-y">
      <div class="cell medium-6">
        <input type="text" v-model="servicesSearch" placeholder="Поиск по услугам"/>
        <ul class="services-goods-list">
          <li v-for="service in filteredServices" v-bind:key="service.id">{{service.name}}</li>
        </ul>
      </div>
      <div class="cell medium-6">
        <input type="text" v-model="goodsSearch" placeholder="Поиск по товарам"/>
        <ul class="services-goods-list">
          <li v-for="good in filteredGoods" v-bind:key="good.id">{{good.name}}</li>
        </ul>
      </div>
    </div>
    <div class="master-card-footer grid-x grid-padding-x grid-padding-y">
      <div class="cell medium-6">
        <select v-model="selectedEmployeePayment">
          <option v-for="payment in employeePaymentTypes" v-bind:key="payment.id" v-bind:value="payment.value" v-bind:selected="payment.id === selectedEmployeePayment">
            {{payment.name}}
          </option>
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
</template>

<script>
export default {
  name: 'MasterCard',
  props: ['master'],
  data () {
    return {
      selectedEmployeePayment: 1,
      servicesSearch: '',
      goodsSearch: ''
    }
  },
  computed: {
    services: {
      get () {
        return this.$store.state.services
      }
    },
    goods: {
      get () {
        return this.$store.state.goods
      }
    },
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      }
    },
    filteredServices: function () {
      return this.services.filter(service => service.name.toLowerCase().includes(this.servicesSearch))
    },
    filteredGoods: function () {
      return this.goods.filter(good => good.name.toLowerCase().includes(this.goodsSearch))
    }
  }
}
</script>

<style>
  .master-card-header {
    background: #FFFFFF;
    border-radius: 5px 5px 0 0;
  }
  .master-card-header .master-card-picture {
    border-radius: 5px 0 0 0;
  }
  .master-card-footer .cell select,
  .master-card-footer .cell input,
  .master-card-footer .cell button {
    margin: 0;
  }
  .services-goods-list {
    list-style: none;
    margin: 0;
    padding: 0;
    height: 200px;
    overflow: auto;
  }
  .services-goods-list li {
    border-bottom: 1px solid #E3E1DD;
    padding: 5px 0;
  }
  .services-goods-list li:last-child {
    border-bottom: none;
  }
</style>
