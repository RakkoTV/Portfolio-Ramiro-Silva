<?php
header('Content-Type: application/json');

// Cargar variables de entorno desde .env
if (file_exists('.env')) {
    $env = parse_ini_file('.env');
    if ($env && isset($env['OPENAI_API_KEY'])) {
        $API_KEY = $env['OPENAI_API_KEY'];
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'API key no encontrada en el archivo .env']);
        exit;
    }
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Archivo .env no encontrado. Por favor, crea el archivo con la variable OPENAI_API_KEY']);
    exit;
}

// Recibir datos POST
$data = json_decode(file_get_contents('php://input'), true);

if (!isset($data['text']) || !isset($data['language'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Datos incompletos']);
    exit;
}

$text = $data['text'];
$language = $data['language'];

// Preparar el prompt para OpenAI
$prompt = "Basado en el siguiente texto, genera un documento de estudio estructurado con títulos, puntos clave y explicaciones detalladas:\n\n" . $text;

// Configuración de la solicitud a OpenAI
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, 'https://api.openai.com/v1/chat/completions');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $API_KEY
]);

$request_data = [
    'model' => 'gpt-3.5-turbo',
    'messages' => [
        [
            'role' => 'system',
            'content' => 'Eres un asistente educativo experto en crear documentos de estudio estructurados y fáciles de entender.'
        ],
        [
            'role' => 'user',
            'content' => $prompt
        ]
    ],
    'temperature' => 0.7,
    'max_tokens' => 2000
];

curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($request_data));

try {
    $response = curl_exec($ch);
    
    if ($response === false) {
        throw new Exception(curl_error($ch));
    }
    
    $result = json_decode($response, true);
    
    if (isset($result['error'])) {
        throw new Exception($result['error']['message']);
    }
    
    $content = $result['choices'][0]['message']['content'];
    
    echo json_encode([
        'content' => $content
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => 'Error al generar el documento: ' . $e->getMessage()
    ]);
} finally {
    curl_close($ch);
}