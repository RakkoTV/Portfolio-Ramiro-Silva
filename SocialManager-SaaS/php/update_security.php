<?php
require_once 'config.php';

// Verificar si el usuario está autenticado
requireLogin();

// Procesar la actualización de configuración de seguridad
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $userId = $_SESSION['user_id'];
    
    // Cambio de contraseña
    if (isset($_POST['current_password']) && isset($_POST['new_password']) && isset($_POST['confirm_password'])) {
        $currentPassword = $_POST['current_password'];
        $newPassword = $_POST['new_password'];
        $confirmPassword = $_POST['confirm_password'];
        
        // Validar que la nueva contraseña y la confirmación coincidan
        if ($newPassword !== $confirmPassword) {
            header('Content-Type: application/json');
            echo json_encode(['success' => false, 'message' => 'La nueva contraseña y la confirmación no coinciden']);
            exit;
        }
        
        try {
            // Verificar la contraseña actual
            $stmt = $pdo->prepare("SELECT password FROM users WHERE id = ?");
            $stmt->execute([$userId]);
            $user = $stmt->fetch();
            
            if (!$user || !password_verify($currentPassword, $user['password'])) {
                header('Content-Type: application/json');
                echo json_encode(['success' => false, 'message' => 'La contraseña actual es incorrecta']);
                exit;
            }
            
            // Actualizar la contraseña
            $hashedPassword = password_hash($newPassword, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("UPDATE users SET password = ? WHERE id = ?");
            $stmt->execute([$hashedPassword, $userId]);
            
            // Responder con éxito
            header('Content-Type: application/json');
            echo json_encode(['success' => true, 'message' => 'Contraseña actualizada correctamente']);
            exit;
        } catch (PDOException $e) {
            // Registrar el error y responder con error
            error_log("Error al actualizar contraseña: " . $e->getMessage());
            header('Content-Type: application/json');
            echo json_encode(['success' => false, 'message' => 'Error al actualizar la contraseña']);
            exit;
        }
    }
    
    // Verificación en dos pasos
    if (isset($_POST['two_factor_auth'])) {
        $twoFactorEnabled = (bool)$_POST['two_factor_auth'];
        
        try {
            // Actualizar la configuración de verificación en dos pasos
            $stmt = $pdo->prepare("UPDATE users SET two_factor_enabled = ? WHERE id = ?");
            $stmt->execute([$twoFactorEnabled ? 1 : 0, $userId]);
            
            // Responder con éxito
            header('Content-Type: application/json');
            echo json_encode(['success' => true, 'message' => 'Configuración de verificación en dos pasos actualizada']);
            exit;
        } catch (PDOException $e) {
            // Registrar el error y responder con error
            error_log("Error al actualizar verificación en dos pasos: " . $e->getMessage());
            header('Content-Type: application/json');
            echo json_encode(['success' => false, 'message' => 'Error al actualizar la configuración de verificación en dos pasos']);
            exit;
        }
    }
    
    // Cerrar sesión remota
    if (isset($_POST['session_id'])) {
        $sessionId = $_POST['session_id'];
        
        try {
            // Eliminar la sesión especificada
            $stmt = $pdo->prepare("DELETE FROM user_sessions WHERE id = ? AND user_id = ?");
            $stmt->execute([$sessionId, $userId]);
            
            // Responder con éxito
            header('Content-Type: application/json');
            echo json_encode(['success' => true, 'message' => 'Sesión cerrada correctamente']);
            exit;
        } catch (PDOException $e) {
            // Registrar el error y responder con error
            error_log("Error al cerrar sesión remota: " . $e->getMessage());
            header('Content-Type: application/json');
            echo json_encode(['success' => false, 'message' => 'Error al cerrar la sesión']);
            exit;
        }
    }
    
    // Si llegamos aquí, no se ha procesado ninguna acción
    header('Content-Type: application/json');
    echo json_encode(['success' => false, 'message' => 'No se ha especificado ninguna acción']);
} else {
    // Método no permitido
    header('HTTP/1.1 405 Method Not Allowed');
    header('Content-Type: application/json');
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
}
?>