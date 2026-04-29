document.addEventListener('DOMContentLoaded', () => {
    const folderCards = document.querySelectorAll('.folder-card');
    let draggedCard = null;

    // Función para extraer el título de un iframe
    const extractPageTitle = (iframe) => {
        try {
            return iframe.contentDocument.title || 'Sin título';
        } catch (e) {
            console.error('Error al acceder al título:', e);
            return 'Sin título';
        }
    };

    // Configurar eventos de arrastrar y soltar para cada tarjeta
    folderCards.forEach(card => {
        card.setAttribute('draggable', 'true');

        card.addEventListener('dragstart', (e) => {
            draggedCard = card;
            card.classList.add('dragging');
            e.dataTransfer.setData('text/plain', ''); // Necesario para Firefox
        });

        card.addEventListener('dragend', () => {
            draggedCard = null;
            card.classList.remove('dragging');
        });

        card.addEventListener('dragover', (e) => {
            e.preventDefault();
            if (card !== draggedCard) {
                const cardRect = card.getBoundingClientRect();
                const cardMiddle = cardRect.y + cardRect.height / 2;
                if (e.clientY < cardMiddle) {
                    card.parentNode.insertBefore(draggedCard, card);
                } else {
                    card.parentNode.insertBefore(draggedCard, card.nextSibling);
                }
            }
        });

        // Agregar navegación al hacer clic en la tarjeta
        // Crear botón de navegación
        const navButton = document.createElement('button');
        navButton.className = 'nav-button';
        navButton.textContent = 'IR';
        navButton.style.cssText = `
            background: linear-gradient(45deg, #ff4d4d, #ff8000);
            color: white;
            border: none;
            padding: 10px 30px;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            box-shadow: 0 4px 15px rgba(255, 77, 77, 0.3);
            transition: all 0.3s ease;
            z-index: 10;
        `;

        navButton.onmouseover = () => {
            navButton.style.transform = 'translateX(-50%) scale(1.1)';
            navButton.style.boxShadow = '0 6px 20px rgba(255, 77, 77, 0.4)';
        };

        navButton.onmouseout = () => {
            navButton.style.transform = 'translateX(-50%)';
            navButton.style.boxShadow = '0 4px 15px rgba(255, 77, 77, 0.3)';
        };

        navButton.onclick = (e) => {
            e.stopPropagation();
            const iframe = card.querySelector('.preview-frame');
            if (iframe) {
                window.location.href = iframe.src;
            }
        };

        card.appendChild(navButton);

        // Actualizar el título de la carpeta cuando el iframe se carga
        const iframe = card.querySelector('.preview-frame');
        if (iframe) {
            iframe.onload = () => {
                const title = extractPageTitle(iframe);
                const headerElement = card.querySelector('.folder-header');
                if (headerElement) {
                    headerElement.textContent = title;
                }
            };
        };
    });

    // Crear los controles de redimensionamiento
    const resizeButtons = document.createElement('div');
    resizeButtons.className = 'resize-controls';
    resizeButtons.innerHTML = `
        <button class="resize-btn decrease">-</button>
        <button class="resize-btn increase">+</button>
    `;

    // Agregar controles de redimensionamiento a cada tarjeta
    folderCards.forEach(card => {
        const controls = resizeButtons.cloneNode(true);
        card.appendChild(controls);

        const previewContainer = card.querySelector('.preview-container');
        let currentScale = 1.0; // Escala inicial más grande

        // Manejar clic en botones de redimensionamiento
        controls.querySelector('.decrease').addEventListener('click', () => {
            if (currentScale > 0.5) {
                currentScale = Math.round((currentScale - 0.1) * 10) / 10; // Redondear para evitar errores de punto flotante
                updatePreviewScale();
            }
        });

        controls.querySelector('.increase').addEventListener('click', () => {
            if (currentScale < 2.0) { // Aumentar el límite máximo
                currentScale = Math.round((currentScale + 0.1) * 10) / 10;
                updatePreviewScale();
            }
        });

        function updatePreviewScale() {
            const frame = previewContainer.querySelector('.preview-frame');
            if (frame) {
                frame.style.transform = `scale(${currentScale})`;
            }
            previewContainer.style.height = `${500 * currentScale}px`; // Aumentar altura base
            previewContainer.style.transition = 'height 0.3s ease'; // Agregar transición suave
        }
    });
});