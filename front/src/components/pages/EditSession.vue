<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">Смена</h1>
      <form class="cell large-6">
        <label>Отделение</label>
        <select v-model="session.officeId">
          <option
            v-for="office in offices"
            v-bind:key="office.id"
            v-bind:value="office.id"
            v-bind:selected="office.id === session.officeId"
          >
            {{office.name}}
          </option>
        </select>
        <h2>Администраторы</h2>
        <div v-for="(admin, index) in selectedAdmins" v-bind:key="admin.id">
          <label v-on:click.prevent class="grid-x">
            <span class="cell auto">Администратор {{index > 0 ? index + 1 : ''}}</span>
            <button
              type="button" class="button clear small cell shrink remove-employee"
              @click="removeEmployee(admin.id)"
              v-if="index > 0"
            >
              Удалить
            </button>
          </label>
          <select v-model="admin.id">
            <option
              v-for="employee in admins"
              v-bind:key="employee.id"
              v-bind:value="employee.id"
              v-bind:selected="employee.id === admin.id"
            >
              {{employee.name}}
            </option>
          </select>
          <label>Продолжительность смены, часы</label>
          <input type="number" v-model="admin.workHours">
        </div>
        <div>
          <button class="button secondary" type="button" @click="addAdmin">Добавить администратора</button>
        </div>
        <h2>Мастера</h2>
        <div v-for="(master, index) in selectedMasters" v-bind:key="master.id">
          <label v-on:click.prevent class="grid-x">
            <span class="cell auto">Мастер {{index > 0 ? index + 1 : ''}}</span>
            <button
              type="button" class="button clear small cell shrink remove-employee"
              @click="removeEmployee(master.id)"
              v-if="index > 0"
            >
              Удалить
            </button>
          </label>
          <select v-model="master.id">
            <option
              v-for="employee in masters"
              v-bind:key="employee.id"
              v-bind:value="employee.id"
              v-bind:selected="employee.id === master.id"
            >
              {{employee.name}}
            </option>
          </select>
          <label>Продолжительность смены, часы</label>
          <input type="number" v-model="master.workHours">
        </div>
        <div>
          <button class="button secondary" type="button" @click="addMaster">Добавить мастера</button>
        </div>
        <div v-if="session.state === 'open'">
          <button class="button primary" type="button" @click="save">{{session.id ? 'Сохранить' : 'Открыть смену'}}</button>
          <button v-if="session.id" class="button secondary" type="button" @click="closeSession">Закрыть смену</button>
        </div>
      </form>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditSession',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
    if (this.$route.params.id) {
      this.session = {
        'id': 1,
        'dateOpened': '21.09.2019 09:30',
        'dateClosed': null,
        'employees': [
          {
            'id': 1,
            'role': 'officeAdmin',
            'workHours': 6
          },
          {
            'id': 2,
            'role': 'master',
            'workHours': 6
          },
          {
            'id': 3,
            'role': 'master',
            'workHours': 6
          },
          {
            'id': 4,
            'role': 'master',
            'workHours': 6
          }
        ],
        'officeId': 1,
        'state': 'open'
      }
    }
  },
  data () {
    return {
      session: {
        'id': null,
        'dateOpened': null,
        'dateClosed': null,
        'employees': [
          {
            'id': 1,
            'role': 'officeAdmin',
            'workHours': 6
          },
          {
            'id': 2,
            'role': 'master',
            'workHours': 6
          }
        ],
        'officeId': 1,
        'state': 'open'
      }
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
    save: function () {},
    closeSession: function () {}
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
        return this.session.employees.filter(e => e.role === 'officeAdmin')
      },
      set (item) {
        var employeeIndex = this.session.employees.findIndex(e => e.id === item.id)
        item.role = 'officeAdmin'
        this.session.employees.$set(employeeIndex, item)
      }
    },
    selectedMasters: {
      get () {
        return this.session.employees.filter(e => e.role === 'master')
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
  .remove-employee {
    margin: 0;
  }
</style>
