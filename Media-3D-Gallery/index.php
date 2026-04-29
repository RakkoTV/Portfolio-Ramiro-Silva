<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reproductor de Video</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            min-height: 100vh;
            box-sizing: border-box;
        }
        h1 {
            color: #fff;
            font-weight: 700;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        h2 {
            color: #f0f0f0;
            font-weight: 400;
            margin-top: 40px;
            margin-bottom: 15px;
        }
        .video-container {
            margin-top: 20px;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            width: 90%;
            max-width: 800px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        video {
            width: 100%;
            border-radius: 8px;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .video-list {
            margin-top: 20px;
            list-style: none;
            padding: 0;
            width: 90%;
            max-width: 800px;
        }
        .video-list li {
            background-color: rgba(255, 255, 255, 0.15);
            color: #fff;
            padding: 12px 18px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-weight: 300;
        }
        .video-list li:hover {
            background-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        /* Estilo para el video activo (opcional) */
        .video-list li.active {
            background-color: rgba(102, 126, 234, 0.5); /* Un color que combine con el gradiente */
            font-weight: 700;
        }

        .video-controls {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 15px;
        }

        .control-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Roboto', sans-serif;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .control-button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0,0,0,0.15);
        }
        .control-button:disabled {
            background: #aaa;
            cursor: not-allowed;
            opacity: 0.7;
        }

        .main-nav {
            margin-bottom: 20px;
            padding: 10px;
            background-color: rgba(0,0,0,0.1);
            border-radius: 8px;
            display: flex;
            gap: 15px;
        }
        .nav-link {
            color: #fff;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 6px;
            transition: background-color 0.3s ease;
        }
        .nav-link:hover {
            background-color: rgba(255,255,255,0.2);
        }
        .nav-link.active-nav {
            background-color: rgba(102, 126, 234, 0.5);
            font-weight: bold;
        }

    </style>
</head>
<body>
    <h1>Reproductor de Videos</h1>
    <nav class="main-nav">
        <a href="index.php" class="nav-link active-nav">Reproductor</a>
        <a href="3d.php" class="nav-link">Página 3D</a>
    </nav>
    <div class="video-container">
        <video id="mainVideo" controls>
            <!-- El primer video se cargará aquí por defecto -->
        </video>
        <div class="video-controls">
            <button id="prevButton" class="control-button">&#9664; Anterior</button>
            <button id="nextButton" class="control-button">Siguiente &#9654;</button>
        </div>
    </div>

    <h2>Lista de Videos</h2>
    <ul id="videoList" class="video-list">
        <?php
            $videosFolderPath = 'V1d30s/';
            $allowedExtensions = ['mp4', 'avi'];
            $videoFiles = [];

            if (is_dir($videosFolderPath)) {
                if ($handle = opendir($videosFolderPath)) {
                    while (false !== ($entry = readdir($handle))) {
                        if ($entry != "." && $entry != "..") {
                            $extension = strtolower(pathinfo($entry, PATHINFO_EXTENSION));
                            if (in_array($extension, $allowedExtensions)) {
                                $videoFiles[] = $entry;
                            }
                        }
                    }
                    closedir($handle);
                }
            }

            if (!empty($videoFiles)) {
                foreach ($videoFiles as $videoFile) {
                    // Se elimina el onclick de aquí, ya que se manejará con JS puro después de cargar el DOM
                    echo "<li>" . htmlspecialchars($videoFile) . "</li>";
                }
            } else {
                echo "<li>No se encontraron videos (.mp4, .avi) en la carpeta 'V1d30s'.</li>";
            }
        ?>
    </ul>

    <script>
        const videoPlayer = document.getElementById('mainVideo');
        // Pausar el video al cargar la página
        window.addEventListener('DOMContentLoaded', function() {
            videoPlayer.pause();
        });
        // Reproducir solo al hacer clic
        videoPlayer.addEventListener('click', function() {
            if (videoPlayer.paused) {
                videoPlayer.play();
            }
        });
        const videoListItems = document.querySelectorAll('#videoList li');
        const videosFolderPath = 'V1d30s/';
        const videoFilesFromPHP = <?php echo json_encode($videoFiles); ?>;
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        let currentVideoIndex = 0;

        function updateButtonStates() {
            if (!prevButton || !nextButton) return; // Asegurarse que los botones existen
            prevButton.disabled = videoFilesFromPHP.length <= 1;
            nextButton.disabled = videoFilesFromPHP.length <= 1;
            // Si quieres deshabilitar en los extremos sin hacer loop:
            // prevButton.disabled = currentVideoIndex === 0;
            // nextButton.disabled = currentVideoIndex === videoFilesFromPHP.length - 1;
        }

        function setActiveListItem(index) {
            videoListItems.forEach((item, idx) => {
                if (idx === index) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        }

        function loadVideo(index) {
            if (videoFilesFromPHP.length === 0) return;
            currentVideoIndex = (index + videoFilesFromPHP.length) % videoFilesFromPHP.length; // Manejo de loop
            const videoName = videoFilesFromPHP[currentVideoIndex];
            videoPlayer.src = videosFolderPath + videoName;
            videoPlayer.play();
            setActiveListItem(currentVideoIndex);
            updateButtonStates(); // Actualizar estado de botones
        }

        if (prevButton) {
            prevButton.onclick = () => {
                if (videoFilesFromPHP.length > 0) {
                    loadVideo(currentVideoIndex - 1);
                }
            };
        }

        if (nextButton) {
            nextButton.onclick = () => {
                if (videoFilesFromPHP.length > 0) {
                    loadVideo(currentVideoIndex + 1);
                }
            };
        }

        videoListItems.forEach((item, idx) => {
            item.onclick = () => loadVideo(idx);
        });

        // Cargar el primer video si hay alguno
        if (videoFilesFromPHP.length > 0) {
            loadVideo(0);
        } else {
            if (prevButton) prevButton.disabled = true;
            if (nextButton) nextButton.disabled = true;
        }
        updateButtonStates(); // Estado inicial de los botones
    </script>
</body>
</html>