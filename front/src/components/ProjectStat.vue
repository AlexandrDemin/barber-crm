<template>
  <div class="project-stat">
      <h2>{{domain}}&nbsp;<small><a v-bind:href="projectLinkUrl" target="_blank">{{projectId}}</a></small></h2>
      <div class="grid-x grid-padding-x grid-padding-y">
        <div class="large-6 cell">
          <h4>Расход за месяц <small>Прогноз до конца месяца</small></h4>
          <line-chart :data="monthSpend"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>Трафик за месяц <small>Прогноз до конца месяца</small></h4>
          <line-chart :data="monthTraffic"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>Трафик за день <small>Прогноз за день</small></h4>
          <line-chart :data="dayTraffic"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>Расход по дням <small>Прогноз за день</small></h4>
          <line-chart :data="daySpend"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>Конверсии за месяц <small>Прогноз за месяц, факт в сумме за месяц</small></h4>
          <line-chart :data="dayConversions"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>CPC <small>Прогноз за месяц</small></h4>
          <line-chart :data="cpc"></line-chart>
        </div>
        <div class="large-6 cell">
          <h4>CPA <small>Прогноз за месяц</small></h4>
          <line-chart :data="cpa"></line-chart>
        </div>
      </div>
  </div>
</template>

<script>
import Vue from 'vue'
import Chartkick from 'chartkick'
import VueChartkick from 'vue-chartkick'
import Highcharts from 'highcharts'

window.Highcharts = Highcharts
Vue.use(VueChartkick, { Chartkick })

export default {
  name: 'ProjectStat',
  props: ['projectId', 'domain', 'holidays', 'dayTraffic', 'daySpend', 'dayConversions',
    'cpc', 'cpa', 'monthSpend', 'monthTraffic'],
  computed: {
    projectLinkUrl: function () {
      return 'http://motor.local/Direct/BidsControl?projectId=' + this.projectId
    }
  },
  data () {
    return {
    }
  },
  methods: {
  },
  created () {
  }
}
</script>

<style>
  .project-stat {
    margin-bottom: 30px;
  }
</style>
