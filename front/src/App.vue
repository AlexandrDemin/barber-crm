<template>
  <div id="app">
    <appheader></appheader>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from '@/components/Header'

export default {
  name: 'App',
  components: {
    appheader: Header
  },
  watch: {
    $route (to, from) {
      document.title = to.meta.title
    }
  }
}
</script>
