<template>
  <main class="translucent-theme-back">
    <appMenu selected-element="session" visual-style="translucent"></appMenu>
    <div class="content">
      <div class="translucent-theme-block" style="margin: 30px auto; width: 940px; height: 1200px;"></div>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'Session',
  components: {
    appMenu: Menu
  },
  mounted: function () {
    document.title = this.$route.meta.title
  }
}
</script>

<style>
  .content {
    margin-left: 100px;
  }
</style>
