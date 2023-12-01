import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'
import SignUp from '../views/Signup.vue'
import LogIn from '../views/Login.vue'
import GameMenu from '../views/game/GameMenu.vue'
import Talk from '../views/game/Talk.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requireLogin: false //true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: false
    }
  },
  {
    path: '/game/game-menu',
    name: 'GameMenu',
    component: GameMenu,
    meta: {
      requireLogin: false
    }
  },
  {
    path: '/game/talk/:characterName',
    name: 'GameTalk',
    component: Talk,
    meta: {
      requireLogin: false
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

/*router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/log-in')
  } else {
    next()
  }
})*/

export default router
