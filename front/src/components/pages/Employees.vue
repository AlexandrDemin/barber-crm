<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Сотрудники <router-link to="/EditEmployee/" class="button no-margion">Добавить</router-link></h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Сотрудник</th>
              <th>Роли</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in employees" v-bind:key="item.id">
              <td>
                <router-link v-bind:to="'/EditEmployee/' + item.id" class="table-link">
                  <img v-if="item.photo" v-bind:src="'url(' + item.photo + ')'">
                  <div v-if="!item.photo">{{$store.getters.getUserPicturePlaceholderText(item.name)}}</div>
                  {{item.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditEmployee/' + item.id" class="table-link">
                  <div v-for="role in item.roles" v-bind:key="role">
                      {{$store.getters.getUserRoleName(role)}}
                  </div>
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
  name: 'Employees',
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
      HTTP.post(`GetEmployees/`, {})
        .then(response => {
          this.employees = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    employees: {
      get () {
        return this.$store.state.employees
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'employees',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
