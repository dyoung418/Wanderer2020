import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Account from './views/Account.vue'
import Level from './views/Level.vue'
import LevelMenuCustom from './views/LevelMenuCustom.vue'
import LevelMenuOriginal from './views/LevelMenuOriginal.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import ViewAccount from './views/ViewAccount.vue'
import LevelCreator from './views/LevelCreator.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/account',
      name: 'account',
      component: Account
    },
    {
      path: '/level/:num',
      name: 'level',
      component: Level
    },
    {
      path: '/levelmenu/custom/:page',
      name: 'levelmenucustom',
      component: LevelMenuCustom
    },
    {
      path: '/levelmenu/original/:page',
      name: 'levelmenuoriginal',
      component: LevelMenuOriginal
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/account/:username',
      name: 'viewaccount',
      component: ViewAccount
    },
    {
      path: '/levelcreator',
      name: 'levelcreator',
      component: LevelCreator
    },
  ]
})
