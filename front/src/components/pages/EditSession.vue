<template>
  <main>
    <appMenu selected-element="session"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">Смена</h1>
      <form class="cell small-6"></form>
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
