import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createStore } from 'vuex'
import App from './App.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/login',
      component: () => import('./views/Login.vue')
    },
    {
      path: '/settings',
      component: () => import('./views/Settings.vue')
    }
  ]
})

const store = createStore({
  state() {
    return {
      user: null,
      platforms: {
        twitch: { enabled: false, config: { apiKey: '', channelId: '' } },
        kick: { enabled: false, config: { apiKey: '', channelId: '' } },
        facebook: { enabled: false, config: { apiKey: '', channelId: '' } },
        tiktok: { enabled: false, config: { apiKey: '', channelId: '' } },
        instagram: { enabled: false, config: { apiKey: '', channelId: '' } },
        youtube: { enabled: false, config: { apiKey: '', channelId: '' } }
      }
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    updatePlatform(state, { platform, config }) {
      state.platforms[platform] = config
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')