<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messageContainer">
      <div v-for="message in messages" :key="message.id" class="message-item">
        <div class="message-header">
          <img :src="getPlatformLogo(message.platform)" :alt="message.platform" class="platform-logo">
          <span class="username">{{ message.username }}</span>
          <span class="timestamp">{{ formatTimestamp(message.timestamp) }}</span>
        </div>
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const messageContainer = ref(null)
    const messages = computed(() => store.state.messages)

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

    const formatTimestamp = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }

    watch(messages, () => {
      if (messageContainer.value) {
        setTimeout(() => {
          messageContainer.value.scrollTop = messageContainer.value.scrollHeight
        }, 50)
      }
    })

    return {
      messages,
      getPlatformLogo,
      formatTimestamp,
      messageContainer
    }
  }
}
</script>

<style lang="scss" scoped>
.chat-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 150px);
  overflow: hidden;
}

.chat-messages {
  height: 100%;
  overflow-y: auto;
  padding: 1rem;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
  }
}

.message-item {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: #f8f9fa;
  transition: background-color 0.2s;

  &:hover {
    background: #f1f3f5;
  }
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  gap: 0.5rem;

  .platform-logo {
    width: 20px;
    height: 20px;
  }

  .username {
    font-weight: bold;
    color: #2c3e50;
  }

  .timestamp {
    color: #6c757d;
    font-size: 0.8rem;
    margin-left: auto;
  }
}

.message-content {
  color: #343a40;
  line-height: 1.4;
  word-break: break-word;
}
</style>