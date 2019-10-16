<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/ExpenseTypes">Типы расходов</router-link></li>
        </ul>
      </nav>
      <h1>Тип расхода</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Название</label>
          <input type="text" v-model="spendType.name" autofocus/>
          <label>Сумма по умолчанию</label>
          <input type="number" v-model="spendType.defaultSum" autofocus/>
          <label>Статус</label>
          <select v-model="spendType.state">
            <option
              v-for="item in spendTypeStates"
              v-bind:key="item.id"
              v-bind:value="item.id"
              v-bind:selected="item.id === spendType.state"
            >
              {{item.name}}
            </option>
          </select>
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

export default {
  name: 'EditExpenseType',
  components: {
    appMenu: Menu,
    VueElementLoading
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
      spendType: this.getEmptyItem()
    }
  },
  methods: {
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetSpendType/`, {'id': id})
        .then(response => {
          this.spendType = response.data
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
      HTTP.post(`EditSpendType/`, this.spendType)
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
      this.spendType = this.getEmptyItem()
      this.$router.push('/EditSpendType')
    },
    getEmptyItem: function () {
      return {
        id: 'null',
        name: '',
        defaultSum: '',
        state: 'active'
      }
    }
  },
  computed: {
    spendTypeStates: {
      get () {
        return this.$store.state.spendTypeStates
      }
    }
  }
}
</script>

<style>
</style>
