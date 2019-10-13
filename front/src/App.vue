<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
  watch: {
    $route (to, from) {
      document.title = to.meta.title
    }
  },
  created: function () {
    this.$store.dispatch('getState')
  }
}
</script>
