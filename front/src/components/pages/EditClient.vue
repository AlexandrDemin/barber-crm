<template>
  <main>
    <appMenu selected-element="clients"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/Clients">Клиенты</router-link></li>
        </ul>
      </nav>
      <h1>Клиент</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Имя</label>
          <input type="text" v-model="client.name" autofocus/>
          <!-- <label>Фото</label>
          <button type="button" class="button secondary">Выбрать</button>
          <input type="file" accept="image/*" style="display:none" ref="photoSelector"> -->
          <div v-for="(contact, index) in client.contacts" v-bind:key="contact">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Контакт {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeContact(index)"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              v-model="contact.type"
              :reduce="s => s.id"
              :value="contact.type"
              label="name"
              :options="contactTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <input type="text" v-model="contact.value"/>
          </div>
          <div>
            <button
              class="button secondary"
              type="button"
              @click="addContact"
            >
              Добавить контакт
            </button>
          </div>
          <label>Комментарий</label>
          <textarea rows="3" v-model="client.comment"></textarea>
          <div>
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary" type="button" @click="save">Сохранить</button>
            <button class="button secondary" type="button" @click="saveAndAddMore">Сохранить и добавить ещё</button>
          </div>
          <div v-if="savingError" class="callout alert">
            <h5>Произошла ошибка при сохранении клиента</h5>
            <p>{{savingError}}</p>
          </div>
        </div>
      </div>
      <div v-if="client.id > 0">
        <h2>История операций по клиенту</h2>
        <table class="operations-table hover">
          <thead>
            <tr>
              <th>Дата</th>
              <th>Мастер</th>
              <th>Услуга / товар</th>
              <th>Сумма</th>
              <th>Премия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="operation in client.operations" v-bind:key="operation.id">
              <td>
                <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                  {{$store.getters.getDateTimeFromOperation(operation)}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                  {{$store.getters.getEmployeeNameFromOperation(operation)}}
                </router-link>
              </td>
              <td>
                <router-link
                  v-bind:to="$store.getters.getOperationLink(operation)"
                  class="table-link"
                  v-html="$store.getters.getOperationContent(operation)"
                ></router-link>
              </td>
              <td>
                <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                  {{$store.getters.getOperationSum(operation)}}
                </router-link>
              </td>
              <td>
                <router-link v-bind:to="$store.getters.getOperationLink(operation)" class="table-link">
                  {{$store.getters.getOperationBonus(operation)}}
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
import vSelect from 'vue-select'

export default {
  name: 'EditClient',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    }
  },
  data () {
    return {
      isLoading: false,
      isSaving: false,
      loadingError: '',
      savingError: '',
      client: this.getEmptyItem()
    }
  },
  methods: {
    addContact: function () {
      if (!this.client.contacts) {
        this.client.contacts = []
      }
      this.client.contacts.push({
        type: 'phone',
        value: ''
      })
    },
    removeContact: function (index) {
      this.client.contacts.splice(index, 1)
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetClient/`, {'id': id})
        .then(response => {
          this.client = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function () {
      this.isSaving = true
      this.savingError = ''
      var client = this.client
      if (client.photo === null) {
        delete client.photo
      }
      if (client.comment === null) {
        client.comment = ''
      }
      if (client.contacts === null || client.contacts === []) {
        delete client.contacts
      }
      delete client.operations
      HTTP.post(`EditClient/`, client)
        .then(response => {
          this.isSaving = false
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    saveAndAddMore: function () {
      this.save()
      this.client = this.getEmptyItem()
      this.$router.push('/EditClient')
    },
    getEmptyItem: function () {
      return {
        id: null,
        name: '',
        photo: null,
        contacts: [
          {
            type: 'phone',
            value: ''
          }
        ],
        comment: ''
      }
    }
  },
  computed: {
    contactTypes: {
      get () {
        return this.$store.state.contactTypes
      }
    }
  }
}
</script>

<style>
</style>
