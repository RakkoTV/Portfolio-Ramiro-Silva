// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Navegación con desplazamiento suave
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Si es un enlace de dropdown, no prevenir el comportamiento predeterminado
            if (this.classList.contains('dropdown-toggle')) {
                e.preventDefault();
                return;
            }
            
            // Prevenir el comportamiento predeterminado del enlace
            e.preventDefault();
            
            // Obtener el destino del enlace
            const targetId = this.getAttribute('href');
            
            // Si es un enlace interno, desplazarse suavemente
            if (targetId.startsWith('#')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            } else {
                // Si es un enlace externo, navegar normalmente
                window.location.href = targetId;
            }
        });
    });
    
    // Manejo de dropdowns en móvil
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            const dropdownMenu = parent.querySelector('.dropdown-menu');
            
            // En móvil, alternar la visibilidad del menú desplegable
            if (window.innerWidth <= 768) {
                if (dropdownMenu.style.display === 'block') {
                    dropdownMenu.style.display = 'none';
                } else {
                    // Cerrar todos los otros menús desplegables primero
                    document.querySelectorAll('.dropdown-menu').forEach(menu => {
                        if (menu !== dropdownMenu) {
                            menu.style.display = 'none';
                        }
                    });
                    dropdownMenu.style.display = 'block';
                }
            }
        });
    });
    
    // Animación de aparición al desplazarse
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .showcase-content, .testimonial-card, .cta-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('visible');
            }
        });
    };
    
    // Ejecutar la animación al cargar la página
    animateOnScroll();
    
    // Ejecutar la animación al desplazarse
    window.addEventListener('scroll', animateOnScroll);
    
    // Menú móvil
    const mobileMenuButton = document.createElement('button');
    mobileMenuButton.classList.add('mobile-menu-button');
    mobileMenuButton.innerHTML = '☰';
    document.querySelector('.header-container').prepend(mobileMenuButton);
    
    mobileMenuButton.addEventListener('click', function() {
        const nav = document.querySelector('nav');
        nav.classList.toggle('active');
    });
    
    // Actualizar año de copyright automáticamente
    const yearElement = document.querySelector('.footer-bottom p');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.innerHTML = `&copy; ${currentYear} Todos los derechos reservados.`;
    }

    // Crear el modal lightbox para las imágenes
    const lightboxModal = document.createElement('div');
    lightboxModal.classList.add('lightbox-modal');
    lightboxModal.innerHTML = `
        <span class="close-lightbox">&times;</span>
        <div class="lightbox-content">
            <img class="lightbox-image" src="" alt="Imagen ampliada">
        </div>
    `;
    document.body.appendChild(lightboxModal);

    // Función para abrir el lightbox
    function openLightbox(imageSrc) {
        const lightboxImage = document.querySelector('.lightbox-image');
        lightboxImage.src = imageSrc;
        lightboxModal.style.display = 'flex';
    }

    // Función para cerrar el lightbox
    function closeLightbox() {
        lightboxModal.style.display = 'none';
    }

    // Agregar evento de clic a las imágenes de la galería
    const galleryImages = document.querySelectorAll('.gallery-image');
    galleryImages.forEach(image => {
        image.addEventListener('click', function() {
            openLightbox(this.src);
        });
    });

    // Cerrar el lightbox al hacer clic en el botón de cierre
    const closeButton = document.querySelector('.close-lightbox');
    closeButton.addEventListener('click', function(e) {
        e.stopPropagation();
        closeLightbox();
    });

    // Cerrar el lightbox al hacer clic fuera de la imagen
    lightboxModal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeLightbox();
        }
    });

    // Cerrar el lightbox al presionar la tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightboxModal.style.display === 'flex') {
            closeLightbox();
        }
    });
});

// Añadir estilos CSS adicionales para las animaciones
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .feature-card, .showcase-content, .testimonial-card, .cta-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        
        .feature-card.visible, .showcase-content.visible, .testimonial-card.visible, .cta-card.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        @media (max-width: 768px) {
            .mobile-menu-button {
                display: block;
                background: none;
                border: none;
                color: var(--text-color);
                font-size: 1.5rem;
                cursor: pointer;
            }
            
            nav {
                display: none;
                width: 100%;
            }
            
            nav.active {
                display: block;
            }
            
            nav ul {
                flex-direction: column;
                align-items: center;
            }
            
            nav ul li {
                margin: 10px 0;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-menu-button {
                display: none;
            }
        }
    `;
    document.head.appendChild(style);
});