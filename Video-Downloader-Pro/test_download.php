<?php
define('TESTING', true);
require_once 'download.php';

// Configurar cabeceras para mostrar texto plano
header('Content-Type: text/plain; charset=utf-8');

// Iniciar buffer de salida
ob_start();

// Verificar que yt-dlp esté disponible
$ytdlp_path = __DIR__ . DIRECTORY_SEPARATOR . 'yt-dlp';
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    $ytdlp_path .= '.exe';
}

if (!file_exists($ytdlp_path)) {
    die("Error: yt-dlp no encontrado en: " . $ytdlp_path);
}

// Crear directorio de descargas si no existe
$downloadDir = __DIR__ . DIRECTORY_SEPARATOR . 'downloads';
if (!file_exists($downloadDir)) {
    mkdir($downloadDir, 0777, true);
}

// URL de prueba
$testUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';

try {
    // Verificar permisos de ejecución en Linux
    if (strtoupper(substr(PHP_OS, 0, 3)) !== 'WIN' && !is_executable($ytdlp_path)) {
        chmod($ytdlp_path, 0755);
    }

    // Configurar el entorno para yt-dlp
    putenv("HOME=" . __DIR__);
    putenv("LANG=es_ES.UTF-8");
    
    // Ejecutar el descargador con configuración mejorada
    echo "Iniciando descarga del video...\n";
    echo "Usando yt-dlp en: " . $ytdlp_path . "\n";
    
    // Crear archivo de configuración temporal
    $tempConfigFile = __DIR__ . '/temp_ytdlp.conf';
    $configContent = "--no-warnings\n--ignore-errors\n--no-check-certificate\n--format bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best\n--socket-timeout 180\n--force-ipv4\n--geo-bypass\n--no-cookies\n--no-cache-dir\n--no-progress\n--add-header \"User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36\"\n--add-header \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\"\n--add-header \"Accept-Language: es-ES,es;q=0.9,en;q=0.8\"\n--extractor-retries 5\n--fragment-retries 5\n--retry-sleep 5\n--throttled-rate 100K\n--buffer-size 16K\n--max-filesize 2G\n--max-downloads 1\n--abort-on-error";
    
    // Configurar timeout de PHP
    set_time_limit(300); // 5 minutos

    file_put_contents($tempConfigFile, $configContent);
    
    // Ejecutar con la nueva configuración
    putenv("YTDLP_CONFIG_FILE=" . $tempConfigFile);
    $result = executeDownloader($testUrl);
    
    // Limpiar archivo temporal
    if (file_exists($tempConfigFile)) {
        unlink($tempConfigFile);}

    if (isset($result['error'])) {
        throw new Exception($result['error']);
    }

    if (isset($result['video_url']) && isset($result['title'])) {
        $videoUrl = $result['video_url'];
        $fileName = preg_replace('/[^\w\s-]/', '', $result['title']) . '.' . $result['ext'];
        $filePath = $downloadDir . '/' . $fileName;

        echo "\nInformación del video:\n";
        echo "Título: " . $result['title'] . "\n";
        echo "Duración: " . $result['duration'] . " segundos\n";
        echo "Miniatura: " . $result['thumbnail'] . "\n";
        echo "\nRuta de descarga: " . realpath($filePath) . "\n";
        
        // Descargar el archivo
        echo "\nIniciando descarga del video...\n";
        echo "Descargando video a: " . $filePath . "\n";
        $fp = fopen($filePath, 'w');
        
        $ch = curl_init($videoUrl);
        curl_setopt($ch, CURLOPT_FILE, $fp);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_NOPROGRESS, false);
        curl_setopt($ch, CURLOPT_TIMEOUT, 300);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
        curl_setopt($ch, CURLOPT_BUFFERSIZE, 16384);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_PROGRESSFUNCTION, function($resource, $downloadSize, $downloaded) {
            static $lastOutput = 0;
            $currentTime = time();
            if ($downloadSize > 0 && ($currentTime - $lastOutput) >= 1) {
                $percent = round($downloaded / $downloadSize * 100, 1);
                $speed = $downloaded > 0 ? round($downloaded / ($currentTime - $lastOutput) / 1024, 2) : 0;
                echo "\rProgreso: {$percent}% ({$downloaded}/{$downloadSize} bytes) - {$speed} KB/s";
                $lastOutput = $currentTime;
            }
        });

        $success = curl_exec($ch);
        if ($success) {
            echo "\n\nDescarga completada exitosamente!\n";
            echo "Archivo guardado en: " . realpath($filePath) . "\n";
        } else {
            throw new Exception(curl_error($ch));
        }

        curl_close($ch);
        fclose($fp);
    } else {
        throw new Exception("No se pudo obtener la información del video");
    }

} catch (Exception $e) {
    echo "\nError: " . $e->getMessage() . "\n";
}

// Mostrar el registro para depuración
echo "\nRegistro de depuración:\n";
echo file_get_contents(__DIR__ . '/downloader.log');

// Obtener contenido del buffer y guardarlo en error_download.txt
$output = ob_get_contents();
ob_end_flush(); // Mostrar en pantalla

// Guardar en archivo con marca de tiempo
$timestamp = date('[Y-m-d H:i:s] ');
file_put_contents(__DIR__ . '/error_download.txt', $timestamp . $output, FILE_APPEND);