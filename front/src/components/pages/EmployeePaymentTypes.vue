<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Типы выплат сотрудникам <router-link to="/EditEmployeePaymentType/" class="button no-margion">Добавить</router-link></h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Название</th>
              <th>Сумма по умолчанию</th>
              <th>Тип</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in employeePaymentTypes" v-bind:key="item.id">
              <td>
                <router-link v-bind:to="'/EditEmployeePaymentType/' + item.id" class="table-link">
                  {{item.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditEmployeePaymentType/' + item.id" class="table-link">
                  {{item.defaultSum}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditEmployeePaymentType/' + item.id" class="table-link">
                  {{$store.getters.getEmployeePaymentTypeTypeName(item.type)}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditEmployeePaymentType/' + item.id" class="table-link">
                  {{$store.getters.getEmployeePaymentStateName(item.state)}}
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import { HTTP } from '../../api/api.js'
import VueElementLoading from 'vue-element-loading'

export default {
  name: 'EmployeePaymentTypes',
  components: {
    appMenu: Menu,
    VueElementLoading
  },
  mounted: function () {
    document.title = this.$route.meta.title
    this.loadData()
  },
  data () {
    return {
      isLoading: false,
      error: ''
    }
  },
  methods: {
    loadData: function () {
      this.isLoading = true
      HTTP.post(`GetEmployeePaymentTypes/`, {})
        .then(response => {
          this.employeePaymentTypes = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    employeePaymentTypes: {
      get () {
        return this.$store.state.employeePaymentTypes
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'employeePaymentTypes',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
