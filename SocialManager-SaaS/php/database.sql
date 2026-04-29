-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS socialmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE socialmanager;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    plan VARCHAR(20) NOT NULL DEFAULT 'basic',
    profile_image VARCHAR(255) DEFAULT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME DEFAULT NULL
) ENGINE=InnoDB;

-- Tabla de publicaciones
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    platform VARCHAR(20) NOT NULL,
    image_url VARCHAR(255) DEFAULT NULL,
    scheduled_date DATETIME DEFAULT NULL,
    published BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla de estadísticas de publicaciones
CREATE TABLE IF NOT EXISTS post_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    views INT DEFAULT 0,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Índices para optimizar consultas
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_post_user ON posts(user_id);
CREATE INDEX idx_post_platform ON posts(platform);
CREATE INDEX idx_post_scheduled ON posts(scheduled_date);