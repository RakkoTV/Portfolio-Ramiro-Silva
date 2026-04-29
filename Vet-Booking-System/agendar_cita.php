<?php

// --- Cabeceras para respuesta JSON y CORS ---
header("Access-Control-Allow-Origin: *");
header("Access-control-allow-headers: Content-Type");
header("Content-Type: application/json; charset=UTF-8");

// --- Manejo de la solicitud ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener el cuerpo de la solicitud (que es JSON) y decodificarlo
    $jsonPayload = file_get_contents('php://input');
    $data = json_decode($jsonPayload, true);

    // --- Validación de datos ---
    $service = $data['service'] ?? null;
    $date = $data['date'] ?? null;
    $time = $data['time'] ?? null;
    $petName = $data['petName'] ?? null;
    $ownerName = $data['ownerName'] ?? null;

    if (empty($service) || empty($date) || empty($time) || empty($petName) || empty($ownerName)) {
        http_response_code(400); // Bad Request
        echo json_encode(['success' => false, 'message' => 'Por favor, completa todos los campos.']);
        exit;
    }

    // --- Envío de datos a Google Forms ---
    $googleFormUrl = 'https://docs.google.com/forms/d/e/1FAIpQLSfOBV1nOGd3E-69-Ni1Ob-Xt49i7VjYVvJIr_duDl3D4iBe4g/formResponse';

    // Esta línea es CORRECTA y debe permanecer, ya que en tu formulario "Peluqueria" no tiene tilde.
    $service = str_replace('í', 'i', $service);

    // Validar que la fecha tenga el formato YYYY-MM-DD.
    $dateObject = DateTime::createFromFormat('Y-m-d', $date);
    if (!$dateObject || $dateObject->format('Y-m-d') !== $date) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Formato de fecha inválido.']);
        exit;
    }

    // --- Validación de reglas de negocio para días y horas ---
    $dayOfWeek = (int)$dateObject->format('w'); // 0 (para Domingo) hasta 6 (para Sábado)
    $timeObject = DateTime::createFromFormat('H:i', $time);

    // 1. No permitir citas los domingos
    if ($dayOfWeek === 0) { // Domingo es 0
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Lo sentimos, no se agendan citas los domingos.']);
        exit;
    }

    // 2. Citas de sábados solo de 09:00 a 14:00
    if ($dayOfWeek === 6) { // Sábado es 6
        if (!$timeObject || $timeObject->format('H:i') !== $time) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Formato de hora inválido para sábado.']);
            exit;
        }

        $saturdayStart = DateTime::createFromFormat('H:i', '09:00');
        $saturdayEnd = DateTime::createFromFormat('H:i', '14:00');

        if ($timeObject < $saturdayStart || $timeObject > $saturdayEnd) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Los sábados solo se agendan citas de 09:00 a 14:00.']);
            exit;
        }
    }

    // ¡IMPORTANTE! Reemplaza estos entry.xxxxx con los que obtengas de tu enlace pre-rellenado.
    $postData = [
        'entry.2032679370' => $ownerName, // Tu Nombre y Apellido
        'entry.1262947740' => $petName,   // Nombre de tu Mascota
        'entry.2064936495' => $service,   // Servicio
        'entry.1059002338' => $date,      // Fecha
        'entry.267938164'  => $time       // Horarios Disponibles
    ];

    // Inicializar cURL
    $ch = curl_init($googleFormUrl);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postData));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // Se eliminan las siguientes dos líneas por seguridad. No son necesarias.
    // curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 
    // curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false); 
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true); // Seguir redirecciones
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'); // Simular User-Agent de navegador
    curl_setopt($ch, CURLOPT_REFERER, 'https://docs.google.com/forms/d/e/1FAIpQLSfOBV1nOGd3E-69-Ni1Ob-Xt49i7VjYVvJIr_duDl3D4iBe4g/viewform'); // Añadir cabecera Referer
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/x-www-form-urlencoded')); // Establecer Content-Type explícitamente
    curl_setopt($ch, CURLOPT_TIMEOUT, 10); // Tiempo de espera de 10 segundos

    // Ejecutar la solicitud
    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curl_error = curl_error($ch);
    curl_close($ch);

    // Verificar la respuesta
    // Google Forms responde con un 200 OK si la entrada es exitosa.
    if ($httpcode == 200) {
        http_response_code(200); // OK
        echo json_encode(['success' => true, 'message' => '¡Gracias! Tu cita ha sido agendada. Te contactaremos pronto para confirmar.']);
    } else {
        http_response_code(500); // Internal Server Error
        echo json_encode([
            'success' => false, 
            'message' => 'Error del servidor: No se pudo registrar la cita. Por favor, intenta llamar por teléfono.',
            'debug' => [
                'http_code' => $httpcode,
                'curl_error' => $curl_error,
                'post_data_sent' => $postData
            ]
        ]);
    }

} else {
    // Si no es una solicitud POST, se rechaza.
    http_response_code(405); // Method Not Allowed
    echo json_encode(['success' => false, 'message' => 'Método no permitido.']);
}
?>