<template>
  <main>
    <appMenu :selected-element="operations[0].sessionId === $store.state.currentSession.id ? 'session' : 'history'"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li v-if="operations[0].sessionId === $store.state.currentSession.id"><router-link to="/Session">Смена</router-link></li>
          <li v-else><router-link to="/SessionsHistory">История смен и операций</router-link></li>
        </ul>
      </nav>
      <h1>Расход</h1>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <div v-for="(expense, index) in operations" v-bind:key="expense.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Расход {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeExpense(expense)"
                v-if="operations[0].sessionId === $store.state.currentSession.id && index > 0"
              >
                Удалить
              </button>
            </label>
            <v-select
              :clearable="false"
              v-model="expense.type"
              :reduce="s => s.id"
              :value="expense.type"
              label="name"
              :options="spendTypes"
            >
              <div slot="no-options">Ничего не найдено</div>
            </v-select>
            <label>Время</label>
            <input type="text" v-model="expense.datetime"/>
            <label>Сумма</label>
            <input type="number" v-model="expense.sum">
            <label>Комментарий</label>
            <textarea rows="2" v-model="expense.comment"></textarea>
          </div>
          <div>
            <button class="button secondary" type="button" @click="addExpense">Добавить расход</button>
          </div>
          <div v-if="operations[0].sessionId === $store.state.currentSession.id">
            <vue-element-loading :active="isSaving" color="#1C457D"/>
            <button class="button primary cell shrink" type="button" @click="save">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'
import VueElementLoading from 'vue-element-loading'
import vSelect from 'vue-select'

export default {
  name: 'EditExpense',
  components: {
    appMenu: Menu,
    VueElementLoading,
    'v-select': vSelect
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.operations = [
        {
          'operationType': 'spend',
          'id': 7,
          'officeId': 1,
          'sessionId': 1,
          'type': 2,
          'datetime': '21.09.2019 12:44',
          'sum': 600,
          'comment': ''
        }
      ]
    }
  },
  data () {
    return {
      isLoading: false,
      isSaving: false,
      operations: [
        {
          'operationType': 'spend',
          'id': null,
          'type': 1,
          'sessionId': this.$route.query.sessionId,
          'officeId': this.$route.query.officeId,
          'datetime': this.$store.getters.getDateTimeNow,
          'sum': 500,
          'comment': ''
        }
      ]
    }
  },
  methods: {
    addExpense: function () {
      this.operations.push({
        'operationType': 'spend',
        'id': null,
        'type': 1,
        'sessionId': this.$route.query.sessionId,
        'officeId': this.$route.query.officeId,
        'datetime': this.$store.getters.getDateTimeNow,
        'sum': 500,
        'comment': ''
      })
    },
    removeExpense: function (item) {
      var index = this.operations.findIndex(o => o.operationType === 'spend' && o.type === item.type && o.id === item.id)
      this.operations.splice(index, 1)
    },
    save: function () {},
    deleteOperation: function () {}
  },
  computed: {
    spendTypes: {
      get () {
        return this.$store.state.spendTypes
      }
    }
  }
}
</script>

<style>
</style>
