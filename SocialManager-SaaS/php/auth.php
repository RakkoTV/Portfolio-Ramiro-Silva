<?php
require_once 'config.php';

// Función para registrar un nuevo usuario
function registerUser($firstName, $lastName, $email, $password, $plan) {
    global $pdo;
    
    // Verificar si el correo ya existe
    $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->execute([$email]);
    
    if ($stmt->rowCount() > 0) {
        return ['success' => false, 'message' => 'Este correo electrónico ya está registrado'];
    }
    
    // Hash de la contraseña
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    
    // Insertar nuevo usuario
    $stmt = $pdo->prepare("INSERT INTO users (first_name, last_name, email, password, plan, created_at) VALUES (?, ?, ?, ?, ?, NOW())");
    $result = $stmt->execute([$firstName, $lastName, $email, $hashedPassword, $plan]);
    
    if ($result) {
        // Obtener el ID del usuario recién creado
        $userId = $pdo->lastInsertId();
        
        // Iniciar sesión
        $_SESSION['user_id'] = $userId;
        $_SESSION['user_name'] = $firstName . ' ' . $lastName;
        $_SESSION['user_email'] = $email;
        $_SESSION['user_plan'] = $plan;
        
        return ['success' => true, 'user_id' => $userId];
    } else {
        return ['success' => false, 'message' => 'Error al registrar el usuario'];
    }
}

// Función para iniciar sesión
function loginUser($email, $password) {
    global $pdo;
    
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();
    
    // Verificar si la contraseña coincide directamente o mediante hash
    if ($user && ($password === $user['password'] || password_verify($password, $user['password']))) {
        // Iniciar sesión
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['first_name'] . ' ' . $user['last_name'];
        $_SESSION['user_email'] = $user['email'];
        $_SESSION['user_plan'] = $user['plan'];
        
        return ['success' => true, 'user' => $user];
    } else {
        return ['success' => false, 'message' => 'Credenciales incorrectas'];
    }
}

// Función para cerrar sesión
function logoutUser() {
    // Destruir todas las variables de sesión
    $_SESSION = [];
    
    // Destruir la cookie de sesión si existe
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000,
            $params["path"], $params["domain"],
            $params["secure"], $params["httponly"
        ]);
    }
    
    // Destruir la sesión
    session_destroy();
    
    return true;
}

// Procesar solicitudes AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = isset($_POST['action']) ? $_POST['action'] : '';
    
    header('Content-Type: application/json');
    
    switch ($action) {
        case 'register':
            $firstName = isset($_POST['first_name']) ? trim($_POST['first_name']) : '';
            $lastName = isset($_POST['last_name']) ? trim($_POST['last_name']) : '';
            $email = isset($_POST['email']) ? trim($_POST['email']) : '';
            $password = isset($_POST['password']) ? $_POST['password'] : '';
            $confirmPassword = isset($_POST['confirm_password']) ? $_POST['confirm_password'] : '';
            $plan = isset($_POST['plan']) ? $_POST['plan'] : 'basic';
            
            // Validaciones básicas
            if (empty($firstName) || empty($lastName) || empty($email) || empty($password)) {
                echo json_encode(['success' => false, 'message' => 'Todos los campos son obligatorios']);
                exit;
            }
            
            if ($password !== $confirmPassword) {
                echo json_encode(['success' => false, 'message' => 'Las contraseñas no coinciden']);
                exit;
            }
            
            $result = registerUser($firstName, $lastName, $email, $password, $plan);
            echo json_encode($result);
            break;
            
        case 'login':
            $email = isset($_POST['email']) ? trim($_POST['email']) : '';
            $password = isset($_POST['password']) ? $_POST['password'] : '';
            $remember = isset($_POST['remember']) ? true : false;
            
            // Validaciones básicas
            if (empty($email) || empty($password)) {
                echo json_encode(['success' => false, 'message' => 'Todos los campos son obligatorios']);
                exit;
            }
            
            $result = loginUser($email, $password);
            echo json_encode($result);
            break;
            
        case 'logout':
            $result = logoutUser();
            echo json_encode(['success' => $result]);
            break;
            
        default:
            echo json_encode(['success' => false, 'message' => 'Acción no válida']);
    }
    exit;
}
?>