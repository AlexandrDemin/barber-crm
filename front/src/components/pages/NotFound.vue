<template>
  <main>
    <appMenu></appMenu>
    <div class="content">
      <h1>Страница не найдена</h1>
      <p><a href="/">На главную</a></p>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'NotFound',
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
