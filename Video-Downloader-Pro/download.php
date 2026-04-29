<?php
header('Content-Type: application/json; charset=utf-8');

if (!defined('TESTING')) {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        http_response_code(405);
        die(json_encode(['error' => 'Método no permitido']));
    }
}

// Configurar el log de errores
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/downloader.log');

function executeDownloader($url) {
    $ytdlp_path = __DIR__ . DIRECTORY_SEPARATOR . 'yt-dlp';
    if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
        $ytdlp_path .= '.exe';
    }

    // Verificar si la URL es válida
    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        return ['error' => 'URL inválida'];
    }

    // Verificar que existe el ejecutable
    if (!file_exists($ytdlp_path)) {
        error_log("[ERROR] yt-dlp no encontrado en: " . $ytdlp_path);
        return ['error' => 'yt-dlp no encontrado'];
    }

    // Preparar el comando con parámetros optimizados
    $command = sprintf('"%s" --config-location "%s/temp_ytdlp.conf" --print "%%%(title)s" --print "%%%(duration)s" --print "%%%(thumbnail)s" --print "%%%(url)s" --print "%%%(ext)s" "%s" 2>&1',
        $ytdlp_path,
        __DIR__,
        $url
    );

    // Ejecutar el comando
    $output = [];
    $return_var = 0;
    exec($command . ' 2>&1', $output, $return_var);

    // Verificar si hubo errores
    if ($return_var !== 0) {
        $error_msg = implode("\n", $output);
        $timestamp = date('Y-m-d H:i:s');
        error_log("[$timestamp] Error al ejecutar yt-dlp para URL: $url\n" . $error_msg);
        
        // Verificar si es un error de bot detection
        if (strpos($error_msg, 'Sign in to confirm you\'re not a bot') !== false) {
            return ['error' => 'YouTube requiere verificación. Por favor, inténtelo de nuevo más tarde.'];
        }
        
        return ['error' => 'Error al procesar el video. Por favor, inténtelo de nuevo más tarde.'];
    }

    // Procesar la salida
    if (count($output) >= 5) {
        return [
            'title' => $output[0],
            'duration' => intval($output[1]),
            'thumbnail' => $output[2],
            'video_url' => $output[3],
            'ext' => $output[4]
        ];
    }

    return ['error' => 'No se pudo obtener la información del video'];
}

if (!defined('TESTING')) {
    // Obtener datos de la solicitud
    $data = json_decode(file_get_contents('php://input'), true);
    $url = isset($data['url']) ? $data['url'] : '';

    // Ejecutar el descargador y devolver resultado
    $result = executeDownloader($url);
    echo json_encode($result);
}