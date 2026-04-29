<?php

require_once 'config.php';
require_once 'translations.php';

if (!isset($_POST['name']) || !isset($_POST['language'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing name or language']);
    exit;
}

$name = $_POST['name'];
$language = $_POST['language'];
$t = $translations[$language] ?? $translations['EN'];

function callGeminiAPI($apiKey, $prompt, $schema) {
    $data = [
        'contents' => [['parts' => [['text' => $prompt]]]],
        'generationConfig' => [
            'response_mime_type' => 'application/json',
            'response_schema' => $schema,
            'temperature' => 0.9,
        ],
    ];

    $ch = curl_init('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' . $apiKey);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpcode != 200) {
        error_log("Gemini text API error: HTTP {$httpcode} " . $response);
        return null;
    }

    $responseData = json_decode($response, true);
    return json_decode($responseData['candidates'][0]['content']['parts'][0]['text'], true);
}

function callImagenAPI($apiKey, $projectId, $projectRegion, $prompt) {
    $url = "https://{$projectRegion}-aiplatform.googleapis.com/v1/projects/{$projectId}/locations/{$projectRegion}/publishers/google/models/imagegeneration:predict";

    $data = [
        'instances' => [
            [
                'prompt' => $prompt
            ]
        ],
        'parameters' => [
            'sampleCount' => 1
        ]
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $apiKey,
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpcode != 200) {
        error_log("Vertex AI image API error: HTTP {$httpcode} " . $response);
        return null;
    }

    $responseData = json_decode($response, true);
    return $responseData['predictions'][0]['bytesBase64Encoded'] ?? null;
}


$characterSchema = [
    'type' => 'OBJECT',
    'properties' => [
        'backstory' => [
            'type' => 'STRING',
            'description' => 'A compelling and detailed backstory for the character, fitting a sci-fi or fantasy video game setting. Should be 2-3 paragraphs.',
        ],
        'abilities' => [
            'type' => 'ARRAY',
            'description' => 'A list of 3-4 unique and creative abilities for the character.',
            'items' => [
                'type' => 'OBJECT',
                'properties' => [
                    'name' => ['type' => 'STRING'],
                    'description' => ['type' => 'STRING'],
                ],
                'required' => ['name', 'description'],
            ],
        ],
    ],
    'required' => ['backstory', 'abilities'],
];

$details = callGeminiAPI($apiKey, "Create a unique video game character concept named \"$name\". The character should exist in a universe blending science fiction and high fantasy. Provide a rich backstory and a list of unique abilities. IMPORTANT: Generate the entire response (backstory, ability names, and ability descriptions) in {$t['languageName']}.", $characterSchema);

if (!$details) {
    http_response_code(500);
    echo json_encode(['error' => $t['errorDefault']]);
    exit;
}

// Generate the image using Vertex AI
$projectId = 'gen-lang-client-0528690123'; // <-- IMPORTANT: REPLACE THIS
$projectRegion = 'us-central1'; // <-- IMPORTANT: VERIFY THIS IS CORRECT

$portraitPrompt = "Sci-fi fantasy concept art, highly detailed digital painting of a character named {$name}. " . substr($details['backstory'], 0, 150) . ". Epic, cinematic, intricate details.";
$imageBase64 = callImagenAPI($vertexApiKey, $projectId, $projectRegion, $portraitPrompt);

$portraitUrl = $imageBase64 
    ? 'data:image/jpeg;base64,' . $imageBase64 
    : 'https://placehold.co/512x768.png?text=' . urlencode($name . ' (Image Gen Failed)');

$characterData = [
    'name' => $name,
    'backstory' => $details['backstory'],
    'abilities' => $details['abilities'],
    'portraitUrl' => $portraitUrl,
];

header('Content-Type: application/json');
echo json_encode($characterData);
