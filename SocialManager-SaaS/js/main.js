// Funcionalidad para el menú de navegación responsive
document.addEventListener('DOMContentLoaded', function() {
    // Variables
    const header = document.querySelector('.header');
    
    // Función para manejar el scroll y añadir sombra al header
    function handleScroll() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
    
    // Event listeners
    window.addEventListener('scroll', handleScroll);
    
    // Navegación suave para los enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Formulario de contacto
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Obtener los valores del formulario
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Aquí normalmente enviarías los datos a un servidor
            // Por ahora, solo mostraremos un mensaje de éxito
            alert(`Gracias ${name} por tu mensaje. Te contactaremos pronto en ${email}.`);
            
            // Limpiar el formulario
            contactForm.reset();
        });
    }
    
    // Simulación de testimonios deslizantes
    const testimonials = document.querySelectorAll('.testimonial');
    let currentTestimonial = 0;
    
    // Función para cambiar testimonios (en una implementación real usaríamos un carrusel)
    function rotateTestimonials() {
        // Esta es una implementación básica, en producción usaríamos una biblioteca de carrusel
        if (testimonials.length > 1) {
            testimonials.forEach(testimonial => {
                testimonial.style.opacity = 0.3;
            });
            
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            testimonials[currentTestimonial].style.opacity = 1;
        }
    }
    
    // Cambiar testimonios cada 5 segundos si hay más de uno
    if (testimonials.length > 1) {
        testimonials.forEach((testimonial, index) => {
            if (index !== 0) {
                testimonial.style.opacity = 0.3;
            }
        });
        
        setInterval(rotateTestimonials, 5000);
    }
    
    // Animación para las tarjetas de características al hacer scroll
    const featureCards = document.querySelectorAll('.feature-card');
    
    function checkScroll() {
        featureCards.forEach(card => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (cardPosition < screenPosition) {
                card.classList.add('animate');
            }
        });
    }
    
    // Verificar posición inicial
    checkScroll();
    
    // Verificar al hacer scroll
    window.addEventListener('scroll', checkScroll);
});

// Añadir clase CSS para animación
document.head.insertAdjacentHTML('beforeend', `
<style>
.feature-card {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease, transform 0.5s ease;
}

.feature-card.animate {
    opacity: 1;
    transform: translateY(0);
}
</style>
`);


// Funcionalidad para el toggle del sidebar en el dashboard
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggle-sidebar-btn');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-open');
        });
    }
});