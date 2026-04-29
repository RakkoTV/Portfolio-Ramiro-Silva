<?php
// Incluir el archivo de configuración
require_once 'config.php';

// Verificar si la conexión fue exitosa
if (isset($pdo)) {
    echo "<h2>Conexión a la base de datos exitosa</h2>";
    
    // Mostrar información de la base de datos
    echo "<h3>Información de la conexión:</h3>";
    echo "<ul>";
    echo "<li>Servidor: {$host}</li>";
    echo "<li>Base de datos: {$dbname}</li>";
    echo "<li>Usuario: {$username}</li>";
    echo "</ul>";
    
    // Obtener información de las tablas
    try {
        $stmt = $pdo->query("SHOW TABLES");
        $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
        
        echo "<h3>Tablas en la base de datos:</h3>";
        echo "<ul>";
        foreach ($tables as $table) {
            echo "<li>{$table}</li>";
        }
        echo "</ul>";
        
        // Mostrar cantidad de registros en la tabla users
        $stmt = $pdo->query("SELECT COUNT(*) as total FROM users");
        $userCount = $stmt->fetch();
        echo "<h3>Estadísticas:</h3>";
        echo "<ul>";
        echo "<li>Total de usuarios: {$userCount['total']}</li>";
        echo "</ul>";
        
    } catch (PDOException $e) {
        echo "<p>Error al consultar la base de datos: " . $e->getMessage() . "</p>";
    }
} else {
    echo "<h2>Error: No se pudo establecer la conexión a la base de datos</h2>";
}
?>

<style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 20px;
        color: #333;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    h3 {
        color: #2980b9;
        margin-top: 20px;
    }
    ul {
        background-color: #f9f9f9;
        padding: 15px 15px 15px 40px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
    }
    li {
        margin-bottom: 8px;
    }
</style>