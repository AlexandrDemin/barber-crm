<template>
  <header class="app-header">
    <div class="grid-x grid-container">
      <div class="large-6 cell">
        <img src="static/logo.svg" class="app-logo">
      </div>
      <div class="large-6 cell text-right user">demo.user</div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style>
 .app-header {
    box-shadow: 0px 1px 2px rgba(23, 61, 99, 0.15);
    padding: 10px 0;
    margin-bottom: 20px;
 }
 .app-logo {
    height:48px;
 }
 .user {
  padding-top:10px;
 }
</style>
