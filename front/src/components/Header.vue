<template>
  <header class="app-header">
    <div class="grid-x grid-container fluid">
      <div class="small-4 cell">
        <a href=""><img src="static/logo.svg" class="app-logo"></a>
      </div>
      <div class="cell auto text-right user">demo.user</div>
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
    margin-bottom: 24px;
 }
 .app-logo {
    height:38px;
 }
 .user {
  padding-top:8px;
 }
</style>
