<template>
  <main>
    <appMenu selected-element="history"></appMenu>
    <div class="content grid-x">
      <h1 class="cell small-12">История смен и операций</h1>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'SessionsHistory',
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
