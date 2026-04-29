<?php
require_once 'config.php';

// Verificar si el usuario está autenticado
requireLogin();

// Procesar la respuesta de autenticación OAuth
if (isset($_GET['platform']) && isset($_GET['code']) && isset($_GET['state'])) {
    // Validate state parameter for CSRF protection
    if (!isset($_SESSION['oauth_state']) || $_SESSION['oauth_state'] !== $_GET['state']) {
        // State mismatch or missing - potential CSRF attack
        unset($_SESSION['oauth_state']); // Clear potentially compromised state
        error_log('OAuth State mismatch. Session: ' . ($_SESSION['oauth_state'] ?? 'Not set') . ', GET: ' . $_GET['state']);
        header('Location: ../configuracion.html?error=csrf');
        exit;
    }
    // State is valid, clear it from session
    unset($_SESSION['oauth_state']);
    $platform = $_GET['platform'];
    $code = $_GET['code'];
    $userId = $_SESSION['user_id'];
    
    // Configuración de OAuth para cada plataforma
    // Token URLs (can also be defined as constants in config.php if preferred)
    $tokenUrls = [
        'facebook' => 'https://graph.facebook.com/v12.0/oauth/access_token',
        'instagram' => 'https://api.instagram.com/oauth/access_token',
        'twitter' => 'https://api.twitter.com/2/oauth2/token', // Note: Twitter OAuth flow might differ
        'linkedin' => 'https://www.linkedin.com/oauth/v2/accessToken'
    ];
    
    // Use constants directly based on the platform
    $clientId = null;
    $clientSecret = null;
    $redirectUri = null;
    $tokenUrl = isset($tokenUrls[$platform]) ? $tokenUrls[$platform] : null;

    switch ($platform) {
        case 'facebook':
            $clientId = FACEBOOK_APP_ID;
            $clientSecret = FACEBOOK_APP_SECRET;
            $redirectUri = FACEBOOK_REDIRECT_URI;
            break;
        case 'instagram':
            $clientId = INSTAGRAM_APP_ID;
            $clientSecret = INSTAGRAM_APP_SECRET;
            $redirectUri = INSTAGRAM_REDIRECT_URI;
            break;
        case 'twitter':
            $clientId = TWITTER_API_KEY;
            $clientSecret = TWITTER_API_SECRET;
            $redirectUri = TWITTER_REDIRECT_URI;
            // Note: Twitter OAuth might require different grant_type or parameters
            break;
        case 'linkedin':
            $clientId = LINKEDIN_CLIENT_ID;
            $clientSecret = LINKEDIN_CLIENT_SECRET;
            $redirectUri = LINKEDIN_REDIRECT_URI;
            break;
    }

    if ($clientId && $clientSecret && $redirectUri && $tokenUrl) {
        // Intercambiar el código de autorización por un token de acceso
        $postData = [
            'client_id' => $clientId,
            'client_secret' => $clientSecret,
            'code' => $code,
            'redirect_uri' => $redirectUri,
            'grant_type' => 'authorization_code'
        ];

        // Configurar la solicitud cURL
        $ch = curl_init($tokenUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        
        // Ajustar los parámetros según la plataforma
        if ($platform === 'instagram') {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
        } else {
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postData));
            curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/x-www-form-urlencoded']);
        }
        
        // Ejecutar la solicitud
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200) {
            $tokenData = json_decode($response, true);
            
            if (isset($tokenData['access_token'])) {
                $accessToken = $tokenData['access_token'];
                $expiresIn = isset($tokenData['expires_in']) ? $tokenData['expires_in'] : 3600;
                
                // Calcular la fecha de expiración
                $expiryDate = date('Y-m-d H:i:s', time() + $expiresIn);
                
                try {
                    // Verificar si ya existe una conexión para esta plataforma
                    $stmt = $pdo->prepare("SELECT id FROM social_connections WHERE user_id = ? AND platform = ?");
                    $stmt->execute([$userId, $platform]);
                    $existingConnection = $stmt->fetch(PDO::FETCH_ASSOC);
                    
                    if ($existingConnection) {
                        // Actualizar la conexión existente
                        $stmt = $pdo->prepare("UPDATE social_connections SET connected = 1, token = ?, token_expiry = ? WHERE user_id = ? AND platform = ?");
                        $stmt->execute([$accessToken, $expiryDate, $userId, $platform]);
                    } else {
                        // Crear una nueva conexión
                        $stmt = $pdo->prepare("INSERT INTO social_connections (user_id, platform, connected, token, token_expiry) VALUES (?, ?, 1, ?, ?)");
                        $stmt->execute([$userId, $platform, $accessToken, $expiryDate]);
                    }
                    
                    // Redirigir a la página de configuración con un mensaje de éxito
                    header('Location: ../configuracion.html?success=1&platform=' . $platform);
                    exit;
                } catch (PDOException $e) {
                    error_log('Error al guardar token: ' . $e->getMessage());
                    // Redirigir con error
                    header('Location: ../configuracion.html?error=db&platform=' . $platform);
                    exit;
                }
            } else {
                error_log('Token no encontrado en la respuesta: ' . $response);
                // Redirigir con error
                header('Location: ../configuracion.html?error=token&platform=' . $platform);
                exit;
            }
        } else {
            error_log('Error al obtener token. Código HTTP: ' . $httpCode . '. Respuesta: ' . $response);
            // Redirigir con error
            header('Location: ../configuracion.html?error=http&platform=' . $platform);
            exit;
        }
    } else {
        // Plataforma no válida
        header('Location: ../configuracion.html?error=platform');
        exit;
    }
} else {
    // Parámetros faltantes (code, platform, or state)
    // Clear state if it exists but other params are missing
    if (isset($_SESSION['oauth_state'])) {
        unset($_SESSION['oauth_state']);
    }
    error_log('OAuth callback missing parameters. GET: ' . print_r($_GET, true));
    header('Location: ../configuracion.html?error=params');
    exit;
}