<template>
  <main>
    <appMenu selected-element="admin"></appMenu>
    <div class="content grid-x">
      <nav>
        <ul class="breadcrumbs">
          <li><router-link to="/Offices">Отделения</router-link></li>
        </ul>
      </nav>
      <h1 class="cell small-12">Отделение</h1>
      <form class="cell small-6"></form>
    </div>
  </main>
</template>

<script>
import Menu from '@/components/Menu'

export default {
  name: 'EditOffice',
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
