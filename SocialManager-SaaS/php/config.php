<?php
// Configuración de la base de datos
$host = '144.76.113.199';
$dbname = 'rakkotech_socialmanager';
$username = 'rakkotech_sm';
$password = '4&uV0dwdR^Vv';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    // Configurar el modo de error PDO a excepción
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    // Configurar el modo de recuperación por defecto a objeto
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch(PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}

// Define SITE_URL (replace with your actual URL)
define('SITE_URL', 'http://localhost/WEBS/17'); // Example: Adjust as needed

// Configuración de APIs de redes sociales - IMPORTANT: Replace placeholders with your actual credentials
define('FACEBOOK_APP_ID', 'YOUR_FACEBOOK_APP_ID');
define('FACEBOOK_APP_SECRET', 'YOUR_FACEBOOK_APP_SECRET');
define('FACEBOOK_REDIRECT_URI', SITE_URL . '/php/oauth_callback.php?platform=facebook');

define('INSTAGRAM_APP_ID', 'YOUR_INSTAGRAM_APP_ID');
define('INSTAGRAM_APP_SECRET', 'YOUR_INSTAGRAM_APP_SECRET');
define('INSTAGRAM_REDIRECT_URI', SITE_URL . '/php/oauth_callback.php?platform=instagram');

define('TWITTER_API_KEY', 'YOUR_TWITTER_API_KEY'); // Also known as Consumer Key
define('TWITTER_API_SECRET', 'YOUR_TWITTER_API_SECRET'); // Also known as Consumer Secret
define('TWITTER_REDIRECT_URI', SITE_URL . '/php/oauth_callback.php?platform=twitter'); // Note: Twitter OAuth 1.0a/2.0 flow might differ

define('LINKEDIN_CLIENT_ID', 'YOUR_LINKEDIN_CLIENT_ID');
define('LINKEDIN_CLIENT_SECRET', 'YOUR_LINKEDIN_CLIENT_SECRET');
define('LINKEDIN_REDIRECT_URI', SITE_URL . '/php/oauth_callback.php?platform=linkedin');

// You can keep the array for reference or remove it if using constants directly
$social_apis = [
    'facebook' => [
        'app_id' => 'YOUR_FACEBOOK_APP_ID',
        'app_secret' => 'YOUR_FACEBOOK_APP_SECRET',
        'redirect_uri' => FACEBOOK_REDIRECT_URI,
        'permissions' => ['pages_show_list', 'pages_read_engagement', 'pages_manage_posts']
    ],
    'instagram' => [
        'client_id' => 'YOUR_INSTAGRAM_CLIENT_ID',
        'client_secret' => 'YOUR_INSTAGRAM_CLIENT_SECRET',
        'redirect_uri' => INSTAGRAM_REDIRECT_URI,
        'scope' => 'user_profile,user_media'
    ],
    'twitter' => [
        'consumer_key' => TWITTER_API_KEY,
        'consumer_secret' => TWITTER_API_SECRET,
        'access_token' => '',
        'access_token_secret' => ''
    ],
    'linkedin' => [
        'client_id' => 'YOUR_LINKEDIN_CLIENT_ID',
        'client_secret' => 'YOUR_LINKEDIN_CLIENT_SECRET',
        'redirect_uri' => LINKEDIN_REDIRECT_URI,
        'scope' => 'r_liteprofile w_member_social'
    ]
];

// Iniciar sesión si no está iniciada
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

// Función para verificar si el usuario está autenticado
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

// Función para redirigir si no está autenticado
function requireLogin() {
    if (!isLoggedIn()) {
        header('Location: login.html');
        exit();
    }
}

// Función para obtener información del usuario actual
function getCurrentUser() {
    if (isLoggedIn()) {
        global $pdo;
        $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
        $stmt->execute([$_SESSION['user_id']]);
        return $stmt->fetch();
    }
    return null;
}
?>