<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content">
      <h1>Загрузка расходов</h1>
      <div class="grid-x grid-margin-x align-middle">
        <div class="cell shrink">
          <button class="button no-margin" type="button">Загрузить расходы</button>
          <input type="file" ref="file" style="display:none">
        </div>
        <div class="cell auto">
          <router-link to="">Скачать шаблон</router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'UploadExpenses',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
  },
  data () {
    return {}
  },
  methods: {},
  computed: {}
}
</script>

<style>
</style>
