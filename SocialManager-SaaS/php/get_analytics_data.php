<?php
// Este archivo simula la obtención de datos analíticos desde una base de datos
// En una implementación real, estos datos vendrían de una base de datos

// Asegurar que la respuesta sea JSON
header('Content-Type: application/json');

// Obtener parámetros de filtro (si existen)
$start_date = isset($_GET['start_date']) ? $_GET['start_date'] : null;
$end_date = isset($_GET['end_date']) ? $_GET['end_date'] : null;
$network = isset($_GET['network']) ? $_GET['network'] : null;

// Datos simulados para las redes sociales
$social_performance = [
    'facebook' => ['value' => 78, 'change' => 5],
    'instagram' => ['value' => 92, 'change' => 12],
    'twitter' => ['value' => 65, 'change' => -3],
    'linkedin' => ['value' => 45, 'change' => 8]
];

// Datos simulados para el crecimiento de seguidores
$followers_growth = [
    'ene' => 120,
    'feb' => 190,
    'mar' => 300,
    'abr' => 250,
    'may' => 400,
    'jun' => 480,
    'jul' => 520
];

// Datos simulados para engagement
$engagement = [
    'likes' => 8542,
    'comments' => 1253,
    'shares' => 3127,
    'views' => 24891
];

// Resumen de rendimiento
$performance_summary = [
    'followers' => 2456,
    'followers_change' => 12,
    'interactions' => 1024,
    'interactions_change' => 8,
    'posts' => 32,
    'posts_change' => -3
];

// Construir respuesta
$response = [
    'social_performance' => $social_performance,
    'followers_growth' => $followers_growth,
    'engagement' => $engagement,
    'performance_summary' => $performance_summary,
    'filter' => [
        'start_date' => $start_date,
        'end_date' => $end_date,
        'network' => $network
    ]
];

// Devolver datos como JSON
echo json_encode($response);