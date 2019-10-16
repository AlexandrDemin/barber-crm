<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/GoodsTypes">Товары</router-link></li>
        </ul>
      </nav>
      <h1>Товар</h1>
      <div v-if="loadingError" class="callout alert">
        <h5>Произошла ошибка при загрузке данных</h5>
        <p>{{loadingError}}</p>
      </div>
      <div class="grid-x">
        <vue-element-loading :active="isLoading" color="#1C457D"/>
        <div class="cell large-6">
          <label>Название</label>
          <input type="text" v-model="goodsType.name" autofocus/>
          <label>Цена</label>
          <input type="number" v-model="goodsType.price" autofocus/>
          <label>Статус</label>
          <select v-model="goodsType.state">
            <option
              v-for="item in goodsStates"
              v-bind:key="item.id"
              v-bind:value="item.id"
              v-bind:selected="item.id === goodsType.state"
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
  name: 'EditGoodsType',
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
      goodsType: this.getEmptyItem()
    }
  },
  methods: {
    load: function (id) {
      this.isLoading = true
      this.loadingError = ''
      HTTP.post(`GetGood/`, {'id': id})
        .then(response => {
          this.goodsType = response.data
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
      HTTP.post(`EditGood/`, this.goodsType)
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
      this.goodsType = this.getEmptyItem()
      this.$router.push('/EditGoodsType')
    },
    getEmptyItem: function () {
      return {
        id: 'null',
        name: '',
        price: '',
        state: 'active'
      }
    }
  },
  computed: {
    goodsStates: {
      get () {
        return this.$store.state.goodsStates
      }
    }
  }
}
</script>

<style>
</style>
