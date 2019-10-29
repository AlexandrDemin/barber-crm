<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Услуги <router-link to="/EditServiceType/" class="button no-margion">Добавить</router-link></h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Название</th>
              <th>Цены</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in serviceTypes" v-bind:key="item.id">
              <td>
                <router-link v-bind:to="'/EditServiceType/' + item.id" class="table-link">
                  {{item.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditServiceType/' + item.id" class="table-link">
                  <div v-for="price in item.prices" v-bind:key="price">
                    <span v-if="price.category">
                      {{$store.getters.getMasterCategoryName(price.category)}}: {{price.price}}&nbsp;₽
                    </span>
                    <span v-if="!price.category && price.category !== 0">
                      Все категории мастеров: {{price.price}}&nbsp;₽
                    </span>
                  </div>
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditServiceType/' + item.id" class="table-link">
                  {{$store.getters.getServiceStateName(item.state)}}
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
  name: 'ServiceTypes',
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
      HTTP.post(`GetServicesPrices/`, {})
        .then(response => {
          this.serviceTypes = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    serviceTypes: {
      get () {
        return this.$store.state.serviceTypes
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'serviceTypes',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
