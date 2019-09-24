<template>
  <div id="app" class="translucent-theme">
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
  }
}
</script>
