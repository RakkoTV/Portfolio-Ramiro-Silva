// Archivo JavaScript para manejar la funcionalidad del sidebar
document.addEventListener('DOMContentLoaded', function() {
    // Marcar el elemento de menú activo basado en la URL actual
    function setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1);
        
        // Seleccionar todos los elementos del menú
        const menuItems = document.querySelectorAll('.sidebar-menu .menu-item');
        
        // Quitar la clase active de todos los elementos
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
        
        // Añadir la clase active al elemento correspondiente a la página actual
        menuItems.forEach(item => {
            const href = item.getAttribute('href');
            // Comprobar si la URL actual coincide con el href del elemento de menú
            // o si estamos en la página de inicio y el href es dashboard.html
            if (href === filename || 
                (filename === '' && href === 'dashboard.html') ||
                (filename === 'audiencia.html' && href === 'audiencia.html')) {
                item.classList.add('active');
            }
        });
    }
    
    // Inicializar el sidebar
    function initSidebar() {
        // Marcar el elemento de menú activo
        setActiveMenuItem();
        
        // Manejar el toggle del sidebar en dispositivos móviles
        const toggleBtn = document.getElementById('toggle-sidebar-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                document.body.classList.toggle('sidebar-open');
            });
        }
    }
    
    // Si el sidebar se carga dinámicamente, esperar a que esté disponible
    if (document.querySelector('.sidebar')) {
        initSidebar();
    } else {
        // Observar cambios en el DOM para detectar cuando se carga el sidebar
        const observer = new MutationObserver(function(mutations) {
            if (document.querySelector('.sidebar')) {
                initSidebar();
                observer.disconnect();
            }
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    }
});