<template>
  <main>
    <appMenu :selected-element="session.id === $store.state.currentSession.id ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="session.id === $store.state.currentSession.id"><router-link to="/">Назад</router-link></li>
          <li v-else><router-link to="/SessionsHistory/">Назад</router-link></li>
        </ul>
      </nav>
      <h1>Смена</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Отделение</label>
          <v-select
            :clearable="false"
            :disabled="!canEdit()"
            v-model="session.officeId"
            :reduce="s => s.id"
            :value="session.officeId"
            label="name"
            :options="offices"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <h2>Администраторы</h2>
          <div v-for="(admin, index) in selectedAdmins" v-bind:key="admin.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Администратор {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeEmployee(admin.id)"
                v-if="index > 0 && canEdit()"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              :disabled="!canEdit()"
              v-model="admin.id"
              :reduce="s => s.id"
              :value="admin.id"
              label="name"
              :options="admins"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Продолжительность смены, часы</label>
            <input type="number" :disabled="!canEdit()" v-model="admin.workHours">
          </div>
          <div v-if="canEdit()">
            <button class="button secondary" type="button" @click="addAdmin">Добавить администратора</button>
          </div>
          <h2>Мастера</h2>
          <div v-for="(master, index) in selectedMasters" v-bind:key="master.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Мастер {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeEmployee(master.id)"
                v-if="index > 0 && canEdit()"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              :disabled="!canEdit()"
              v-model="master.id"
              :reduce="s => s.id"
              :value="master.id"
              label="name"
              :options="masters"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Продолжительность смены, часы</label>
            <input type="number" :disabled="!canEdit()" v-model="master.workHours">
          </div>
          <div v-if="canEdit()">
            <button class="button secondary" type="button" @click="addMaster">Добавить мастера</button>
          </div>
          <div v-if="canEdit()" class="grid-x align-justify">
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary cell shrink" type="button" @click="save(false)">{{session.id ? 'Сохранить' : 'Открыть смену'}}</button>
            <button v-if="session.id && session.state === 'open'" class="button secondary alert cell shrink" type="button" @click="save(true)">Закрыть смену</button>
          </div>
          <div v-if="savingError" class="callout alert">
            <h5>Произошла ошибка при сохранении смены</h5>
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
  name: 'EditSession',
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
      session: this.getEmptyItem()
    }
  },
  methods: {
    addAdmin: function () {
      this.session.employees.push({
        'id': this.admins[0].id,
        'role': 'officeAdmin',
        'workHours': 6
      })
    },
    addMaster: function () {
      this.session.employees.push({
        'id': this.masters[0].id,
        'role': 'master',
        'workHours': 6
      })
    },
    removeEmployee: function (id) {
      var employeeIndex = this.session.employees.findIndex(e => e.id === id)
      this.session.employees.splice(employeeIndex, 1)
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetSession/`, {'id': id, withOperations: false})
        .then(response => {
          var session = response.data
          if (session.employees === null) {
            session.employees = []
          }
          if (session.dateOpened) {
            session.dateOpened = this.moment(session.dateOpened, 'DD.MM.YYYY HH:mm')
          }
          if (session.dateClosed) {
            session.dateClosed = this.moment(session.dateClosed, 'DD.MM.YYYY HH:mm')
          }
          this.session = session
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function (needClose) {
      console.log(needClose)
      this.isSaving = true
      this.savingError = ''
      var session = this.session
      if (needClose) {
        session.state = 'closed'
        session.dateClosed = this.moment()
      }
      if (session.dateClosed === null) {
        delete session.dateClosed
      }
      HTTP.post(`EditSession/`, this.session)
        .then(response => {
          this.isSaving = false
          this.$store.dispatch('getCurrentSession')
          this.$router.push({ path: '/' })
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    getEmptyItem: function () {
      return {
        'id': null,
        'dateOpened': this.moment(),
        'dateClosed': null,
        'employees': [],
        'officeId': this.$store.state.currentOfficeId,
        'state': 'open',
        'openCash': 0
      }
    },
    canEdit: function () {
      return this.session.state === 'open' && (this.session.id === this.$store.state.currentSession.id || !this.session.id)
    }
  },
  computed: {
    offices: {
      get () {
        return this.$store.state.offices
      }
    },
    admins: {
      get () {
        return this.$store.state.employees.filter(e => e.roles.includes('officeAdmin'))
      }
    },
    masters: {
      get () {
        return this.$store.state.employees.filter(e => e.roles.includes('master'))
      }
    },
    selectedAdmins: {
      get () {
        if (this.session.employees) {
          return this.session.employees.filter(e => e.role === 'officeAdmin')
        }
        return null
      },
      set (item) {
        var employeeIndex = this.session.employees.findIndex(e => e.id === item.id)
        item.role = 'officeAdmin'
        this.session.employees.$set(employeeIndex, item)
      }
    },
    selectedMasters: {
      get () {
        if (this.session.employees) {
          return this.session.employees.filter(e => e.role === 'master')
        }
        return null
      },
      set (item) {
        var employeeIndex = this.session.employees.findIndex(e => e.id === item.id)
        item.role = 'master'
        this.session.employees.$set(employeeIndex, item)
      }
    }
  }
}
</script>

<style>
</style>
