<template>
  <div class="settings-container">
    <div class="settings-card">
      <h2>Settings</h2>

      <div class="settings-section">
        <h3>Platform Settings</h3>
        <div class="platform-list">
          <div v-for="(platform, name) in platforms" :key="name" class="platform-item">
            <div class="platform-header">
              <img :src="getPlatformLogo(name)" :alt="name">
              <h4>{{ formatPlatformName(name) }}</h4>
              <label class="switch">
                <input
                  type="checkbox"
                  v-model="platform.enabled"
                  @change="togglePlatform(name)"
                >
                <span class="slider"></span>
              </label>
            </div>

            <div v-if="platform.enabled" class="platform-config">
              <div class="form-group">
                <label>API Key</label>
                <input
                  type="password"
                  v-model="platform.config.apiKey"
                  placeholder="Enter API Key"
                  @change="updatePlatformConfig(name)"
                >
              </div>
              <div class="form-group">
                <label>Channel ID</label>
                <input
                  type="text"
                  v-model="platform.config.channelId"
                  placeholder="Enter Channel ID"
                  @change="updatePlatformConfig(name)"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="settings-section">
        <h3>Display Settings</h3>
        <div class="form-group">
          <label>Message Display Duration</label>
          <select v-model="displaySettings.messageDuration">
            <option value="5">5 seconds</option>
            <option value="10">10 seconds</option>
            <option value="15">15 seconds</option>
            <option value="0">No limit</option>
          </select>
        </div>

        <div class="form-group">
          <label>Theme</label>
          <select v-model="displaySettings.theme">
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="system">System Default</option>
          </select>
        </div>

        <div class="form-group">
          <label>Font Size</label>
          <select v-model="displaySettings.fontSize">
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="large">Large</option>
          </select>
        </div>
      </div>

      <div class="settings-section">
        <h3>Notification Settings</h3>
        <div class="form-group checkbox">
          <label>
            <input type="checkbox" v-model="notificationSettings.sound">
            Enable Sound Notifications
          </label>
        </div>
        <div class="form-group checkbox">
          <label>
            <input type="checkbox" v-model="notificationSettings.desktop">
            Enable Desktop Notifications
          </label>
        </div>
      </div>

      <button @click="saveSettings" class="save-button">
        <i class="fas fa-save"></i> Save Settings
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Settings',
  setup() {
    const store = useStore()
    const platforms = computed(() => store.state.platforms)

    const displaySettings = ref({
      messageDuration: '10',
      theme: 'light',
      fontSize: 'medium'
    })

    const notificationSettings = ref({
      sound: true,
      desktop: false
    })

    const platformLogos = {
      twitch: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzY0NDE5NSIgZD0iTTExLjU3MSA0LjcxNGgyLjg1N3Y4LjU3MUgxMS41N3ptNy44NTcgMGgyLjg1N3Y4LjU3MUgxOS40M3ptLTE1LjcxNCAwaDIuODU3djguNTcxSDMuNzE0em0xNy4xNDMgMTYuNDI5SDEuMjg2VjEuODU3aDIwLjU3MXYxOS4yODZ6Ii8+PC9zdmc+',
      kick: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwZmYwMCIgZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTEgMC04LTMuNTg5LTgtOHMzLjU4OS04IDgtOCA4IDMuNTg5IDggOC0zLjU4OSA4LTggOHoiLz48L3N2Zz4=',
      facebook: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzE4NzdmMiIgZD0iTTI0IDEyLjA3M2MwLTYuNjI3LTUuMzczLTEyLTEyLTEycy0xMiA1LjM3My0xMiAxMmMwIDUuOTkgNC4zODggMTAuOTU0IDEwLjEyNSAxMS44NTR2LTguMzg1SDcuMDc4di0zLjQ3aDMuMDQ3VjkuNDNjMC0zLjAwNyAxLjc5Mi00LjY2OSA0LjUzMy00LjY2OSAxLjMxMiAwIDIuNjg2LjIzNSAyLjY4Ni4yMzV2Mi45NTNoLTEuNTEzYy0xLjQ5IDAtMS45NTUuOTI1LTEuOTU1IDEuODc0djIuMjVoMy4zMjhsLS41MzIgMy40N2gtMi43OTZ2OC4zODVDMTkuNjEyIDIzLjAyNyAyNCAxOC4wNjIgMjQgMTIuMDczeiIvPjwvc3ZnPg==',
      tiktok: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwMDAwMCIgZD0iTTIyLjUgOS41ODR2My42M2gtNC4xNjd2LTMuNjNoLTMuNjN2NC4xNjdoMy42M3YzLjYzaDQuMTY3di0zLjYzaDMuNjN2LTQuMTY3aC0zLjYzem0tMTEuMjUgMGgtMy42M3Y0LjE2N2gzLjYzdi00LjE2N3ptLTcuMjUgMEguNXY0LjE2N2gzLjYzdi00LjE2N3oiLz48L3N2Zz4=',
      instagram: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMCIgeTE9IjI0IiB4Mj0iMjQiIHkyPSIwIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNmZmQ2MDAiLz48c3RvcCBvZmZzZXQ9IjAuNSIgc3RvcC1jb2xvcj0iI2ZmMDEwMSIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI2Q4MDBiOSIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxwYXRoIGZpbGw9InVybCgjYSkiIGQ9Ik0xMiAyYy0yLjcxNiAwLTMuMDU2LjAxMi00LjEyMy4wNi0xLjA2NC4wNDktMS43OTEuMjE3LTIuNDI3LjQ2M2E0LjkwMiA0LjkwMiAwIDAwLTEuNzcyIDEuMTUzIDQuOTAyIDQuOTAyIDAgMDAtMS4xNTMgMS43NzJjLS4yNDYuNjM2LS40MTQgMS4zNjMtLjQ2MyAyLjQyN0MyLjAxMiA4Ljk0NCAyIDkuMjg0IDIgMTJzLjAxMiAzLjA1Ni4wNiA0LjEyM2MuMDQ5IDEuMDY0LjIxNyAxLjc5MS40NjMgMi40MjdhNC45MDIgNC45MDIgMCAwMDEuMTUzIDEuNzcyIDQuOTAyIDQuOTAyIDAgMDAxLjc3MiAxLjE1M2MuNjM2LjI0NiAxLjM2My40MTQgMi40MjcuNDYzIDEuMDY3LjA0OCAxLjQwNy4wNiA0LjEyMy4wNnMzLjA1Ni0uMDEyIDQuMTIzLS4wNmMxLjA2NC0uMDQ5IDEuNzkxLS4yMTcgMi40MjctLjQ2M2E0LjkwMiA0LjkwMiAwIDAwMS43NzItMS4xNTMgNC45MDIgNC45MDIgMCAwMDEuMTUzLTEuNzcyYy4yNDYtLjYzNi40MTQtMS4zNjMuNDYzLTIuNDI3LjA0OC0xLjA2Ny4wNi0xLjQwNy4wNi00LjEyM3MtLjAxMi0zLjA1Ni0uMDYtNC4xMjNjLS4wNDktMS4wNjQtLjIxNy0xLjc5MS0uNDYzLTIuNDI3YTQuOTAyIDQuOTAyIDAgMDAtMS4xNTMtMS43NzJBNC45MDIgNC45MDIgMCAwMDE4LjU1IDIuNTIzYy0uNjM2LS4yNDYtMS4zNjMtLjQxNC0yLjQyNy0uNDYzQzE1LjA1NiAyLjAxMiAxNC43MTYgMiAxMiAyem0wIDEuODAyYzIuNjcgMCAyLjk4Ni4wMSA0LjA0LjA1OC45NzYuMDQ1IDEuNTA1LjIwNyAxLjg1OC4zNDQuNDY3LjE4Mi44LjM5OSAxLjE1Ljc0OC4zNS4zNS41NjYuNjgzLjc0OCAxLjE1LjEzNy4zNTMuMy44ODIuMzQ0IDEuODU3LjA0OCAxLjA1NS4wNTggMS4zNy4wNTggNC4wNDFzLS4wMSAyLjk4Ni0uMDU4IDQuMDQxYy0uMDQ0Ljk3Ni0uMjA3IDEuNTA1LS4zNDQgMS44NTgtLjE4Mi40NjctLjM5OS44LS43NDggMS4xNS0uMzUuMzUtLjY4My41NjYtMS4xNS43NDgtLjM1My4xMzctLjg4Mi4zLTEuODU3LjM0NC0xLjA1NC4wNDgtMS4zNy4wNTgtNC4wNDEuMDU4cy0yLjk4Ny0uMDEtNC4wNC0uMDU4Yy0uOTc2LS4wNDUtMS41MDUtLjIwNy0xLjg1OC0uMzQ0YTMuMDk3IDMuMDk3IDAgMDEtMS4xNS0uNzQ4IDMuMDk3IDMuMDk3IDAgMDEtLjc0OC0xLjE1Yy0uMTM3LS4zNTMtLjMtLjg4Mi0uMzQ0LTEuODU3LS4wNDgtMS4wNTUtLjA1OC0xLjM3LS4wNTgtNC4wNDFzLjAxLTIuOTg2LjA1OC00LjA0Yy4wNDQtLjk3Ni4yMDctMS41MDUuMzQ0LTEuODU4LjE4Mi0uNDY3LjM5OS0uOC43NDgtMS4xNS4zNS0uMzUuNjgzLS41NjYgMS4xNS0uNzQ4LjM1My0uMTM3Ljg4Mi0uMyAxLjg1Ny0uMzQ0IDEuMDU0LS4wNDggMS4zNy0uMDU4IDQuMDQxLS4wNTh6Ii8+PC9zdmc+',
      youtube: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmMDAwMCIgZD0iTTIzLjQ5NSA2LjIwNWEzLjAwNyAzLjAwNyAwIDAwLTIuMDg4LTIuMDg4Yy0xLjg3LS41MDEtOS4zOTYtLjUwMS05LjM5Ni0uNTAxcy03LjUwNy0uMDEtOS4zOTYuNTAxQTMuMDA3IDMuMDA3IDAgMDAuNTI3IDYuMjA1YTMxLjI0NyAzMS4yNDcgMCAwMC0uNTIyIDUuODA1IDMxLjI0NyAzMS4yNDcgMCAwMC41MjIgNS43ODMgMy4wMDcgMy4wMDcgMCAwMDIuMDg4IDIuMDg4YzEuODY4LjUwMiA5LjM5Ni41MDIgOS4zOTYuNTAyczc1MDctLjAwOSA5LjM5Ni0uNTAyYTMuMDA3IDMuMDA3IDAgMDAyLjA4OC0yLjA4OCAzMS4yNDcgMzEuMjQ3IDAgMDAuNTIyLTUuNzgzIDMxLjI0NyAzMS4yNDcgMCAwMC0uNTIyLTUuODA1ek05LjYwOSAxNS42MDFWOC40MDhsNi4yNjQgMy42MDJ6Ii8+PC9zdmc+',
      custom: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzgwODA4MCIgZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTEgMC04LTMuNTg5LTgtOHMzLjU4OS04IDgtOCA4IDMuNTg5IDggOC0zLjU4OSA4LTggOHoiLz48L3N2Zz4='
    }

    const getPlatformLogo = (platform) => {
      return platformLogos[platform.toLowerCase()] || platformLogos.custom
    }

    const formatPlatformName = (name) => {
      return name.charAt(0).toUpperCase() + name.slice(1)
    }

    const togglePlatform = (platform) => {
      store.commit('togglePlatform', platform)
    }

    const updatePlatformConfig = (platform) => {
      store.commit('updatePlatformConfig', {
        platform,
        config: platforms.value[platform].config
      })
    }

    const saveSettings = () => {
      // Save settings to local storage or backend
      console.log('Settings saved')
    }

    return {
      platforms,
      displaySettings,
      notificationSettings,
      getPlatformLogo,
      formatPlatformName,
      togglePlatform,
      updatePlatformConfig,
      saveSettings
    }
  }
}
</script>

<style lang="scss" scoped>
.settings-container {
  padding: 1rem;
}

.settings-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;

  h2 {
    margin-bottom: 2rem;
    color: #2c3e50;
    text-align: center;
  }
}

.settings-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;

  &:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  h3 {
    margin-bottom: 1rem;
    color: #2c3e50;
  }
}

.platform-list {
  display: grid;
  gap: 1rem;
}

.platform-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;

  .platform-header {
    display: flex;
    align-items: center;
    gap: 1rem;

    img {
      width: 24px;
      height: 24px;
    }

    h4 {
      margin: 0;
      flex: 1;
    }
  }
}

.platform-config {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.form-group {
  margin-bottom: 1rem;

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }

  input,
  select {
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

  &.checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;

    label {
      margin: 0;
      cursor: pointer;
    }

    input[type="checkbox"] {
      width: auto;
      cursor: pointer;
    }
  }
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;

  input {
    opacity: 0;
    width: 0;
    height: 0;

    &:checked + .slider {
      background-color: #2ecc71;
    }

    &:checked + .slider:before {
      transform: translateX(26px);
    }
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;

    &:before {
      position: absolute;
      content: "";
      height: 16px;
      width: 16px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: .4s;
      border-radius: 50%;
    }
  }
}

.save-button {
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
</style>