<template>
  <div class="app-container">
    <nav class="main-nav">
      <router-link to="/" class="nav-logo">MultiChat</router-link>
      <div class="nav-links">
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog"></i> Settings
        </router-link>
        <router-link to="/login" class="nav-item" v-if="!user">
          <i class="fas fa-sign-in-alt"></i> Login
        </router-link>
        <a @click="logout" class="nav-item" v-else>
          <i class="fas fa-sign-out-alt"></i> Logout
        </a>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const user = computed(() => store.state.user)

    const logout = () => {
      store.commit('setUser', null)
    }

    return {
      user,
      logout
    }
  }
}
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background: #f5f5f5;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-nav {
  background: #2c3e50;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;

  .nav-logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
  }

  .nav-links {
    display: flex;
    gap: 1rem;

    .nav-item {
      color: white;
      text-decoration: none;
      cursor: pointer;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      transition: background-color 0.3s;

      &:hover {
        background-color: rgba(255, 255, 255, 0.1);
      }

      i {
        margin-right: 0.5rem;
      }
    }
  }
}

.main-content {
  flex: 1;
  padding: 2rem;
}
</style>