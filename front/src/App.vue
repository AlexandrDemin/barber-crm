<template>
  <div id="app">
    <vue-element-loading :active="isStateLoading" :is-full-screen="true" color="#1C457D"/>
    <router-view></router-view>
  </div>
</template>

<script>
import VueElementLoading from 'vue-element-loading'

export default {
  name: 'App',
  components: {
    VueElementLoading
  },
  watch: {
    $route (to, from) {
      document.title = to.meta.title
    }
  },
  computed: {
    isStateLoading: function () {
      return this.$store.state.isStateLoading
    }
  },
  created: function () {
    this.$store.dispatch('getState')
  }
}
</script>
