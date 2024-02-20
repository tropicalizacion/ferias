import Vue from 'vue'
import Router from 'vue-router'
import BuilderPage from '../components/BuilderPage'
import CrosswordPage from '../components/CrosswordPage'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'page.index',
      redirect: '/builder',
    },
    {
      path: '/crossword',
      name: 'page.crossword',
      component: CrosswordPage,
    },
    {
      path: '/builder',
      name: 'page.builder',
      component: BuilderPage,
    },
  ],
})
