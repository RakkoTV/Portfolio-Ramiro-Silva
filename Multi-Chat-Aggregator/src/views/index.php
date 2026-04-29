<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Multiplatform</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 20px;
        }
        .platform-list {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .chat-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            height: 80vh;
        }
        .platform-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .platform-card label {
            display: block;
            margin-bottom: 10px;
        }
        .platform-card input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .message {
            padding: 8px;
            margin-bottom: 8px;
            border-radius: 4px;
            background: #f0f0f0;
        }
        .message .platform {
            font-weight: bold;
            color: #4CAF50;
        }
        .message .user {
            font-weight: bold;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="platform-list" id="platformList"></div>
        <div class="chat-container">
            <div class="chat-messages" id="chatMessages"></div>
        </div>
    </div>

    <script>
        let platforms = [];
        let messageUpdateInterval;

        async function loadConfig() {
            try {
                const response = await fetch('../config.php');
                const config = await response.json();
                platforms = config.length ? config : [
                    { name: 'Twitch', enabled: false, config: { apiKey: '', channelId: '' } },
                    { name: 'Kick', enabled: false, config: { apiKey: '', channelId: '' } },
                    { name: 'Facebook', enabled: false, config: { apiKey: '', channelId: '' } },
                    { name: 'TikTok', enabled: false, config: { apiKey: '', channelId: '' } },
                    { name: 'Instagram', enabled: false, config: { apiKey: '', channelId: '' } },
                    { name: 'YouTube', enabled: false, config: { apiKey: '', channelId: '' } }
                ];
                renderPlatforms();
            } catch (error) {
                console.error('Error loading config:', error);
            }
        }

        function createPlatformCard(platform) {
            const card = document.createElement('div');
            card.className = 'platform-card';
            card.innerHTML = `
                <label>
                    <input type="checkbox" 
                           ${platform.enabled ? 'checked' : ''}
                           onchange="togglePlatform('${platform.name}', this.checked)">
                    ${platform.name}
                </label>
                <input type="text" 
                       placeholder="API Key"
                       value="${platform.config.apiKey}"
                       onchange="updateConfig('${platform.name}', 'apiKey', this.value)">
                <input type="text"
                       placeholder="Channel ID"
                       value="${platform.config.channelId}"
                       onchange="updateConfig('${platform.name}', 'channelId', this.value)">
            `;
            return card;
        }

        async function togglePlatform(platformName, enabled) {
            const platform = platforms.find(p => p.name === platformName);
            if (platform) {
                platform.enabled = enabled;
                await saveConfig();
                if (enabled) {
                    startChatConnection();
                }
            }
        }

        async function updateConfig(platformName, key, value) {
            const platform = platforms.find(p => p.name === platformName);
            if (platform) {
                platform.config[key] = value;
                await saveConfig();
            }
        }

        async function saveConfig() {
            try {
                await fetch('../config.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(platforms)
                });
            } catch (error) {
                console.error('Error saving config:', error);
            }
        }

        function renderPlatforms() {
            const platformList = document.getElementById('platformList');
            platformList.innerHTML = '';
            platforms.forEach(platform => {
                platformList.appendChild(createPlatformCard(platform));
            });
        }

        async function startChatConnection() {
            try {
                const response = await fetch('../chat.php', {
                    method: 'POST'
                });
                const result = await response.json();
                if (result.status === 'connected') {
                    startMessageUpdates();
                }
            } catch (error) {
                console.error('Error connecting to chat:', error);
            }
        }

        async function updateMessages() {
            try {
                const response = await fetch('../chat.php');
                const data = await response.json();
                const chatMessages = document.getElementById('chatMessages');
                data.messages.forEach(msg => {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message';
                    messageDiv.innerHTML = `
                        <span class="platform">[${msg.platform}]</span>
                        <span class="user">${msg.user}:</span>
                        ${msg.message}
                    `;
                    chatMessages.appendChild(messageDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                });
            } catch (error) {
                console.error('Error updating messages:', error);
            }
        }

        function startMessageUpdates() {
            if (!messageUpdateInterval) {
                messageUpdateInterval = setInterval(updateMessages, 3000);
            }
        }

        loadConfig();
    </script>
</body>
</html>