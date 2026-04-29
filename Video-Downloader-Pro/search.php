<?php
header('Content-Type: application/json');

function searchVideos($query) {
    $apiKey = getenv('YOUTUBE_API_KEY');
    if (!$apiKey) {
        return ['error' => 'API key no configurada'];
    }

    $maxResults = 10;
    
    try {
        $url = 'https://www.googleapis.com/youtube/v3/search?'
             . 'part=snippet'
             . '&type=video'
             . '&maxResults=' . $maxResults
             . '&q=' . urlencode($query)
             . '&key=' . $apiKey;
        
        $context = stream_context_create(['http' => ['ignore_errors' => true]]);
        $response = file_get_contents($url, false, $context);
        
        if ($response === false) {
            return ['error' => 'Error al conectar con la API de YouTube'];
        }
        
        $data = json_decode($response, true);
    
    if (!$data) {
        return ['error' => 'Error al decodificar la respuesta de YouTube'];
    }

    if (isset($data['error'])) {
        $error_message = $data['error']['message'] ?? 'Error desconocido en la API de YouTube';
        return ['error' => $error_message];
    }
    
    if (!isset($data['items']) || empty($data['items'])) {
        return ['videos' => [], 'message' => 'No se encontraron videos'];
    }
    
    $videos = [];
    foreach ($data['items'] as $item) {
        if (isset($item['id']['videoId']) && isset($item['snippet'])) {
            $videos[] = [
                'id' => $item['id']['videoId'],
                'title' => htmlspecialchars($item['snippet']['title']),
                'thumbnail' => $item['snippet']['thumbnails']['medium']['url'] ?? '',
                'channel' => htmlspecialchars($item['snippet']['channelTitle'] ?? ''),
                'description' => htmlspecialchars($item['snippet']['description'] ?? '')
            ];
        }
    }
    
    return ['videos' => $videos];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    $query = $data['query'] ?? '';
    
    if (empty($query)) {
        echo json_encode(['error' => 'Query parameter is required']);
        exit;
    }
    
    $results = searchVideos($query);
    echo json_encode($results);
} else {
    echo json_encode(['error' => 'Method not allowed']);
}