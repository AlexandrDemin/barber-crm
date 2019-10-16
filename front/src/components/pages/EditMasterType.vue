<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/MasterTypes">Категории мастеров</router-link></li>
        </ul>
      </nav>
      <h1>Категория мастера</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Название</label>
          <input type="text" v-model="masterCategory.name" autofocus/>
          <label>Статус</label>
          <select v-model="masterCategory.state">
            <option
              v-for="item in masterCategoryStates"
              v-bind:key="item.id"
              v-bind:value="item.id"
              v-bind:selected="item.id === masterCategory.state"
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
  name: 'EditMasterType',
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
      masterCategory: this.getEmptyItem()
    }
  },
  methods: {
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetBarberCategory/`, {'id': id})
        .then(response => {
          this.masterCategory = response.data
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
      HTTP.post(`EditBarberCategory/`, this.masterCategory)
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
      this.masterCategory = this.getEmptyItem()
      this.$router.push('/EditMasterType')
    },
    getEmptyItem: function () {
      return {
        id: 'null',
        name: '',
        state: 'active'
      }
    }
  },
  computed: {
    masterCategoryStates: {
      get () {
        return this.$store.state.masterCategoryStates
      }
    }
  }
}
</script>

<style>
</style>
