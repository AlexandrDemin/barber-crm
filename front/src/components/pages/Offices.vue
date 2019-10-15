<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Отделения</h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Название</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="office in offices" v-bind:key="office.id">
              <td>
                <router-link v-bind:to="'/EditOffice/' + office.id" class="table-link">
                  {{office.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditOffice/' + office.id" class="table-link">
                  {{$store.getters.getOfficeStateName(office.state)}}
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
  name: 'Offices',
  components: {
    appMenu: Menu,
    VueElementLoading
  },
  mounted: function () {
    document.title = this.$route.meta.title
    this.loadOffices()
  },
  data () {
    return {
      isLoading: false,
      error: ''
    }
  },
  methods: {
    loadOffices: function () {
      this.isLoading = true
      HTTP.post(`GetOffices/`, {})
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
    offices: {
      get () {
        return this.$store.state.offices
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'offices',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
