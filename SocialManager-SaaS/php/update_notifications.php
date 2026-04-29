<?php
require_once 'config.php';

// Verificar si el usuario está autenticado
requireLogin();

// Procesar la actualización de preferencias de notificaciones
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $userId = $_SESSION['user_id'];
    
    // Obtener las preferencias de notificaciones
    $emailNotifications = isset($_POST['email_notifications']) ? $_POST['email_notifications'] : [];
    $pushNotifications = isset($_POST['push_notifications']) ? $_POST['push_notifications'] : [];
    
    // Crear un array con las preferencias
    $notificationSettings = [
        'email' => [
            'comments' => in_array('comments', $emailNotifications),
            'messages' => in_array('messages', $emailNotifications),
            'followers' => in_array('followers', $emailNotifications),
            'analytics' => in_array('analytics', $emailNotifications)
        ],
        'push' => [
            'comments' => in_array('comments', $pushNotifications),
            'messages' => in_array('messages', $pushNotifications),
            'followers' => in_array('followers', $pushNotifications),
            'analytics' => in_array('analytics', $pushNotifications)
        ]
    ];
    
    try {
        // Verificar si ya existen configuraciones para este usuario
        $stmt = $pdo->prepare("SELECT id FROM user_settings WHERE user_id = ? AND setting_type = 'notifications'");
        $stmt->execute([$userId]);
        $exists = $stmt->fetch();
        
        // Convertir el array de configuraciones a JSON
        $settingsJson = json_encode($notificationSettings);
        
        if ($exists) {
            // Actualizar las configuraciones existentes
            $stmt = $pdo->prepare("UPDATE user_settings SET settings_value = ? WHERE user_id = ? AND setting_type = 'notifications'");
            $stmt->execute([$settingsJson, $userId]);
        } else {
            // Crear nuevas configuraciones
            $stmt = $pdo->prepare("INSERT INTO user_settings (user_id, setting_type, settings_value) VALUES (?, 'notifications', ?)");
            $stmt->execute([$userId, $settingsJson]);
        }
        
        // Responder con éxito
        header('Content-Type: application/json');
        echo json_encode(['success' => true]);
    } catch (PDOException $e) {
        // Registrar el error y responder con error
        error_log("Error al guardar preferencias de notificaciones: " . $e->getMessage());
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Error al guardar las preferencias']);
    }
} else {
    // Método no permitido
    header('HTTP/1.1 405 Method Not Allowed');
    header('Content-Type: application/json');
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
}
?>