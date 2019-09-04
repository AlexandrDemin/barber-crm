<template>
  <div>
    <ul v-if="crumbs" class="bread-crumbs">
      <li v-for="crumb in crumbs" v-bind:key="crumb.text">
        <a v-bind:href="crumb.link">{{crumb.text}}</a>
        <span>&nbsp;/&nbsp;</span>
      </li>
    </ul>
    <h1>{{header}}</h1>
  </div>
</template>

<script>
export default {
  name: 'BreadCrumbs',
  props: ['header', 'crumbs']
}
</script>

<style>
  .bread-crumbs {
    list-style: none;
    margin: 0;
  }
  .bread-crumbs li {
    display: inline-block;
    margin: 0;
    padding: 0;
  }
  h1 {
    margin-bottom: 24px;
  }
</style>
