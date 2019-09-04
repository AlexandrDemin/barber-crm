<template>
  <ul v-if="project" class="project-info">
    <li>
      Статус:
      <svg width="8" height="8" viewBox="0 0 8 8" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="4" cy="4" r="4" v-bind:fill="$store.getters.getStatusColor(project.status)"/>
      </svg>
      <strong>{{$store.getters.getStatusText(project.status)}}</strong>
    </li>
    <li>Услуга: <strong>{{project.service}}</strong></li>
    <li>ProjectId: <strong>{{project.projectId}}</strong></li>
    <li>Стратегия продвижения: <strong>{{project.strategy}}</strong></li>
  </ul>
</template>

<script>
export default {
  name: 'ProjectInfo',
  props: ['project']
}
</script>

<style>
  .project-info {
    list-style: none;
    margin: 0 0 24px 0;
  }
  .project-info li {
    display: inline-block;
    margin: 0;
    padding: 0 18px 0 0;
  }
</style>
