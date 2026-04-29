<?php
require_once 'config.php';

// Verificar si el usuario está autenticado
requireLogin();

// Función para obtener el estado de conexión de las redes sociales de un usuario
function getUserSocialConnections($userId) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("SELECT platform, connected, token, token_expiry FROM social_connections WHERE user_id = ?");
        $stmt->execute([$userId]);
        
        $connections = [
            'facebook' => ['connected' => false, 'token' => null, 'expiry' => null],
            'instagram' => ['connected' => false, 'token' => null, 'expiry' => null],
            'twitter' => ['connected' => false, 'token' => null, 'expiry' => null],
            'linkedin' => ['connected' => false, 'token' => null, 'expiry' => null]
        ];
        
        while ($row = $stmt->fetch()) {
            $connections[$row['platform']] = [
                'connected' => (bool)$row['connected'],
                'token' => $row['token'],
                'expiry' => $row['token_expiry']
            ];
        }
        
        return ['success' => true, 'connections' => $connections];
    } catch (PDOException $e) {
        error_log("Error al obtener conexiones sociales: " . $e->getMessage());
        return ['success' => false, 'message' => 'Error al obtener las conexiones'];
    }
}

// Función para actualizar el estado de conexión de una red social
function updateSocialConnection($userId, $platform, $connected, $token = null, $expiry = null) {
    global $pdo;
    
    try {
        // Verificar si ya existe una entrada para esta plataforma y usuario
        $stmt = $pdo->prepare("SELECT id FROM social_connections WHERE user_id = ? AND platform = ?");
        $stmt->execute([$userId, $platform]);
        $exists = $stmt->fetch();
        
        if ($exists) {
            // Actualizar la conexión existente
            $stmt = $pdo->prepare("UPDATE social_connections SET connected = ?, token = ?, token_expiry = ? WHERE user_id = ? AND platform = ?");
            $stmt->execute([$connected ? 1 : 0, $token, $expiry, $userId, $platform]);
        } else {
            // Crear una nueva conexión
            $stmt = $pdo->prepare("INSERT INTO social_connections (user_id, platform, connected, token, token_expiry) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$userId, $platform, $connected ? 1 : 0, $token, $expiry]);
        }
        
        return ['success' => true];
    } catch (PDOException $e) {
        error_log("Error al actualizar conexión social: " . $e->getMessage());
        return ['success' => false, 'message' => 'Error al actualizar la conexión'];
    }
}

// Endpoint para obtener las conexiones sociales del usuario actual
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'get_connections') {
    requireLogin();
    $userId = $_SESSION['user_id'];
    
    $result = getUserSocialConnections($userId);
    header('Content-Type: application/json');
    echo json_encode($result);
    exit;
}

// Endpoint para conectar o desconectar una red social
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'update_connection') {
    requireLogin();
    $userId = $_SESSION['user_id'];
    
    // Validar parámetros
    if (!isset($_POST['platform']) || !in_array($_POST['platform'], ['facebook', 'instagram', 'twitter', 'linkedin'])) {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Plataforma no válida']);
        exit;
    }
    
    $platform = $_POST['platform'];
    $connected = isset($_POST['connected']) ? (bool)$_POST['connected'] : false;
    $token = isset($_POST['token']) ? $_POST['token'] : null;
    $expiry = isset($_POST['expiry']) ? $_POST['expiry'] : null;
    
    $result = updateSocialConnection($userId, $platform, $connected, $token, $expiry);
    header('Content-Type: application/json');
    echo json_encode($result);
    exit;
}

// Función para iniciar el proceso de autenticación con una red social
function initiateOAuthFlow($platform) {
    
    // Constants are defined in config.php, no need to check $social_apis array here
    // We'll check the platform directly in the switch statement.
    
    switch ($platform) {
        case 'facebook':
            $authUrl = 'https://www.facebook.com/v12.0/dialog/oauth?' . http_build_query([
                'client_id' => FACEBOOK_APP_ID,
                'redirect_uri' => FACEBOOK_REDIRECT_URI,
                'state' => ($state = bin2hex(random_bytes(16))), // Generate and store state
                // Define permissions scope if needed, e.g., 'scope' => 'email,public_profile'
                // 'scope' => implode(',', $social_apis['facebook']['permissions']) // Keep if $social_apis is still used for permissions
            ]);
            break;
            
        case 'instagram':
            $authUrl = 'https://api.instagram.com/oauth/authorize?' . http_build_query([
                'client_id' => INSTAGRAM_APP_ID,
                'redirect_uri' => INSTAGRAM_REDIRECT_URI,
                'state' => ($state = bin2hex(random_bytes(16))), // Generate and store state
                // Define scope if needed, e.g., 'scope' => 'user_profile,user_media'
                'response_type' => 'code'
            ]);
            break;
            
        case 'twitter':
            // Twitter usa OAuth 1.0a, que requiere una implementación más compleja
            // En una implementación real, usaríamos una biblioteca como abraham/twitteroauth
            $authUrl = '#'; // Placeholder
            return ['success' => false, 'message' => 'Autenticación de Twitter no implementada en esta versión'];
            break;
            
        case 'linkedin':
            $authUrl = 'https://www.linkedin.com/oauth/v2/authorization?' . http_build_query([
                'response_type' => 'code',
                'client_id' => LINKEDIN_CLIENT_ID,
                'redirect_uri' => LINKEDIN_REDIRECT_URI,
                'state' => ($state = bin2hex(random_bytes(16))), // Generate and store state
                // Define scope if needed, e.g., 'scope' => 'r_liteprofile w_member_social'
                // 'scope' => $social_apis['linkedin']['scope'] // Keep if $social_apis is still used for scope
            ]);
            break;
            
        default:
            return ['success' => false, 'message' => 'Plataforma no soportada'];
    }

    // Store the state in session for later validation
    if (isset($state)) {
        $_SESSION['oauth_state'] = $state;
    }
    
    return ['success' => true, 'auth_url' => $authUrl];
}

// Endpoint para iniciar el flujo de autenticación OAuth
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] === 'oauth_init') {
    requireLogin();
    
    if (!isset($_GET['platform']) || !in_array($_GET['platform'], ['facebook', 'instagram', 'twitter', 'linkedin'])) {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Plataforma no válida']);
        exit;
    }
    
    $platform = $_GET['platform'];
    $result = initiateOAuthFlow($platform);
    
    header('Content-Type: application/json');
    echo json_encode($result);
    exit;
}
?>