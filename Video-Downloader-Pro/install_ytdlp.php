<?php
// Configuración inicial
ini_set('display_errors', 1);
ini_set('error_reporting', E_ALL);

// Función para registrar actividad
function logActivity($message, $type = 'INFO') {
    $logFile = __DIR__ . '/ytdlp_install.log';
    $timestamp = date('Y-m-d H:i:s');
    $logMessage = "[$timestamp][$type] $message\n";
    error_log($logMessage, 3, $logFile);
}

// Función para verificar si yt-dlp está instalado
function isYtDlpInstalled() {
    $ytdlpPath = __DIR__ . '/yt-dlp';
    if (!file_exists($ytdlpPath)) {
        logActivity('yt-dlp no encontrado', 'ERROR');
        return false;
    }
    if (!is_readable($ytdlpPath)) {
        logActivity('yt-dlp no tiene permisos de lectura', 'ERROR');
        return false;
    }
    return true;
}

// Función para descargar yt-dlp
function downloadYtDlp() {
    $ytdlpUrl = 'https://github.com/yt-dlp/yt-dlp/releases/download/2022.01.21/yt-dlp';
    $targetPath = __DIR__ . '/yt-dlp';
    
    logActivity('Iniciando descarga de yt-dlp');
    
    $ch = curl_init($ytdlpUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
    
    $data = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if (curl_errno($ch)) {
        logActivity('Error al descargar yt-dlp: ' . curl_error($ch), 'ERROR');
        curl_close($ch);
        return false;
    }
    
    curl_close($ch);
    
    if ($httpCode !== 200) {
        logActivity("Error HTTP al descargar yt-dlp: $httpCode", 'ERROR');
        return false;
    }
    
    if (file_put_contents($targetPath, $data) === false) {
        logActivity('Error al guardar yt-dlp', 'ERROR');
        return false;
    }

    // Verificar el tamaño del archivo
    $fileSize = filesize($targetPath);
    if ($fileSize < 1000000) { // El archivo debe ser mayor a 1MB
        logActivity('El archivo descargado es demasiado pequeño', 'ERROR');
        unlink($targetPath);
        return false;
    }

    // Establecer permisos de ejecución
    if (!chmod($targetPath, 0755)) {
        logActivity('Error al establecer permisos de ejecución', 'ERROR');
        return false;
    }
    
    logActivity('yt-dlp descargado exitosamente');
    return true;
}

// Función principal de instalación
function installYtDlp() {
    header('Content-Type: application/json; charset=utf-8');
    
    if (isYtDlpInstalled()) {
        echo json_encode([
            'success' => true,
            'message' => 'yt-dlp ya está instalado en el sistema'
        ]);
        return;
    }
    
    if (!downloadYtDlp()) {
        echo json_encode([
            'success' => false,
            'message' => 'Error al descargar e instalar yt-dlp'
        ]);
        return;
    }
    
    // Verificar la instalación
    if (isYtDlpInstalled()) {
        logActivity('Instalación de yt-dlp completada exitosamente');
        echo json_encode([
            'success' => true,
            'message' => 'yt-dlp ha sido instalado correctamente'
        ]);
    } else {
        logActivity('La instalación de yt-dlp falló en la verificación final', 'ERROR');
        echo json_encode([
            'success' => false,
            'message' => 'Error en la verificación final de la instalación'
        ]);
    }
}

// Ejecutar la instalación
installYtDlp();