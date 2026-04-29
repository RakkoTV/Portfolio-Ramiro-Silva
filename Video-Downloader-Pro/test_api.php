<?php
header('Content-Type: application/json');

// Configuración
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// API Key de YouTube
define('YOUTUBE_API_KEY', 'AIzaSyBjnPaYlAI7EmJxdhIaqkfBQPPihwrAAxY');

// Función para realizar pruebas de la API
function testYouTubeAPI() {
    $tests = [
        'connection' => [
            'name' => 'Prueba de Conexión Básica',
            'endpoint' => 'https://www.googleapis.com/youtube/v3/videos',
            'params' => ['part' => 'snippet', 'chart' => 'mostPopular', 'maxResults' => 1]
        ],
        'search' => [
            'name' => 'Prueba de Búsqueda',
            'endpoint' => 'https://www.googleapis.com/youtube/v3/search',
            'params' => ['part' => 'snippet', 'q' => 'test', 'maxResults' => 1]
        ],
        'channels' => [
            'name' => 'Prueba de Canales',
            'endpoint' => 'https://www.googleapis.com/youtube/v3/channels',
            'params' => ['part' => 'snippet', 'forUsername' => 'Google']
        ]
    ];

    $results = [];

    foreach ($tests as $key => $test) {
        $params = array_merge($test['params'], ['key' => YOUTUBE_API_KEY]);
        $url = $test['endpoint'] . '?' . http_build_query($params);

        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]);

        $startTime = microtime(true);
        $response = curl_exec($ch);
        $endTime = microtime(true);

        $httpStatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        $responseTime = round(($endTime - $startTime) * 1000, 2); // en milisegundos
        $httpStatus = $httpStatus ? "HTTP/{$httpStatus}" : 'No response';

        $results[$key] = [
            'name' => $test['name'],
            'success' => $response !== false && empty($curlError),
            'response_time' => $responseTime . 'ms',
            'http_status' => $httpStatus,
            'error' => !empty($curlError) ? $curlError : ($response === false ? 'Failed to get response' : null),
            'response' => $response !== false ? json_decode($response, true) : null
        ];

        // Agregar detalles del error si existe
        if ($response !== false) {
            $data = json_decode($response, true);
            if (isset($data['error'])) {
                $results[$key]['error_details'] = $data['error'];
            }
        }
    }

    return [
        'timestamp' => date('Y-m-d H:i:s'),
        'api_key_length' => strlen(YOUTUBE_API_KEY),
        'tests' => $results
    ];
}

try {
    $testResults = testYouTubeAPI();
    echo json_encode(['success' => true, 'data' => $testResults], JSON_PRETTY_PRINT);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'trace' => $e->getTraceAsString()
    ], JSON_PRETTY_PRINT);
}