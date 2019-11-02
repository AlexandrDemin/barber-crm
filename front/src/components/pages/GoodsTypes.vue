<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Товары <router-link to="/EditGoodsType/" class="button no-margion">Добавить</router-link></h1>
      <div>
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="table-container">
          <table class="hover">
            <thead>
              <tr>
                <th class="sticky-header">Название</th>
                <th class="sticky-header">Цена</th>
                <th class="sticky-header">Статус</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in goodsTypes" v-bind:key="item.id">
                <td>
                  <router-link v-bind:to="'/EditGoodsType/' + item.id" class="table-link">
                    {{item.name}}
                  </router-link>
                </td>
                <td>
                  <router-link v-bind:to="'/EditGoodsType/' + item.id" class="table-link">
                    {{item.price}}
                  </router-link>
                </td>
                <td>
                  <router-link v-bind:to="'/EditGoodsType/' + item.id" class="table-link">
                    {{$store.getters.getGoodsStateName(item.state)}}
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import { HTTP } from '../../api/api.js'
import VueElementLoading from 'vue-element-loading'

export default {
  name: 'GoodsTypes',
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
      HTTP.post(`GetGoods/`, {})
        .then(response => {
          this.goodsTypes = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    goodsTypes: {
      get () {
        return this.$store.state.goodsTypes
      },
      set (value) {
        this.$store.commit('updateStore', {
          name: 'goodsTypes',
          value: value
        })
      }
    }
  }
}
</script>

<style>
</style>
