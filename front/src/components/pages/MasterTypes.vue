<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Категории мастеров</h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Категория</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in masterCategories" v-bind:key="item.id">
              <td>
                <router-link v-bind:to="'/EditMasterType/' + item.id" class="table-link">
                  {{item.name}}
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
  name: 'MasterTypes',
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
      HTTP.post(`GetBarberCategories/`, {})
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
    masterCategories: {
      get () {
        return this.$store.state.masterCategories
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'masterCategories',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
