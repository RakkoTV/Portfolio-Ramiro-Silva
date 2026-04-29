<?php
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .custom-btn {
            background-color: #ff0000;
            color: white;
            border: none;
            padding: 10px 20px;
        }
        .custom-btn:hover {
            background-color: #cc0000;
            color: white;
        }
        .viral-btn {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 15px 30px;
        }
        .section-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center mb-5">Video Downloader</h1>
        <div class="text-center mb-4">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-danger active" data-platform="youtube">YouTube</button>
                <button class="btn btn-outline-dark" data-platform="tiktok">TikTok</button>
                <button class="btn btn-outline-primary" data-platform="instagram">Instagram</button>
            </div>
        </div>
        
        <!-- Botón VIRAL NOW -->
        <div class="text-center mb-4">
            <button class="btn custom-btn viral-btn" id="viralBtn">
                🔥 VIRAL NOW
            </button>
        </div>

        <!-- Información del Canal -->
        <div class="section-card">
            <h3 class="mb-3">Información del Canal</h3>
            <div class="input-group mb-3">
                <input type="text" class="form-control" id="channelUrl" placeholder="Ej: @RakkoTech o youtube.com/@RakkoTech">
                <button class="btn custom-btn" id="getChannelInfo">Obtener Info</button>
            </div>
        </div>

        <!-- Descarga de Videos -->
        <div class="section-card">
            <h3 class="mb-3">Descarga de Videos</h3>
            <div class="input-group mb-3">
                <input type="text" class="form-control" id="searchQuery" placeholder="Ej: Tutorial Python">
                <button class="btn custom-btn" id="searchVideo">Buscar</button>
            </div>
            <div class="input-group mb-3">
                <input type="text" class="form-control" id="videoUrl" placeholder="Ingresa la URL del video...">
                <button class="btn custom-btn" id="downloadVideo">Descargar</button>
            </div>
            <div id="downloadStatus" class="alert alert-info d-none">
                <div class="status-text">Iniciando descarga...</div>
                <div class="progress mt-2">
                    <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <div class="download-details mt-2 d-none">
                    <small>Velocidad: <span class="speed">0 MB/s</span> | Tiempo restante: <span class="eta">0s</span></small>
                </div>
            </div>
        </div>

        <!-- Descarga por Segmentos -->
        <div class="section-card">
            <h3 class="mb-3">Descarga por Segmentos</h3>
            <div class="row g-3 align-items-center">
                <div class="col-auto">
                    <label class="col-form-label">Duración (seg):</label>
                </div>
                <div class="col-auto">
                    <input type="number" class="form-control" id="segmentSeconds" value="15">
                </div>
                <div class="col-auto">
                    <label class="col-form-label">Número de partes:</label>
                </div>
                <div class="col-auto">
                    <input type="number" class="form-control" id="segmentParts" value="3">
                </div>
            </div>
        </div>

        <!-- Área de Mensajes -->
        <div class="alert alert-info d-none" id="messageArea" role="alert"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const messageArea = document.getElementById('messageArea');
            const downloadStatus = document.getElementById('downloadStatus');
            let selectedPlatform = 'youtube';

            // Platform selection
            document.querySelectorAll('[data-platform]').forEach(button => {
                button.addEventListener('click', () => {
                    document.querySelectorAll('[data-platform]').forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    selectedPlatform = button.dataset.platform;
                    updatePlaceholder();
                });
            });

            function updatePlaceholder() {
                const urlInput = document.getElementById('videoUrl');
                switch(selectedPlatform) {
                    case 'youtube':
                        urlInput.placeholder = 'Ej: https://www.youtube.com/watch?v=...';
                        break;
                    case 'tiktok':
                        urlInput.placeholder = 'Ej: https://www.tiktok.com/@usuario/video/...';
                        break;
                    case 'instagram':
                        urlInput.placeholder = 'Ej: https://www.instagram.com/p/...';
                        break;
                }
            }

            function showMessage(message, isError = false) {
                messageArea.textContent = message;
                messageArea.className = `alert ${isError ? 'alert-danger' : 'alert-info'}`;
                messageArea.classList.remove('d-none');
            }

            async function makeRequest(endpoint, data) {
                try {
                    downloadStatus.className = 'alert alert-info';
                    downloadStatus.classList.remove('d-none');

                    const progressBar = downloadStatus.querySelector('.progress-bar');
                    const statusText = downloadStatus.querySelector('.status-text');
                    const downloadDetails = downloadStatus.querySelector('.download-details');

                    statusText.textContent = 'Iniciando descarga...';
                    progressBar.style.width = '0%';
                    progressBar.setAttribute('aria-valuenow', 0);
                    downloadDetails.classList.add('d-none');

                    let response;
                    if (endpoint === 'download') {
                        response = await fetch('download.php', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        });
                    } else {
                        response = await fetch(`api/${endpoint}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        });
                    }
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Error en la comunicación con el servidor');
                    }
                    
                    const result = await response.json();

                    if (endpoint === 'download' && result.video_url) {
                        statusText.textContent = 'Descargando archivo...';
                        progressBar.style.width = '50%';
                        progressBar.setAttribute('aria-valuenow', 50);

                        window.location.href = result.video_url;
                        
                        progressBar.style.width = '100%';
                        progressBar.setAttribute('aria-valuenow', 100);
                        statusText.textContent = 'Descarga iniciada';
                        downloadStatus.className = 'alert alert-success';
                        
                        setTimeout(() => {
                            downloadStatus.className = 'alert alert-success';
                            statusText.textContent = 'Descarga Completa';
                            downloadDetails.classList.add('d-none');
                        }, 1000);
                    } else {
                        throw new Error('No se pudo obtener la URL del video');
                    }
                } catch (error) {
                    console.error('Error en la descarga:', error);
                    downloadStatus.className = 'alert alert-danger';
                    
                    let errorMessage = error.message || 'No se pudo completar la descarga. Por favor, verifica la URL e intenta nuevamente.';
                    
                    if (errorMessage.includes('Failed to fetch') || errorMessage.includes('NetworkError')) {
                        errorMessage = 'Error de conexión: No se pudo acceder al recurso. Puede ser un problema de conexión o que el video no está disponible.';
                    }
                    
                    downloadStatus.querySelector('.status-text').textContent = `Error: ${errorMessage}`;
                    downloadDetails.classList.add('d-none');
                    const progressBar = downloadStatus.querySelector('.progress-bar');
                    progressBar.style.width = '0%';
                    progressBar.setAttribute('aria-valuenow', 0);
                }
            }

            // Event Listeners
            document.getElementById('viralBtn').onclick = () => {
                showMessage('Buscando videos virales...');
            };

            document.getElementById('getChannelInfo').onclick = () => {
                const channelUrl = document.getElementById('channelUrl').value;
                makeRequest('channel-info', { channelUrl });
            };

            document.getElementById('searchVideo').onclick = async () => {
                const query = document.getElementById('searchQuery').value;
                if (!query || query === 'Ej: Tutorial Python') {
                    showMessage('Por favor ingresa un término de búsqueda', true);
                    return;
                }
                
                // Mostrar indicador de carga
                showMessage('Buscando videos...', false);

                try {
                    const response = await fetch('search.php', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query })
                    });

                    const data = await response.json();
                    
                    if (data.error) {
                        showMessage('Error: ' + data.error, true);
                        return;
                    }

                    if (!data.videos || data.videos.length === 0) {
                        showMessage(data.message || 'No se encontraron videos para tu búsqueda', true);
                        return;
                    }
                    
                    // Limpiar mensaje de carga
                    messageArea.classList.add('d-none');

                    // Crear y mostrar los resultados
                    const resultsHtml = data.videos.map(video => `
                        <div class="card mb-3">
                            <div class="row g-0">
                                <div class="col-md-4">
                                    <img src="${video.thumbnail}" class="img-fluid rounded-start" alt="${video.title}">
                                </div>
                                <div class="col-md-8">
                                    <div class="card-body">
                                        <h5 class="card-title">${video.title}</h5>
                                        <p class="card-text">${video.description}</p>
                                        <p class="card-text"><small class="text-muted">Canal: ${video.channel}</small></p>
                                        <button class="btn custom-btn" onclick="document.getElementById('videoUrl').value = 'https://www.youtube.com/watch?v=${video.id}'">Seleccionar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('');

                    // Crear o actualizar el contenedor de resultados
                    let resultsContainer = document.getElementById('searchResults');
                    if (!resultsContainer) {
                        resultsContainer = document.createElement('div');
                        resultsContainer.id = 'searchResults';
                        document.getElementById('video_frame').insertBefore(resultsContainer, document.getElementById('videoUrl').parentNode);
                    }
                    resultsContainer.innerHTML = resultsHtml;

                } catch (error) {
                    showMessage('Error al buscar videos: ' + error.message, true);
                }
            };

            document.getElementById('downloadVideo').onclick = () => {
                const url = document.getElementById('videoUrl').value;
                makeRequest('download', { url });
            };
        });
    </script>
</body>
</html>