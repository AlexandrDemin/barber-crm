<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/Employees">Сотрудники</router-link></li>
        </ul>
      </nav>
      <h1>Сотрудник</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Имя</label>
          <input type="text" v-model="employee.name" autofocus/>
          <label>Фото</label>
          <button type="button" class="button secondary">Выбрать</button>
          <input type="file" accept="image/*" style="display:none" ref="photoSelector">
          <label>Статус</label>
          <v-select
            :clearable="false"
            v-model="employee.state"
            :reduce="state => state.id"
            :value="employee.state"
            label="name"
            :options="employeeStates"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Роли</label>
          <v-select
            multiple
            v-model="employee.roles"
            :reduce="role => role.id"
            :value="employee.roles"
            label="name"
            :options="userRoles"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Категория мастера</label>
          <v-select
            :clearable="false"
            v-model="employee.categoryId"
            :reduce="category => category.id"
            :value="employee.categoryId"
            label="name"
            :options="masterCategories"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Логин</label>
          <input type="text" v-model="employee.login"/>
          <label>Пароль</label>
          <input type="password" v-model="employee.password"/>
          <div v-for="(contact, index) in employee.contacts" v-bind:key="contact">
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
          <label>Оклад</label>
          <input type="number" v-model="employee.salary"/>
          <label>% премии от услуг</label>
          <input type="number" v-model="employee.servicePercent"/>
          <label>% премии от товаров</label>
          <input type="number" v-model="employee.goodsPercent"/>
          <div>
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary" type="button" @click="save">Сохранить</button>
            <button class="button secondary" type="button" @click="saveAndAddMore">Сохранить и добавить ещё</button>
          </div>
          <div v-if="savingError" class="callout alert">
            <h5>Произошла ошибка при сохранении данных</h5>
            <p>{{savingError}}</p>
          </div>
        </div>
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
  name: 'EditEmployee',
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
      employee: this.getEmptyItem()
    }
  },
  methods: {
    addContact: function () {
      if (!this.employee.contacts) {
        this.employee.contacts = []
      }
      this.employee.contacts.push({
        type: 'phone',
        value: ''
      })
    },
    removeContact: function (index) {
      this.employee.contacts.splice(index, 1)
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetEmployee/`, {'id': id})
        .then(response => {
          this.employee = response.data
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
      HTTP.post(`EditEmployee/`, this.employee)
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
      this.employee = this.getEmptyItem()
      this.$router.push('/EditEmployee/')
    },
    getEmptyItem: function () {
      return {
        id: 'null',
        name: '',
        login: '',
        password: '',
        contacts: [],
        roles: ['master'],
        photo: null,
        salary: 0,
        servicePercent: 0.1,
        goodsPercent: 0.1,
        categoryId: 0,
        state: 'active',
        employeeRating: null,
        controlRating: null
      }
    }
  },
  computed: {
    userRoles: {
      get () {
        return this.$store.state.userRoles
      }
    },
    employeeStates: {
      get () {
        return this.$store.state.employeeStates
      }
    },
    contactTypes: {
      get () {
        return this.$store.state.contactTypes
      }
    },
    masterCategories: {
      get () {
        return this.$store.state.masterCategories
      }
    }
  }
}
</script>

<style>
</style>
