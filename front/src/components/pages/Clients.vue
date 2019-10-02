<template>
  <main>
    <appMenu selected-element="clients"></appMenu>
    <div class="content">
      <h1>Клиенты</h1>
      <form class="input-group">
        <input class="input-group-field" v-model="q" v-on:keyup.enter="loadClients" autofocus type="text" placeholder="Имя или контакт клиента"/>
        <div class="input-group-button">
          <button type="button" class="button primary" @click="loadClients">Найти</button>
        </div>
      </form>
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
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'Clients',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
  },
  data () {
    return {
      q: '',
      clients: this.$store.state.clients
    }
  },
  methods: {
    loadClients: function () {}
  },
  computed: {}
}
</script>

<style>
</style>
