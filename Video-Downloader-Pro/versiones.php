<?php

// Función para ejecutar comandos del sistema de manera segura
function ejecutarComando($comando) {
    try {
        $output = shell_exec($comando . ' 2>&1');
        if ($output === null || $output === false) {
            error_log("Error al ejecutar comando: " . $comando);
            return 'Error al ejecutar comando';
        }
        return trim($output);
    } catch (Exception $e) {
        error_log("Excepción al ejecutar comando: " . $comando . " - " . $e->getMessage());
        return 'Error: ' . $e->getMessage();
    }
}

// Función para determinar el comando correcto según el sistema operativo
function getComandoSO() {
    $esWindows = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN';
    return $esWindows ? 'ver' : 'uname -a';
}

// Obtener información del sistema
$info = [];
$timestamp = date('Y-m-d H:i:s');
$info['Timestamp'] = $timestamp;

// Detectar sistema operativo
$esWindows = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN';
$info['Sistema Operativo'] = PHP_OS;
$info['Version SO'] = ejecutarComando(getComandoSO());

// Versión de PHP
$info['PHP'] = PHP_VERSION;
$info['PHP SAPI'] = php_sapi_name();

// Versión de Python
$pythonCmd = $esWindows ? 'python' : '/usr/bin/python3';
$info['Python'] = ejecutarComando($pythonCmd . ' --version');

// Versión de yt-dlp y su ubicación
$ytdlpCmd = $esWindows ? '.\yt-dlp.exe' : './yt-dlp';
if (!file_exists($ytdlpCmd)) {
    $ytdlpCmd = $esWindows ? 'yt-dlp.exe' : 'yt-dlp';
}
$info['yt-dlp'] = ejecutarComando($ytdlpCmd . ' --version');
$info['yt-dlp Path'] = realpath($ytdlpCmd) ?: 'No encontrado';

// Información adicional del sistema
$info['Memoria Límite PHP'] = ini_get('memory_limit');
$info['Max Execution Time'] = ini_get('max_execution_time') . ' segundos';
$info['Directorio Actual'] = getcwd();

// Formatear la información para mostrar
$output = "Información del Sistema\n";
$output .= "=====================\n";
$output .= "Generado: {$info['Timestamp']}\n\n";

// Organizar la información por categorías
$categorias = [
    'Sistema' => ['Sistema Operativo', 'Version SO', 'Directorio Actual'],
    'PHP' => ['PHP', 'PHP SAPI', 'Memoria Límite PHP', 'Max Execution Time'],
    'Herramientas' => ['Python', 'yt-dlp', 'yt-dlp Path']
];

foreach ($categorias as $categoria => $campos) {
    $output .= "\n$categoria:\n" . str_repeat('-', strlen($categoria) + 1) . "\n";
    foreach ($campos as $campo) {
        if (isset($info[$campo])) {
            $output .= sprintf("%-20s: %s\n", $campo, $info[$campo]);
        }
    }
}

// Mostrar en pantalla con estilo
echo "<pre style='background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: monospace;'>";
echo htmlspecialchars($output);
echo "</pre>";

// Guardar en archivo con timestamp
$logFile = 'versiones.txt';
file_put_contents($logFile, $output);

// Registrar en el log si hay errores
foreach ($info as $key => $value) {
    if (strpos(strtolower($value), 'error') !== false) {
        error_log("[{$info['Timestamp']}] Error en $key: $value");
    }
}

?>