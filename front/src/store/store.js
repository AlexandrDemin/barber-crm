import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    offerid: '',
    maxRivalsCount: 100000,
    sqiDiffCoef: 100,
    maxPos: 10,
    minCountInSerm: 6,
    notRivals: [],
    keywords: [],
    regions: [],
    keywordsWithData: [],
    minKeywordRivals: 2,
    keywordsToDelete: {}
  },
  getters: {
    // Here we will create a getter
  },
  mutations: {
    updateStore (state, payload) {
      state[payload.name] = payload.value
    }
  },
  actions: {
    // Here we will create Larry
  }
})
