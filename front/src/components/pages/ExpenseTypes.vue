<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Типы расходов</h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Название</th>
              <th>Сумма по умолчанию</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in spendTypes" v-bind:key="item.id">
              <td>
                <router-link v-bind:to="'/EditExpenseType/' + item.id" class="table-link">
                  {{item.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditExpenseType/' + item.id" class="table-link">
                  {{item.defaultSum}}
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
  name: 'ExpenseTypes',
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
      HTTP.post(`GetSpendTypes/`, {})
        .then(response => {
          this.offices = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'spendTypes',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
