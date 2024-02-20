// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueGoogleApi from 'vue-google-api'

import './shitcode'
import App from './App'
import { http, eventbus } from './plugins'

Vue.config.devTools = true
Vue.config.productionTip = false

Vue.use(http)
Vue.use(eventbus)
Vue.use(VueGoogleApi, {
  scope: 'profile',
  discoveryDocs: ['https://people.googleapis.com/$discovery/rest'],
})

/* eslint-disable no-new */
new Vue({
  el: '#crossword',

  components: { App },

  data: () => ({
    user: null,
  }),

  mounted () {
    this.$bus.$on('user::update', (user) => {
      this.user = user
    })

    this.$bus.$on('user::clear', () => {
      this.user = null
    })
  },

  methods: {
    serialize (obj, prefix) {
      let str = []
      let prop

      for (prop in obj) {
        if (obj.hasOwnProperty(prop)) { // eslint-disable-line
          let key = prefix ? `${prefix}[${prop}]` : prop
          let value = obj[prop]

          str.push((value !== null && typeof value === 'object')
            ? this.serialize(value, key)
            : encodeURIComponent(key) + '=' + encodeURIComponent(value))
        }
      }
      return str.join('&')
    },

    async fetch (url) {
      const response = await fetch(url, { mode: 'no-cors' })

      return response
    },

    getAllWordCells (words) {
      return words.flatMap(this.getWordCells)
    },

    getWordCells ({ word, x, y, isVertical }) {
      return Array.from({ length: word.length || word.word.length })
        .map((letter, idx) => isVertical ? `${x}:${y + idx}` : `${x + idx}:${y}`)
    },

    getWordLetters ({ word }) {
      return Array.from({ length: word.length })
        .map((letter, idx) => word[`letter_${idx + 1}`])
    },
  },

  template: '<App :user="user" />',
})

export const MAX_GRID_SIZE = 40
