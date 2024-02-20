import axios from 'axios'


export const http = axios.create({
  baseURL: 'https://crossword.live/crossword',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
})

export default function install (Vue) {
  Object.defineProperty(Vue.prototype, '$http', {
    get () {
      return http
    },
  })
}
