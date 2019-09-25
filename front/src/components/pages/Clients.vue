<template>
  <main>
    <appMenu selected-element="clients"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">Клиенты</h1>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'Clients',
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
