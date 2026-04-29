<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

class ChatHandler {
    private $platforms = [];
    
    public function __construct() {
        $configFile = 'platform_config.json';
        if (file_exists($configFile)) {
            $this->platforms = json_decode(file_get_contents($configFile), true);
        }
    }
    
    public function connect() {
        $enabledPlatforms = array_filter($this->platforms, function($platform) {
            return $platform['enabled'];
        });
        
        return [
            'status' => 'connected',
            'platforms' => array_keys($enabledPlatforms)
        ];
    }
    
    public function getMessages() {
        // Simulación de mensajes para demostración
        return [
            'messages' => [
                ['platform' => 'Twitch', 'user' => 'usuario1', 'message' => 'Hola desde Twitch'],
                ['platform' => 'YouTube', 'user' => 'usuario2', 'message' => 'Hola desde YouTube']
            ]
        ];
    }
}

$chatHandler = new ChatHandler();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode($chatHandler->getMessages());
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo json_encode($chatHandler->connect());
}