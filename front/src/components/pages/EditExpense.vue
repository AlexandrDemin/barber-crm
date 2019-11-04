<template>
  <main>
    <appMenu :selected-element="canEdit ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="canEdit"><router-link to="/Session">Смена</router-link></li>
          <li v-else><router-link to="/SessionsHistory">История смен и операций</router-link></li>
        </ul>
      </nav>
      <h1>Расход</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div v-if="loadingError" class="callout alert">
          <h5>Произошла ошибка при загрузке данных</h5>
          <p>{{loadingError}}</p>
        </div>
        <div class="cell large-6">
          <label>Время</label>
          <input type="time" v-model="time"/>
          <div v-for="(expense, index) in operations" v-bind:key="expense.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Расход {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeExpense(expense)"
                v-if="canEdit && index > 0"
              >
                Удалить
              </button>
            </label>
            <v-select
              @input="updateSpendSum(expense)"
              :clearable="false"
              v-model="expense.expenseTypeId"
              :reduce="s => s.id"
              :value="expense.expenseTypeId"
              label="name"
              :options="spendTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Сумма</label>
            <input type="number" v-model.number="expense.sum">
            <label>Комментарий</label>
            <textarea rows="2" v-model="expense.comment"></textarea>
          </div>
          <div v-if="canEdit">
            <button class="button secondary" type="button" @click="addExpense">Добавить расход</button>
          </div>
          <div v-if="canEdit">
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary" type="button" @click="save">Сохранить</button>
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
  name: 'EditExpense',
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
      this.operations = [this.getEmptyItem()]
    }
  },
  data () {
    return {
      isLoading: false,
      loadingError: false,
      isSaving: false,
      savingError: '',
      operations: [],
      time: this.moment().format('HH:mm')
    }
  },
  methods: {
    getEmptyItem: function () {
      return {
        'type': 'spendoperation',
        'id': null,
        'expenseTypeId': this.spendTypes[0].id,
        'sessionId': this.currentSession.id,
        'officeId': this.currentSession.officeId,
        'datetime': this.moment(),
        'sum': this.getSpendSum(this.spendTypes[0].id),
        'comment': ''
      }
    },
    updateSpendSum: function (operation) {
      operation.sum = this.getSpendSum(operation.expenseTypeId)
    },
    getSpendSum: function (spendId) {
      return parseInt(this.spendTypes.filter(x => x.id === spendId)[0].defaultSum)
    },
    addExpense: function () {
      this.operations.push(this.getEmptyItem())
    },
    removeExpense: function (item) {
      var index = this.operations.findIndex(o => o.type === 'spendoperation' && o.type === item.type && o.id === item.id)
      this.operations.splice(index, 1)
    },
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetSpendOperation/`, {'id': id})
        .then(response => {
          var operation = response.data
          operation.type = 'spendoperation'
          operation.datetime = this.moment.utc(operation.datetime, 'DD.MM.YYYY HH:mm').local()
          this.operations = [operation]
          this.time = operation.datetime.format('HH:mm')
          this.isLoading = false
        })
        .catch(e => {
          this.loadingError = e
          this.isLoading = false
        })
    },
    save: function () {
      this.savingError = ''
      this.isSaving = true
      var operations = this.operations
      for (var index in operations) {
        operations[index].datetime = this.moment(this.time, 'HH:mm').utc()
      }
      this.operations = operations
      HTTP.post(`EditOperations/`, this.operations)
        .then(response => {
          this.$store.dispatch('getCurrentSession')
          this.isSaving = false
          this.$router.push('/')
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    }
  },
  computed: {
    currentSession: {
      get () {
        return this.$store.state.currentSession
      }
    },
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    },
    canEdit: function () {
      if (this.operations[0]) {
        return !this.operations[0].id || (this.operations[0].sessionId === this.currentSession.id)
      }
      return false
    }
  }
}
</script>

<style>
</style>
