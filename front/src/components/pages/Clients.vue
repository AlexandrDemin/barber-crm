<template>
  <main>
    <appMenu selected-element="clients"></appMenu>
    <div class="content">
      <h1>Клиенты</h1>
      <div class="input-group">
        <input class="input-group-field" v-model="q" v-on:keyup.enter.stop="loadClients" autofocus type="text" placeholder="Имя или контакт клиента"/>
        <div class="input-group-button">
          <button type="button" class="button primary" @click="loadClients">Найти</button>
        </div>
      </div>
      <div class="position-relative">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <table class="hover">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Контакты</th>
              <th>Количество операций</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="client in clients" v-bind:key="client.id">
              <td>
                <router-link v-bind:to="'/EditClient/' + client.id" class="table-link">
                  {{client.name}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditClient/' + client.id" class="table-link">
                  <div v-for="(contact, index) in client.contacts" v-bind:key="index">
                    {{$store.getters.getContactTypeName(contact.type)}}: {{contact.value}}
                  </div>
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="'/EditClient/' + client.id" class="table-link">
                  {{client.operationsCount}}
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
  name: 'Clients',
  components: {
    appMenu: Menu,
    VueElementLoading
  },
  mounted: function () {
    document.title = this.$route.meta.title
    this.clients = this.storeClients
  },
  data () {
    return {
      q: '',
      clients: [],
      isLoading: false,
      error: ''
    }
  },
  methods: {
    loadClients: function () {
      this.isLoading = true
      HTTP.post(`GetClients/`, {q: this.q})
        .then(response => {
          this.clients = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.error = e
          this.isLoading = false
        })
    }
  },
  computed: {
    storeClients: function () {
      return this.$store.state.clients
    }
  },
  watch: {
    storeClients () {
      if (this.q === '') {
        this.clients = this.storeClients
      }
    }
  }
}
</script>

<style>
</style>
