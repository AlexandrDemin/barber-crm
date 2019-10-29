<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/ServiceTypes">Услуги</router-link></li>
        </ul>
      </nav>
      <h1>Тип услуги</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Название</label>
          <input type="text" v-model="serviceType.name" autofocus/>
          <div v-for="price in serviceType.prices" v-bind:key="price">
            <label>Категория мастера: {{$store.getters.getMasterCategoryName(price.category)}}</label>
            <label>Цена</label>
            <input type="number" v-model.number="price.price"/>
          </div>
          <label>Статус</label>
          <v-select
            :clearable="false"
            v-model="serviceType.state"
            :reduce="s => s.id"
            :value="serviceType.state"
            label="name"
            :options="serviceStates"
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
  name: 'EditServiceType',
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
      serviceType: this.getEmptyItem()
    }
  },
  methods: {
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetService/`, {'id': id})
        .then(response => {
          this.serviceType = response.data
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
      HTTP.post(`EditService/`, this.serviceType)
        .then(response => {
          this.isSaving = false
          this.$router.push({name: 'ServiceTypes'})
        })
        .catch(e => {
          this.savingError = e
          this.isSaving = false
        })
    },
    saveAndAddMore: function () {
      this.save()
      this.serviceType = this.getEmptyItem()
      this.$router.push('/EditServiceType')
    },
    getEmptyItem: function () {
      return {
        id: null,
        name: '',
        prices: this.getMergedPrices(),
        state: 'active'
      }
    },
    getMergedPrices: function () {
      var prices = []
      this.$store.state.masterCategories.map(x => {
        var price = 0
        try {
          price = this.serviceType.prices.filter(t => t.category === x.id)[0].price
        } catch (e) {}
        prices.push({
          'category': x.id,
          'price': parseInt(price)
        })
      })
      return prices
    }
  },
  computed: {
    serviceStates: {
      get () {
        return this.$store.state.serviceStates
      }
    }
  }
}
</script>

<style>
</style>
