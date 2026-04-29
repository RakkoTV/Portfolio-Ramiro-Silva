<?php
session_start(); // Asegurar que la sesión esté iniciada
require_once 'config.php';

// Verificar si el usuario está autenticado
if (!isset($_SESSION['user_id'])) {
    // Si no hay sesión, devolver datos de ejemplo
    echo json_encode([
        'success' => false,
        'message' => 'Usuario no autenticado',
        'data' => [
            'first_name' => 'Invitado',
            'last_name' => '',
            'plan' => 'Básico',
            'profile_image' => ''
        ]
    ]);
    exit;
}

// Obtener datos del usuario actual desde la base de datos
try {
    $userId = $_SESSION['user_id'];
    $stmt = $pdo->prepare("SELECT first_name, last_name, plan, profile_image FROM users WHERE id = ?");
    $stmt->execute([$userId]);
    
    $userData = $stmt->fetch();
    
    if ($userData) {
        // Generar iniciales para el avatar si no hay imagen de perfil
        $initials = strtoupper(substr($userData['first_name'], 0, 1) . substr($userData['last_name'], 0, 1));
        
        echo json_encode([
            'success' => true,
            'data' => [
                'first_name' => $userData['first_name'],
                'last_name' => $userData['last_name'],
                'plan' => $userData['plan'],
                'profile_image' => $userData['profile_image'],
                'initials' => $initials
            ]
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Usuario no encontrado'
        ]);
    }
} catch (PDOException $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Error al obtener datos: ' . $e->getMessage()
    ]);
}