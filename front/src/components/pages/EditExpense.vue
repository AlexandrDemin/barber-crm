<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content">
      <h1>Расход</h1>
      <div class="grid-x">
        <form class="cell large-6">
          <div v-for="(expense, index) in operations" v-bind:key="expense.id">
            <label v-on:click.prevent class="grid-x">
              <span class="cell auto">Расход {{index > 0 ? index + 1 : ''}}</span>
              <button
                type="button" class="button clear small cell shrink no-margin"
                @click="removeExpense(expense)"
                v-if="session.state === 'open' && index > 0"
              >
                Удалить
              </button>
            </label>
            <select v-model="expense.type">
              <option
                v-for="item in spendTypes"
                v-bind:key="item.id"
                v-bind:value="item.id"
                v-bind:selected="item.id === expense.type"
              >
                {{item.name}}
              </option>
            </select>
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
          <div v-if="session.state === 'open'" class="grid-x align-justify">
            <button class="button primary cell shrink" type="button" @click="save">Сохранить</button>
            <button class="button alert cell shrink" type="button" @click="deleteOperation">Удалить</button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditExpense',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.session = {
        'state': 'open'
      }
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
      session: {
        'state': this.$route.query.sessionState || 'open'
      },
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