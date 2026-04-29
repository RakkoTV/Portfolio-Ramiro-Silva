<?php
require_once 'config.php';

// Este script inserta datos de prueba en la tabla users
// Solo ejecutar si la tabla está vacía o se necesitan datos de prueba

try {
    // Verificar si ya existen usuarios en la tabla
    $checkStmt = $pdo->query("SELECT COUNT(*) FROM users");
    $userCount = $checkStmt->fetchColumn();
    
    if ($userCount > 0) {
        echo "<p>Ya existen usuarios en la base de datos. No se insertarán datos de prueba.</p>";
    } else {
        // Insertar usuarios de prueba
        $users = [
            [
                'first_name' => 'Carlos',
                'last_name' => 'Rodríguez',
                'email' => 'carlos@ejemplo.com',
                'password' => password_hash('password123', PASSWORD_DEFAULT),
                'plan' => 'Plan Premium',
                'profile_image' => ''
            ],
            [
                'first_name' => 'María',
                'last_name' => 'González',
                'email' => 'maria@ejemplo.com',
                'password' => password_hash('password123', PASSWORD_DEFAULT),
                'plan' => 'Plan Profesional',
                'profile_image' => ''
            ],
            [
                'first_name' => 'Alejandro',
                'last_name' => 'López',
                'email' => 'alejandro@ejemplo.com',
                'password' => password_hash('password123', PASSWORD_DEFAULT),
                'plan' => 'Plan Básico',
                'profile_image' => ''
            ]
        ];
        
        $stmt = $pdo->prepare("INSERT INTO users (first_name, last_name, email, password, plan, profile_image, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())");
        
        foreach ($users as $user) {
            $stmt->execute([
                $user['first_name'],
                $user['last_name'],
                $user['email'],
                $user['password'],
                $user['plan'],
                $user['profile_image']
            ]);
        }
        
        echo "<p>Datos de prueba insertados correctamente.</p>";
        echo "<p>Usuarios creados:</p>";
        echo "<ul>";
        foreach ($users as $user) {
            echo "<li>{$user['first_name']} {$user['last_name']} - {$user['email']} - {$user['plan']}</li>";
        }
        echo "</ul>";
    }
    
    echo "<p><a href='../login.html'>Ir a la página de login</a></p>";
    
} catch (PDOException $e) {
    echo "<p>Error al insertar datos de prueba: " . $e->getMessage() . "</p>";
}