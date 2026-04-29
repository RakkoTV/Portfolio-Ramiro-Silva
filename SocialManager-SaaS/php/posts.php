<?php
require_once 'config.php';

// Verificar si el usuario está autenticado
requireLogin();

// Función para crear una nueva publicación
function createPost($userId, $content, $platform, $scheduledDate = null, $image = null) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("INSERT INTO posts (user_id, content, platform, image_url, scheduled_date, created_at) VALUES (?, ?, ?, ?, ?, NOW())");
        $result = $stmt->execute([$userId, $content, $platform, $image, $scheduledDate]);
        
        if ($result) {
            return ['success' => true, 'post_id' => $pdo->lastInsertId()];
        } else {
            return ['success' => false, 'message' => 'Error al crear la publicación'];
        }
    } catch (PDOException $e) {
        return ['success' => false, 'message' => 'Error: ' . $e->getMessage()];
    }
}

// Función para crear publicaciones en múltiples redes sociales
function createMultiplePosts($userId, $content, $platforms, $scheduledDate = null, $image = null) {
    global $pdo;
    $posts = [];
    $success = true;
    $errorMessage = '';
    
    // Iniciar transacción para asegurar que todas las publicaciones se crean o ninguna
    $pdo->beginTransaction();
    
    try {
        foreach ($platforms as $platform) {
            $stmt = $pdo->prepare("INSERT INTO posts (user_id, content, platform, image_url, scheduled_date, created_at) VALUES (?, ?, ?, ?, ?, NOW())");
            $result = $stmt->execute([$userId, $content, $platform, $image, $scheduledDate]);
            
            if ($result) {
                $postId = $pdo->lastInsertId();
                // Obtener la publicación recién creada
                $stmt = $pdo->prepare("SELECT * FROM posts WHERE id = ?");
                $stmt->execute([$postId]);
                $posts[] = $stmt->fetch();
            } else {
                $success = false;
                $errorMessage = 'Error al crear la publicación en ' . $platform;
                break;
            }
        }
        
        if ($success) {
            $pdo->commit();
            return ['success' => true, 'posts' => $posts];
        } else {
            $pdo->rollBack();
            return ['success' => false, 'message' => $errorMessage];
        }
    } catch (PDOException $e) {
        $pdo->rollBack();
        return ['success' => false, 'message' => 'Error: ' . $e->getMessage()];
    }
}

// Función para obtener publicaciones de un usuario
function getUserPosts($userId, $limit = 10, $offset = 0, $platform = null) {
    global $pdo;
    
    $query = "SELECT * FROM posts WHERE user_id = ?";
    $params = [$userId];
    
    if ($platform) {
        $query .= " AND platform = ?";
        $params[] = $platform;
    }
    
    $query .= " ORDER BY scheduled_date DESC, created_at DESC LIMIT ? OFFSET ?";
    $params[] = $limit;
    $params[] = $offset;
    
    $stmt = $pdo->prepare($query);
    $stmt->execute($params);
    
    return $stmt->fetchAll();
}

// Función para obtener una publicación específica
function getPost($postId, $userId) {
    global $pdo;
    
    $stmt = $pdo->prepare("SELECT * FROM posts WHERE id = ? AND user_id = ?");
    $stmt->execute([$postId, $userId]);
    
    return $stmt->fetch();
}

// Función para actualizar una publicación
function updatePost($postId, $userId, $content, $platform, $scheduledDate = null, $image = null) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("UPDATE posts SET content = ?, platform = ?, scheduled_date = ?, image_url = ?, updated_at = NOW() WHERE id = ? AND user_id = ?");
        $result = $stmt->execute([$content, $platform, $scheduledDate, $image, $postId, $userId]);
        
        if ($result) {
            return ['success' => true];
        } else {
            return ['success' => false, 'message' => 'Error al actualizar la publicación'];
        }
    } catch (PDOException $e) {
        return ['success' => false, 'message' => 'Error: ' . $e->getMessage()];
    }
}

// Función para eliminar una publicación
function deletePost($postId, $userId) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("DELETE FROM posts WHERE id = ? AND user_id = ?");
        $result = $stmt->execute([$postId, $userId]);
        
        if ($result) {
            return ['success' => true];
        } else {
            return ['success' => false, 'message' => 'Error al eliminar la publicación'];
        }
    } catch (PDOException $e) {
        return ['success' => false, 'message' => 'Error: ' . $e->getMessage()];
    }
}

// Función para obtener estadísticas de publicaciones
function getPostStats($userId) {
    global $pdo;
    
    // Total de publicaciones
    $stmt = $pdo->prepare("SELECT COUNT(*) as total FROM posts WHERE user_id = ?");
    $stmt->execute([$userId]);
    $totalPosts = $stmt->fetch()['total'];
    
    // Publicaciones por plataforma
    $stmt = $pdo->prepare("SELECT platform, COUNT(*) as count FROM posts WHERE user_id = ? GROUP BY platform");
    $stmt->execute([$userId]);
    $platformStats = $stmt->fetchAll();
    
    // Publicaciones programadas pendientes
    $stmt = $pdo->prepare("SELECT COUNT(*) as pending FROM posts WHERE user_id = ? AND scheduled_date > NOW()");
    $stmt->execute([$userId]);
    $pendingPosts = $stmt->fetch()['pending'];
    
    return [
        'total' => $totalPosts,
        'by_platform' => $platformStats,
        'pending' => $pendingPosts
    ];
}

// Procesar solicitudes AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = isset($_POST['action']) ? $_POST['action'] : '';
    
    header('Content-Type: application/json');
    
    switch ($action) {
        case 'create':
            $content = isset($_POST['content']) ? trim($_POST['content']) : '';
            $platforms = isset($_POST['platforms']) ? $_POST['platforms'] : [];
            $scheduledDate = !empty($_POST['scheduled_date']) ? $_POST['scheduled_date'] : null;
            
            // Validaciones básicas
            if (empty($content) || empty($platforms)) {
                echo json_encode(['success' => false, 'message' => 'El contenido y al menos una red social son obligatorios']);
                exit;
            }
            
            // Procesar imagen si existe
            $imageUrl = null;
            if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
                $uploadDir = '../uploads/';
                
                // Crear directorio si no existe
                if (!file_exists($uploadDir)) {
                    mkdir($uploadDir, 0777, true);
                }
                
                $fileName = time() . '_' . basename($_FILES['image']['name']);
                $uploadFile = $uploadDir . $fileName;
                
                if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadFile)) {
                    $imageUrl = 'uploads/' . $fileName;
                }
            }
            
            // Usar la función de múltiples publicaciones si hay más de una plataforma
            $result = createMultiplePosts($_SESSION['user_id'], $content, $platforms, $scheduledDate, $imageUrl);
            echo json_encode($result);
            break;
            
        case 'update':
            $postId = isset($_POST['post_id']) ? intval($_POST['post_id']) : 0;
            $content = isset($_POST['content']) ? trim($_POST['content']) : '';
            $platform = isset($_POST['platform']) ? $_POST['platform'] : '';
            $scheduledDate = !empty($_POST['scheduled_date']) ? $_POST['scheduled_date'] : null;
            
            // Validaciones básicas
            if ($postId <= 0 || empty($content) || empty($platform)) {
                echo json_encode(['success' => false, 'message' => 'Datos inválidos']);
                exit;
            }
            
            // Verificar que la publicación pertenece al usuario
            $post = getPost($postId, $_SESSION['user_id']);
            if (!$post) {
                echo json_encode(['success' => false, 'message' => 'Publicación no encontrada']);
                exit;
            }
            
            // Procesar imagen si existe
            $imageUrl = $post['image_url'];
            if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
                $uploadDir = '../uploads/';
                
                // Crear directorio si no existe
                if (!file_exists($uploadDir)) {
                    mkdir($uploadDir, 0777, true);
                }
                
                $fileName = time() . '_' . basename($_FILES['image']['name']);
                $uploadFile = $uploadDir . $fileName;
                
                if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadFile)) {
                    $imageUrl = 'uploads/' . $fileName;
                }
            }
            
            $result = updatePost($postId, $_SESSION['user_id'], $content, $platform, $scheduledDate, $imageUrl);
            echo json_encode($result);
            break;
            
        case 'delete':
            $postId = isset($_POST['post_id']) ? intval($_POST['post_id']) : 0;
            
            if ($postId <= 0) {
                echo json_encode(['success' => false, 'message' => 'ID de publicación inválido']);
                exit;
            }
            
            $result = deletePost($postId, $_SESSION['user_id']);
            echo json_encode($result);
            break;
            
        default:
            echo json_encode(['success' => false, 'message' => 'Acción no válida']);
    }
    exit;
}

// Procesar solicitudes GET para obtener publicaciones
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = isset($_GET['action']) ? $_GET['action'] : 'list';
    
    header('Content-Type: application/json');
    
    switch ($action) {
        case 'list':
            $platform = isset($_GET['platform']) ? $_GET['platform'] : null;
            $limit = isset($_GET['limit']) ? intval($_GET['limit']) : 10;
            $offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;
            
            $posts = getUserPosts($_SESSION['user_id'], $limit, $offset, $platform);
            echo json_encode(['success' => true, 'posts' => $posts]);
            break;
            
        case 'get':
            $postId = isset($_GET['post_id']) ? intval($_GET['post_id']) : 0;
            
            if ($postId <= 0) {
                echo json_encode(['success' => false, 'message' => 'ID de publicación inválido']);
                exit;
            }
            
            $post = getPost($postId, $_SESSION['user_id']);
            
            if ($post) {
                echo json_encode(['success' => true, 'post' => $post]);
            } else {
                echo json_encode(['success' => false, 'message' => 'Publicación no encontrada']);
            }
            break;
            
        case 'stats':
            $stats = getPostStats($_SESSION['user_id']);
            echo json_encode(['success' => true, 'stats' => $stats]);
            break;
            
        default:
            echo json_encode(['success' => false, 'message' => 'Acción no válida']);
    }
    exit;
}
?>