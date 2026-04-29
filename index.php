<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - Ramiro Silva</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Portfolio - Ramiro Silva</h1>
    </header>

    <div class="container">
        <div class="folders-grid">
            <?php
            // Obtener todas las carpetas en el directorio actual
            $dirs = array_filter(glob('*'), 'is_dir');
            
            // Ordenar alfabéticamente
            sort($dirs);
            
            // Generar las tarjetas de carpetas dinámicamente
            foreach ($dirs as $folder) {
                // Ignorar carpetas que empiezan con _ (nuestras carpetas de organización)
                if (strpos($folder, '_') === 0) continue;

                $indexPathHtml = $folder . '/index.html';
                $indexPathPhp = $folder . '/index.php';
                
                if (file_exists($indexPathHtml) || file_exists($indexPathPhp)) {
                    $indexPath = file_exists($indexPathHtml) ? $indexPathHtml : $indexPathPhp;
                    echo "<div class='folder-card'>";
                    echo "    <div class='folder-header'>$folder</div>";
                    echo "    <div class='preview-container'>";
                    echo "        <iframe src='$indexPath' class='preview-frame' title='Preview'></iframe>";
                    echo "    </div>";
                    echo "</div>";
                }
            }
            ?>
        </div>
    </div>

    <footer>
        <p>© 2025 Ramiro Silva</p>
    </footer>

    <script src="app.js"></script>
</body>
</html>