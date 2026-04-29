<?php
// Configuración
ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);
ini_set('memory_limit', '256M');

// Función para registrar actividad
function logActivity($message, $type = 'INFO') {
    $logFile = __DIR__ . '/downloads.log';
    $timestamp = date('Y-m-d H:i:s');
    $logMessage = "[$timestamp][$type] $message\n";
    error_log($logMessage, 3, $logFile);
}

// Función para enviar respuesta de error
function sendError($message, $code = 400) {
    logActivity($message, 'ERROR');
    http_response_code($code);
    header('Content-Type: text/plain; charset=utf-8');
    echo $message;
    exit;
}

// Verificar si se proporcionó un nombre de archivo
if (!isset($_GET['file'])) {
    sendError('Archivo no especificado');
}

// Validar y sanitizar el nombre del archivo
$filename = basename(trim($_GET['file']));
if (empty($filename) || strlen($filename) > 255) {
    sendError('Nombre de archivo inválido');
}

// Prevenir directory traversal y caracteres no permitidos
if (preg_match('/[\/\\]|\.\.|[<>:"\|\?\*]/', $filename)) {
    logActivity("Intento de directory traversal detectado: {$filename}", 'WARNING');
    sendError('Nombre de archivo no permitido', 403);
}

$filepath = sys_get_temp_dir() . DIRECTORY_SEPARATOR . $filename;

// Verificar si el archivo existe y es legible
if (!file_exists($filepath) || !is_readable($filepath)) {
    sendError('Archivo no encontrado o no accesible', 404);
}

// Verificar si el archivo es temporal y reciente (menos de 1 hora)
if (time() - filemtime($filepath) > 3600) {
    if (file_exists($filepath)) {
        unlink($filepath); // Eliminar archivo antiguo
        logActivity("Archivo expirado eliminado: {$filename}");
    }
    sendError('El enlace de descarga ha expirado', 410);
}

// Obtener el tipo MIME del archivo de forma segura
$finfo = finfo_open(FILEINFO_MIME_TYPE);
if ($finfo === false) {
    sendError('Error al determinar el tipo de archivo', 500);
}
$mime_type = finfo_file($finfo, $filepath) ?: 'application/octet-stream';
finfo_close($finfo);

// Configurar cabeceras para la descarga
header('Content-Type: ' . $mime_type);
header('Content-Disposition: attachment; filename="' . $filename . '"; filename*=UTF-8\'\''. rawurlencode($filename));
header('Content-Length: ' . filesize($filepath));
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');
header('Expires: 0');

// Registrar la descarga
logActivity("Iniciando descarga: {$filename}");

// Enviar archivo de forma optimizada
$handle = fopen($filepath, 'rb');
if ($handle === false) {
    sendError('Error al abrir el archivo', 500);
}

while (!feof($handle)) {
    $buffer = fread($handle, 8192);
    if ($buffer === false) {
        fclose($handle);
        sendError('Error al leer el archivo', 500);
    }
    echo $buffer;
    flush();
}

fclose($handle);

// Eliminar archivo temporal después de la descarga
if (file_exists($filepath)) {
    unlink($filepath);
    logActivity("Archivo temporal eliminado: {$filename}");
}