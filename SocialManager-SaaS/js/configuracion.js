// Archivo JavaScript para la página de configuración
document.addEventListener('DOMContentLoaded', function() {
    // Cargar el sidebar y marcar la opción de configuración como activa
    loadSidebar();
    
    // Inicializar las pestañas de configuración
    initTabs();
    
    // Cargar el estado de las conexiones sociales
    loadSocialConnections();
    
    // Inicializar los formularios
    initForms();
    
    // Función para cargar el sidebar
    function loadSidebar() {
        fetch('sidebar.html')
            .then(response => response.text())
            .then(data => {
                document.getElementById('sidebar-placeholder').innerHTML = data;
                
                // Marcar la opción de configuración como activa
                const menuItems = document.querySelectorAll('.sidebar-menu .menu-item');
                menuItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href') === 'configuracion.html') {
                        item.classList.add('active');
                    }
                });
                
                // Inicializar el toggle del sidebar
                const toggleBtn = document.getElementById('toggle-sidebar-btn');
                if (toggleBtn) {
                    toggleBtn.addEventListener('click', function() {
                        document.body.classList.toggle('sidebar-open');
                    });
                }
            })
            .catch(error => console.error('Error al cargar el sidebar:', error));
    }
    
    // Función para inicializar las pestañas
    function initTabs() {
        const tabButtons = document.querySelectorAll('[data-tab]');
        const tabContents = document.querySelectorAll('.tab-content');
        
        // Ocultar todos los contenidos de pestañas excepto el primero
        tabContents.forEach((content, index) => {
            if (index !== 0) {
                content.style.display = 'none';
            }
        });
        
        // Añadir eventos a los botones de pestañas
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Quitar la clase activa de todos los botones
                tabButtons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.style.borderBottom = 'none';
                    btn.style.color = 'inherit';
                });
                
                // Añadir la clase activa al botón clickeado
                this.classList.add('active');
                this.style.borderBottom = '3px solid var(--primary-color)';
                this.style.color = 'var(--primary-color)';
                
                // Ocultar todos los contenidos
                tabContents.forEach(content => {
                    content.style.display = 'none';
                });
                
                // Mostrar el contenido correspondiente
                const tabId = this.getAttribute('data-tab');
                document.getElementById(tabId).style.display = 'block';
            });
        });
    }
    
    // Función para cargar el estado de las conexiones sociales
    function loadSocialConnections() {
        fetch('php/social_connections.php?action=get_connections')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateConnectionsUI(data.connections);
                    
                    // Verificar si hay mensajes de éxito o error en la URL
                    const urlParams = new URLSearchParams(window.location.search);
                    if (urlParams.has('success') && urlParams.has('platform')) {
                        const platform = urlParams.get('platform');
                        alert(`Cuenta de ${platform} conectada correctamente`);
                        // Limpiar los parámetros de la URL
                        window.history.replaceState({}, document.title, 'configuracion.html');
                    } else if (urlParams.has('error')) {
                        const errorType = urlParams.get('error');
                        const platform = urlParams.get('platform') || '';
                        let errorMessage = 'Error al conectar la cuenta';
                        
                        switch(errorType) {
                            case 'token':
                                errorMessage = `Error al obtener el token de acceso para ${platform}`;
                                break;
                            case 'http':
                                errorMessage = `Error de comunicación con la API de ${platform}`;
                                break;
                            case 'db':
                                errorMessage = 'Error al guardar la información de conexión';
                                break;
                            case 'platform':
                                errorMessage = 'Plataforma no válida';
                                break;
                            case 'params':
                                errorMessage = 'Parámetros de autenticación incorrectos';
                                break;
                            case 'csrf':
                                errorMessage = 'Error de seguridad al conectar la cuenta. Inténtalo de nuevo.';
                                break;
                        }
                        
                        alert(errorMessage);
                        // Limpiar los parámetros de la URL
                        window.history.replaceState({}, document.title, 'configuracion.html');
                    }
                } else {
                    console.error('Error al cargar conexiones:', data.message);
                }
            })
            .catch(error => console.error('Error al cargar conexiones:', error));
    }
    
    // Función para actualizar la UI con el estado de las conexiones
    function updateConnectionsUI(connections) {
        const platforms = ['facebook', 'instagram', 'twitter', 'linkedin'];
        
        platforms.forEach(platform => {
            const connected = connections[platform] && connections[platform].connected;
            const connectButton = document.querySelector(`[data-platform="${platform}"] button`);
            
            if (connectButton) {
                if (connected) {
                    connectButton.innerHTML = '<i class="fas fa-check"></i> Conectado';
                    connectButton.style.background = '#e9ecef';
                    connectButton.style.color = 'var(--secondary-color)';
                } else {
                    connectButton.innerHTML = '<i class="fas fa-plug"></i> Conectar';
                    connectButton.style.background = 'var(--primary-gradient)';
                    connectButton.style.color = 'white';
                }
            }
        });
    }
    
    // Función para inicializar los formularios
    function initForms() {
        // Formulario de perfil
        const profileForm = document.getElementById('profile-form');
        if (profileForm) {
            profileForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Recoger datos del formulario
                const formData = new FormData(profileForm);
                
                // Enviar datos al servidor
                fetch('php/update_profile.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Perfil actualizado correctamente');
                    } else {
                        alert('Error al actualizar el perfil: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar el perfil');
                });
            });
        }
        
        // Botones de conexión de redes sociales
        const connectButtons = document.querySelectorAll('[data-platform] button');
        connectButtons.forEach(button => {
            button.addEventListener('click', function() {
                const platform = this.closest('[data-platform]').getAttribute('data-platform');
                
                // Si el botón dice "Conectado", desconectar
                if (this.innerHTML.includes('Conectado')) {
                    disconnectPlatform(platform);
                } else {
                    // Iniciar flujo de autenticación
                    connectPlatform(platform);
                }
            });
        });
        
        // Formulario de notificaciones
        const notificationsForm = document.getElementById('notifications-form');
        if (notificationsForm) {
            notificationsForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Recoger datos del formulario
                const formData = new FormData(notificationsForm);
                
                // Enviar datos al servidor
                fetch('php/update_notifications.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Preferencias de notificaciones actualizadas correctamente');
                    } else {
                        alert('Error al actualizar las preferencias: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar las preferencias');
                });
            });
        }
        
        // Formulario de seguridad
        const securityForm = document.getElementById('security-form');
        if (securityForm) {
            securityForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Recoger datos del formulario
                const formData = new FormData(securityForm);
                
                // Enviar datos al servidor
                fetch('php/update_security.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Configuración de seguridad actualizada correctamente');
                    } else {
                        alert('Error al actualizar la configuración: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar la configuración');
                });
            });
        }
        
        // Botones para cerrar sesiones remotas
        const logoutSessionButtons = document.querySelectorAll('.logout-session');
        logoutSessionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const sessionId = this.getAttribute('data-session-id');
                if (sessionId) {
                    if (confirm('¿Estás seguro de que deseas cerrar esta sesión?')) {
                        const formData = new FormData();
                        formData.append('session_id', sessionId);
                        
                        fetch('php/update_security.php', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                // Eliminar el elemento de la sesión del DOM
                                this.closest('.session-item').remove();
                                alert('Sesión cerrada correctamente');
                            } else {
                                alert('Error al cerrar la sesión: ' + data.message);
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error al cerrar la sesión');
                        });
                    }
                }
            });
        });
    }
    
    // Función para conectar una plataforma
    function connectPlatform(platform) {
        fetch(`php/social_connections.php?action=oauth_init&platform=${platform}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirigir al usuario a la URL de autenticación
                    window.location.href = data.auth_url;
                } else {
                    alert('Error al iniciar la conexión: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al iniciar la conexión');
            });
    }
    
    // Función para desconectar una plataforma
    function disconnectPlatform(platform) {
        if (confirm(`¿Estás seguro de que deseas desconectar tu cuenta de ${platform}?`)) {
            const formData = new FormData();
            formData.append('action', 'update_connection');
            formData.append('platform', platform);
            formData.append('connected', 0);
            
            fetch('php/social_connections.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar la UI
                    const button = document.querySelector(`[data-platform="${platform}"] button`);
                    if (button) {
                        button.innerHTML = '<i class="fas fa-plug"></i> Conectar';
                        button.style.background = 'var(--primary-gradient)';
                        button.style.color = 'white';
                    }
                    
                    alert(`Cuenta de ${platform} desconectada correctamente`);
                } else {
                    alert('Error al desconectar la cuenta: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al desconectar la cuenta');
            });
        }
    }
});