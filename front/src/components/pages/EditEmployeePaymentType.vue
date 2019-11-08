<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/EmployeePaymentTypes">Типы выплат сотрудникам</router-link></li>
        </ul>
      </nav>
      <h1>Тип выплаты сотрудникам</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Название</label>
          <input type="text" v-model="employeePaymentType.name" autofocus/>
          <label>Сумма по умолчанию</label>
          <input type="number" v-model="employeePaymentType.defaultSum" autofocus/>
          <label>Тип</label>
          <v-select
            :clearable="false"
            v-model="employeePaymentType.type"
            :reduce="s => s.id"
            :value="employeePaymentType.type"
            label="name"
            :options="employeePaymentTypeTypes"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
          <label>Статус</label>
          <v-select
            :clearable="false"
            v-model="employeePaymentType.state"
            :reduce="s => s.id"
            :value="employeePaymentType.state"
            label="name"
            :options="employeePaymentTypeStates"
          >
            <div slot="no-options">Ничего не найдено</div>
          </v-select>
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
  name: 'EditEmployeePaymentType',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  created: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.load(this.$route.params.id)
    } else {
      this.employeePaymentType = this.getEmptyItem()
    }
  },
  data () {
    return {
      isLoading: false,
      isSaving: false,
      loadingError: '',
      savingError: '',
      employeePaymentType: {}
    }
  },
  methods: {
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetEmployeePaymentType/`, {'id': id})
        .then(response => {
          this.employeePaymentType = response.data
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function (noReturnToList) {
      this.isSaving = true
      this.savingError = ''
      HTTP.post(`EditEmployeePaymentType/`, this.employeePaymentType)
        .then(response => {
          this.isSaving = false
          if (!noReturnToList) {
            this.$router.push({name: 'EmployeePaymentTypes'})
          }
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    saveAndAddMore: function () {
      this.save(true)
      this.employeePaymentType = this.getEmptyItem()
      this.$router.push('/EditEmployeePaymentType')
    },
    getEmptyItem: function () {
      return {
        id: null,
        name: '',
        defaultSum: 0,
        type: this.employeePaymentTypeTypes[0].id,
        state: 'active'
      }
    }
  },
  computed: {
    employeePaymentTypeStates: {
      get () {
        return this.$store.state.employeePaymentTypeStates
      }
    },
    employeePaymentTypeTypes: {
      get () {
        return this.$store.state.employeePaymentTypeTypes
      }
    }
  }
}
</script>

<style>
</style>
