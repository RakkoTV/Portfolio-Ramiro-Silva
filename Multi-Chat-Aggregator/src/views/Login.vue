<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            placeholder="Enter your username"
          >
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="Enter your password"
          >
        </div>
        <button type="submit" class="login-button">
          <i class="fas fa-sign-in-alt"></i> Login
        </button>
      </form>

      <div class="platform-connections">
        <h3>Connect Platforms</h3>
        <div class="platform-grid">
          <div
            v-for="platform in platforms"
            :key="platform.name"
            class="platform-item"
            :class="{ 'connected': platform.connected }"
            @click="togglePlatform(platform.name)"
          >
            <img :src="platform.logo" :alt="platform.name">
            <span>{{ platform.name }}</span>
            <i
              class="fas"
              :class="platform.connected ? 'fa-check-circle' : 'fa-plus-circle'"
            ></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const platforms = [
      {
        name: 'Twitch',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzY0NDE5NSIgZD0iTTExLjU3MSA0LjcxNGgyLjg1N3Y4LjU3MUgxMS41N3ptNy44NTcgMGgyLjg1N3Y4LjU3MUgxOS40M3ptLTE1LjcxNCAwaDIuODU3djguNTcxSDMuNzE0em0xNy4xNDMgMTYuNDI5SDEuMjg2VjEuODU3aDIwLjU3MXYxOS4yODZ6Ii8+PC9zdmc+',
        connected: false
      },
      {
        name: 'Kick',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwZmYwMCIgZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTEgMC04LTMuNTg5LTgtOHMzLjU4OS04IDgtOCA4IDMuNTg5IDggOC0zLjU4OSA4LTggOHoiLz48L3N2Zz4=',
        connected: false
      },
      {
        name: 'Facebook',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzE4NzdmMiIgZD0iTTI0IDEyLjA3M2MwLTYuNjI3LTUuMzczLTEyLTEyLTEycy0xMiA1LjM3My0xMiAxMmMwIDUuOTkgNC4zODggMTAuOTU0IDEwLjEyNSAxMS44NTR2LTguMzg1SDcuMDc4di0zLjQ3aDMuMDQ3VjkuNDNjMC0zLjAwNyAxLjc5Mi00LjY2OSA0LjUzMy00LjY2OSAxLjMxMiAwIDIuNjg2LjIzNSAyLjY4Ni4yMzV2Mi45NTNoLTEuNTEzYy0xLjQ5IDAtMS45NTUuOTI1LTEuOTU1IDEuODc0djIuMjVoMy4zMjhsLS41MzIgMy40N2gtMi43OTZ2OC4zODVDMTkuNjEyIDIzLjAyNyAyNCAxOC4wNjIgMjQgMTIuMDczeiIvPjwvc3ZnPg==',
        connected: false
      },
      {
        name: 'TikTok',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwMDAwMCIgZD0iTTIyLjUgOS41ODR2My42M2gtNC4xNjd2LTMuNjNoLTMuNjN2NC4xNjdoMy42M3YzLjYzaDQuMTY3di0zLjYzaDMuNjN2LTQuMTY3aC0zLjYzem0tMTEuMjUgMGgtMy42M3Y0LjE2N2gzLjYzdi00LjE2N3ptLTcuMjUgMEguNXY0LjE2N2gzLjYzdi00LjE2N3oiLz48L3N2Zz4=',
        connected: false
      },
      {
        name: 'Instagram',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMCIgeTE9IjI0IiB4Mj0iMjQiIHkyPSIwIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNmZmQ2MDAiLz48c3RvcCBvZmZzZXQ9IjAuNSIgc3RvcC1jb2xvcj0iI2ZmMDEwMSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI2Q4MDBiOSIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxwYXRoIGZpbGw9InVybCgjYSkiIGQ9Ik0xMiAyYy0yLjcxNiAwLTMuMDU2LjAxMi00LjEyMy4wNi0xLjA2NC4wNDktMS43OTEuMjE3LTIuNDI3LjQ2M2E0LjkwMiA0LjkwMiAwIDAwLTEuNzcyIDEuMTUzIDQuOTAyIDQuOTAyIDAgMDAtMS4xNTMgMS43NzJjLS4yNDYuNjM2LS40MTQgMS4zNjMtLjQ2MyAyLjQyN0MyLjAxMiA4Ljk0NCAyIDkuMjg0IDIgMTJzLjAxMiAzLjA1Ni4wNiA0LjEyM2MuMDQ5IDEuMDY0LjIxNyAxLjc5MS40NjMgMi40MjdhNC45MDIgNC45MDIgMCAwMDEuMTUzIDEuNzcyIDQuOTAyIDQuOTAyIDAgMDAxLjc3MiAxLjE1M2MuNjM2LjI0NiAxLjM2My40MTQgMi40MjcuNDYzIDEuMDY3LjA0OCAxLjQwNy4wNiA0LjEyMy4wNnMzLjA1Ni0uMDEyIDQuMTIzLS4wNmMxLjA2NC0uMDQ5IDEuNzkxLS4yMTcgMi40MjctLjQ2M2E0LjkwMiA0LjkwMiAwIDAwMS43NzItMS4xNTMgNC45MDIgNC45MDIgMCAwMDEuMTUzLTEuNzcyYy4yNDYtLjYzNi40MTQtMS4zNjMuNDYzLTIuNDI3LjA0OC0xLjA2Ny4wNi0xLjQwNy4wNi00LjEyM3MtLjAxMi0zLjA1Ni0uMDYtNC4xMjNjLS4wNDktMS4wNjQtLjIxNy0xLjc5MS0uNDYzLTIuNDI3YTQuOTAyIDQuOTAyIDAgMDAtMS4xNTMtMS43NzJBNC45MDIgNC45MDIgMCAwMDE4LjU1IDIuNTIzYy0uNjM2LS4yNDYtMS4zNjMtLjQxNC0yLjQyNy0uNDYzQzE1LjA1NiAyLjAxMiAxNC43MTYgMiAxMiAyem0wIDEuODAyYzIuNjcgMCAyLjk4Ni4wMSA0LjA0LjA1OC45NzYuMDQ1IDEuNTA1LjIwNyAxLjg1OC4zNDQuNDY3LjE4Mi44LjM5OSAxLjE1Ljc0OC4zNS4zNS41NjYuNjgzLjc0OCAxLjE1LjEzNy4zNTMuMy44ODIuMzQ0IDEuODU3LjA0OCAxLjA1NS4wNTggMS4zNy4wNTggNC4wNDFzLS4wMSAyLjk4Ni0uMDU4IDQuMDQxYy0uMDQ0Ljk3Ni0uMjA3IDEuNTA1LS4zNDQgMS44NTgtLjE4Mi40NjctLjM5OS44LS43NDggMS4xNS0uMzUuMzUtLjY4My41NjYtMS4xNS43NDgtLjM1My4xMzctLjg4Mi4zLTEuODU3LjM0NC0xLjA1NC4wNDgtMS4zNy4wNTgtNC4wNDEuMDU4cy0yLjk4Ny0uMDEtNC4wNC0uMDU4Yy0uOTc2LS4wNDUtMS41MDUtLjIwNy0xLjg1OC0uMzQ0YTMuMDk3IDMuMDk3IDAgMDEtMS4xNS0uNzQ4IDMuMDk3IDMuMDk3IDAgMDEtLjc0OC0xLjE1Yy0uMTM3LS4zNTMtLjMtLjg4Mi0uMzQ0LTEuODU3LS4wNDgtMS4wNTUtLjA1OC0xLjM3LS4wNTgtNC4wNDFzLjAxLTIuOTg2LjA1OC00LjA0Yy4wNDQtLjk3Ni4yMDctMS41MDUuMzQ0LTEuODU4LjE4Mi0uNDY3LjM5OS0uOC43NDgtMS4xNS4zNS0uMzUuNjgzLS41NjYgMS4xNS0uNzQ4LjM1My0uMTM3Ljg4Mi0uMyAxLjg1Ny0uMzQ0IDEuMDU0LS4wNDggMS4zNy0uMDU4IDQuMDQxLS4wNTh6Ii8+PC9zdmc+',
        connected: false
      },
      {
        name: 'YouTube',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmMDAwMCIgZD0iTTIzLjQ5NSA2LjIwNWEzLjAwNyAzLjAwNyAwIDAwLTIuMDg4LTIuMDg4Yy0xLjg3LS41MDEtOS4zOTYtLjUwMS05LjM5Ni0uNTAxcy03LjUwNy0uMDEtOS4zOTYuNTAxQTMuMDA3IDMuMDA3IDAgMDAuNTI3IDYuMjA1YTMxLjI0NyAzMS4yNDcgMCAwMC0uNTIyIDUuODA1IDMxLjI0NyAzMS4yNDcgMCAwMC41MjIgNS43ODMgMy4wMDcgMy4wMDcgMCAwMDIuMDg4IDIuMDg4YzEuODY4LjUwMiA5LjM5Ni41MDIgOS4zOTYuNTAyczc1MDctLjAwOSA5LjM5Ni0uNTAyYTMuMDA3IDMuMDA3IDAgMDAyLjA4OC0yLjA4OCAzMS4yNDcgMzEuMjQ3IDAgMDAuNTIyLTUuNzgzIDMxLjI0NyAzMS4yNDcgMCAwMC0uNTIyLTUuODA1ek05LjYwOSAxNS42MDFWOC40MDhsNi4yNjQgMy42MDJ6Ii8+PC9zdmc+',
        connected: false
      },
      {
        name: 'Custom',
        logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzgwODA4MCIgZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTEgMC04LTMuNTg5LTgtOHMzLjU4OS04IDgtOCA4IDMuNTg5IDggOC0zLjU4OSA4LTggOHoiLz48L3N2Zz4=',
        connected: false
      }
    ]

    const handleLogin = () => {
      // In a real app, validate credentials here
      store.commit('setUser', { username: username.value })
      router.push('/')
    }

    const togglePlatform = (platformName) => {
      const platform = platforms.find(p => p.name === platformName)
      if (platform) {
        platform.connected = !platform.connected
        store.commit('togglePlatform', platformName.toLowerCase())
      }
    }

    return {
      username,
      password,
      platforms,
      handleLogin,
      togglePlatform
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px);
}

.login-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 500px;

  h2 {
    margin-bottom: 1.5rem;
    color: #2c3e50;
    text-align: center;
  }
}

.login-form {
  margin-bottom: 2rem;

  .form-group {
    margin-bottom: 1rem;

    label {
      display: block;
      margin-bottom: 0.5rem;
      color: #2c3e50;
    }

    input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;

      &:focus {
        outline: none;
        border-color: #3498db;
      }
    }
  }
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background: #2980b9;
  }

  i {
    margin-right: 0.5rem;
  }
}

.platform-connections {
  h3 {
    margin-bottom: 1rem;
    color: #2c3e50;
    text-align: center;
  }
}

.platform-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}

.platform-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  &.connected {
    border-color: #2ecc71;
    background: #f1f9f1;
  }

  img {
    width: 32px;
    height: 32px;
    margin-bottom: 0.5rem;
  }

  span {
    font-size: 0.9rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }

  i {
    color: #2ecc71;
  }
}
</style>