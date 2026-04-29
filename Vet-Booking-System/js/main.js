document.addEventListener('DOMContentLoaded', () => {

    // --- Mobile Menu ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        document.querySelectorAll('#mobile-menu a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // --- Sticky Header ---
    const header = document.getElementById('header');
    if(header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('py-2');
                header.classList.remove('py-3');
            } else {
                header.classList.add('py-3');
                header.classList.remove('py-2');
            }
        });
    }

    // --- Online Booking Form ---
    const bookingForm = document.getElementById('booking-form');
    const dateInput = document.getElementById('date');
    const timeSlotsContainer = document.getElementById('time-slots');
    const formFeedback = document.getElementById('form-feedback');
    let selectedTime = null;

    if (bookingForm) {
        // Set min date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);

        const availableTimes = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00', '18:00'];

        function generateTimeSlots() {
            timeSlotsContainer.innerHTML = '';
            availableTimes.forEach(time => {
                const button = document.createElement('button');
                button.type = 'button';
                button.textContent = time;
                button.className = 'p-2 border rounded-lg hover:bg-teal-100 focus:bg-teal-500 focus:text-white focus:outline-none transition';
                button.addEventListener('click', () => {
                    selectedTime = time;
                    document.querySelectorAll('#time-slots button').forEach(btn => {
                        btn.classList.remove('bg-teal-500', 'text-white');
                    });
                    button.classList.add('bg-teal-500', 'text-white');
                });
                timeSlotsContainer.appendChild(button);
            });
        }
        
        dateInput.addEventListener('change', generateTimeSlots);
        generateTimeSlots();

        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitButton = bookingForm.querySelector('button[type="submit"]');

            // Recoger datos del formulario
            const formData = {
                service: document.getElementById('service').value,
                date: dateInput.value,
                time: selectedTime,
                petName: document.getElementById('pet-name').value,
                ownerName: document.getElementById('owner-name').value
            };

            // Validación simple
            if (!formData.date || !formData.time || !formData.petName || !formData.ownerName) {
                showFeedback('Por favor, completa todos los campos, incluyendo fecha y hora.', 'error');
                return;
            }

            // Mostrar estado de carga
            submitButton.disabled = true;
            submitButton.classList.add('btn-loading');
            submitButton.querySelector('span').textContent = 'Enviando...';

            try {
                const response = await fetch('agendar_cita.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok) {
                    bookingForm.classList.add('hidden');
                    showFeedback(result.message, 'success');
                } else {
                    throw new Error(result.message || 'Ocurrió un error.');
                }

            } catch (error) {
                showFeedback(error.message, 'error');
            } finally {
                // Restaurar botón
                submitButton.disabled = false;
                submitButton.classList.remove('btn-loading');
                submitButton.querySelector('span').textContent = 'Confirmar Cita';
            }
        });

        function showFeedback(message, type) {
            formFeedback.textContent = message;
            formFeedback.className = `form-feedback ${type}`;
            formFeedback.style.display = 'block';
        }
    }

    // --- Testimonial Slider ---
    const slider = document.getElementById('testimonial-slider');
    const prevBtn = document.getElementById('prev-testimonial');
    const nextBtn = document.getElementById('next-testimonial');
    
    if (slider && prevBtn && nextBtn) {
        const testimonials = document.querySelectorAll('.testimonial-card');
        let currentIndex = 0;

        function updateSliderPosition() {
            slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        }
        
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % testimonials.length;
            updateSliderPosition();
        });

        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
            updateSliderPosition();
        });
        
        setInterval(() => {
            currentIndex = (currentIndex + 1) % testimonials.length;
            updateSliderPosition();
        }, 5000);
    }

    // --- Footer Year ---
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
