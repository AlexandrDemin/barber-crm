<template>
  <main>
    <appMenu selected-element="reports"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">Отчёт по клиентам</h1>
      <form class="cell small-6"></form>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'ClientsReport',
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
