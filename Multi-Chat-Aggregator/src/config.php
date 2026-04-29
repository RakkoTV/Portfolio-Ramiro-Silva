<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

class PlatformConfig {
    private $configFile = 'platform_config.json';

    public function getConfig() {
        if (file_exists($this->configFile)) {
            return json_decode(file_get_contents($this->configFile), true);
        }
        return [];
    }

    public function saveConfig($config) {
        file_put_contents($this->configFile, json_encode($config));
        return ['success' => true];
    }
}

$platformConfig = new PlatformConfig();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode($platformConfig->getConfig());
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    echo json_encode($platformConfig->saveConfig($data));
}