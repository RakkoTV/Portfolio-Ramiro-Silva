// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const imageGallery = document.getElementById('image-gallery');
    const loadingIndicator = document.getElementById('loading-indicator');
    const container = document.querySelector('.container');
    const downloadBtn = document.getElementById('download-all-btn'); // Obtener el botón de descarga

    // --- Inicio: Verificación de estado del servidor ---
    const statusElement = document.createElement('div');
    statusElement.id = 'server-status';
    statusElement.style.marginTop = '15px';
    statusElement.style.padding = '10px';
    statusElement.style.borderRadius = '5px';
    statusElement.style.textAlign = 'center';
    container.insertBefore(statusElement, form); // Insertar antes del formulario

    fetch('/status')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                statusElement.textContent = '✅ Servidor listo.';
                statusElement.style.backgroundColor = '#e6ffed';
                statusElement.style.color = '#006400';
            } else {
                statusElement.textContent = `⚠️ ${data.message || 'Problema con el servidor.'}`;
                statusElement.style.backgroundColor = '#fffbe6';
                statusElement.style.color = '#8B4513';
            }
        })
        .catch(error => {
            console.error('Error checking server status:', error);
            statusElement.textContent = '❌ No se pudo conectar con el servidor.';
            statusElement.style.backgroundColor = '#ffe6e6';
            statusElement.style.color = '#a00';
            // Deshabilitar formulario si no se puede conectar
            form.querySelector('button[type="submit"]').disabled = true;
            form.querySelector('.file-label').style.opacity = '0.5';
            form.querySelector('.file-label').style.cursor = 'not-allowed';
            form.querySelector('#file-input').disabled = true;
        });
    // --- Fin: Verificación de estado del servidor ---

    // Animación inicial del contenedor con GSAP
    gsap.to(container, { duration: 0.8, opacity: 1, y: 0, ease: 'power2.out' });

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        loadingIndicator.style.display = 'block'; // Mostrar indicador de carga
        imageGallery.innerHTML = ''; // Limpiar galería anterior
        downloadBtn.style.display = 'none'; // Ocultar botón de descarga al iniciar
        downloadBtn.onclick = null; // Limpiar listener anterior

        const formData = new FormData(form);

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                // Intentar obtener mensaje de error del backend si está en JSON
                let errorMsg = `Error: ${response.statusText}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) { /* No es JSON, usar statusText */ }
                throw new Error(errorMsg);
            }

            const result = await response.json();

            // Mostrar imágenes si existen
            if (result.image_urls && result.image_urls.length > 0) {
                result.image_urls.forEach(imageUrl => {
                    const img = document.createElement('img');
                    img.src = imageUrl + '?t=' + new Date().getTime(); // Añadir timestamp para evitar caché
                    img.alt = 'Imagen convertida';
                    imageGallery.appendChild(img);
                });

                // Animar las imágenes recién añadidas con GSAP
                gsap.fromTo(imageGallery.children, 
                    { opacity: 0, scale: 0.8, y: 20 }, 
                    { 
                        duration: 0.5, 
                        opacity: 1, 
                        scale: 1, 
                        y: 0, 
                        stagger: 0.1, // Añade un pequeño retraso entre cada imagen
                        ease: 'back.out(1.7)'
                    }
                );
            }

            // Habilitar botón de descarga si existe la URL del ZIP
            if (result.zip_url) {
                downloadBtn.style.display = 'inline-block'; // Mostrar el botón
                downloadBtn.onclick = () => {
                    window.location.href = result.zip_url; // Redirigir para descargar
                };
                 // Animar el botón de descarga
                 gsap.fromTo(downloadBtn, {opacity: 0, y: 10}, {duration: 0.5, opacity: 1, y: 0, ease: 'power2.out', delay: 0.5});
            }

            // Mostrar error si no hay imágenes ni zip (puede ocurrir si falla la conversión)
            if ((!result.image_urls || result.image_urls.length === 0) && !result.zip_url) {
                 // Si ya se lanzó un error antes, no mostrar este mensaje genérico
                 if (!response.ok) return; // El error ya se manejó
                 imageGallery.innerHTML = '<p style="color: red;">No se pudieron generar imágenes o el archivo ZIP.</p>';
            }

        } catch (error) {
            console.error('Error en la conversión:', error);
            imageGallery.innerHTML = `<p style="color: red;">Error durante la conversión: ${error.message}</p>`;
        } finally {
            loadingIndicator.style.display = 'none'; // Ocultar indicador de carga
        }
    });
});