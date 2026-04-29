<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VitalCan - Veterinaria de Confianza en Montevideo</title>
    <meta name="description" content="VitalCan, tu veterinaria de confianza en Montevideo. Ofrecemos consultas, vacunación, cirugía, urgencias 24hs y más.">
    <meta name="keywords" content="veterinaria, montevideo, pocitos, urgencias, mascota, perro, gato">
    
    <!-- Open Graph -->
    <meta property="og:title" content="VitalCan - Veterinaria de Confianza en Montevideo">
    <meta property="og:description" content="Tecnología y calidez para tu mascota en el corazón de Montevideo.">
    <meta property="og:image" content="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=2670&auto=format&fit=crop">
    <meta property="og:url" content="URL_DE_TU_SITIO_WEB">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts: Poppins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- Custom Styles -->
    <link rel="stylesheet" href="css/custom.css">
</head>
<body class="bg-gray-50 text-gray-800">

    <!-- Header & Navigation -->
    <header id="header" class="bg-white shadow-md fixed w-full z-50 top-0 transition-all duration-300">
        <nav class="container mx-auto px-6 py-3 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold text-teal-500 flex items-center">
                <i class="fas fa-paw mr-2"></i>
                VitalCan
            </a>
            <div class="hidden md:flex space-x-6 items-center">
                <a href="#servicios" class="text-gray-600 hover:text-teal-500 transition">Servicios</a>
                <a href="#equipo" class="text-gray-600 hover:text-teal-500 transition">Equipo</a>
                <a href="#testimonios" class="text-gray-600 hover:text-teal-500 transition">Testimonios</a>
                <a href="#contacto" class="text-gray-600 hover:text-teal-500 transition">Contacto</a>
            </div>
            <a href="#agenda" class="hidden md:inline-block bg-teal-500 text-white font-semibold px-5 py-2 rounded-full hover:bg-teal-600 cta-button">
                Agendar Cita
            </a>
            <button id="mobile-menu-button" class="md:hidden text-2xl">
                <i class="fas fa-bars"></i>
            </button>
        </nav>
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden bg-white">
            <a href="#servicios" class="block py-2 px-6 text-sm hover:bg-gray-100">Servicios</a>
            <a href="#equipo" class="block py-2 px-6 text-sm hover:bg-gray-100">Equipo</a>
            <a href="#testimonios" class="block py-2 px-6 text-sm hover:bg-gray-100">Testimonios</a>
            <a href="#contacto" class="block py-2 px-6 text-sm hover:bg-gray-100">Contacto</a>
            <a href="#agenda" class="block py-3 px-6 text-sm bg-teal-500 text-white text-center font-semibold">Agendar Cita</a>
        </div>
    </header>

    <main>
        <!-- Hero Section -->
        <section class="hero-bg h-screen flex items-center justify-center text-white text-center">
            <div class="container mx-auto px-6">
                <h1 class="text-4xl md:text-6xl font-bold mb-4 leading-tight" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Cuidamos de los que más quieres</h1>
                <p class="text-lg md:text-2xl mb-8 font-light" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">Tecnología y calidez para tu mascota en el corazón de Montevideo.</p>
                <a href="#agenda" class="bg-teal-500 text-white font-bold py-4 px-8 rounded-full text-lg hover:bg-teal-600 cta-button">
                    Reservar una Cita Ahora
                </a>
            </div>
        </section>

        <!-- Services Section -->
        <section id="servicios" class="py-20">
            <div class="container mx-auto px-6">
                <h2 class="text-4xl font-bold text-center section-title">Nuestros Servicios</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-10">
                    <!-- Service Card 1 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-stethoscope"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Consultas Generales</h3>
                        <p class="text-gray-600">Chequeos completos y diagnóstico para mantener a tu mascota saludable y feliz.</p>
                    </div>
                    <!-- Service Card 2 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-syringe"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Vacunación</h3>
                        <p class="text-gray-600">Planes de vacunación personalizados para proteger a tu compañero de vida.</p>
                    </div>
                    <!-- Service Card 3 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-user-md"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Cirugía Especializada</h3>
                        <p class="text-gray-600">Quirófano moderno y equipo experto para procedimientos seguros y eficaces.</p>
                    </div>
                    <!-- Service Card 4 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-cut"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Peluquería y Estética</h3>
                        <p class="text-gray-600">Baños, cortes y tratamientos para que tu mascota luzca y se sienta genial.</p>
                    </div>
                    <!-- Service Card 5 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-heartbeat"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Urgencias 24hs</h3>
                        <p class="text-gray-600">Atención inmediata para emergencias. Estamos siempre disponibles para ti.</p>
                    </div>
                    <!-- Service Card 6 -->
                    <div class="service-card bg-white p-8 rounded-xl shadow-lg text-center">
                        <div class="text-5xl text-teal-500 mb-4"><i class="fas fa-flask"></i></div>
                        <h3 class="text-xl font-semibold mb-2">Laboratorio Propio</h3>
                        <p class="text-gray-600">Resultados rápidos y precisos para un diagnóstico certero y oportuno.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Online Booking Section -->
        <section id="agenda" class="py-20 bg-teal-500 text-white">
            <div class="container mx-auto px-6">
                <h2 class="text-4xl font-bold text-center section-title !text-white after:!bg-white">Agenda tu Cita Online</h2>
                <div class="max-w-2xl mx-auto mt-10 bg-white text-gray-800 p-8 rounded-2xl shadow-2xl">
                    <form id="booking-form">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label for="service" class="block mb-2 font-semibold">Servicio</label>
                                <select id="service" class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400">
                                    <option>Consulta General</option>
                                    <option>Vacunación</option>
                                    <option>Peluquería</option>
                                    <option>Revisión Quirúrgica</option>
                                </select>
                            </div>
                            <div>
                                <label for="date" class="block mb-2 font-semibold">Fecha</label>
                                <input type="date" id="date" class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400">
                            </div>
                        </div>
                        <div class="mt-6">
                            <label class="block mb-2 font-semibold">Horarios Disponibles</label>
                            <div id="time-slots" class="grid grid-cols-3 sm:grid-cols-4 gap-2">
                                <!-- Time slots will be generated by JS -->
                            </div>
                        </div>
                        <div class="mt-6">
                            <label for="pet-name" class="block mb-2 font-semibold">Nombre de tu Mascota</label>
                            <input type="text" id="pet-name" placeholder="Ej: Rocky" class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400">
                        </div>
                         <div class="mt-6">
                            <label for="owner-name" class="block mb-2 font-semibold">Tu Nombre y Apellido</label>
                            <input type="text" id="owner-name" placeholder="Ej: Ana Rodríguez" class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-teal-400">
                        </div>
                        <div class="mt-8 text-center">
                            <button type="submit" class="bg-orange-500 text-white font-bold py-3 px-10 rounded-full text-lg hover:bg-orange-600 cta-button w-full md:w-auto">
                                <span>Confirmar Cita</span>
                            </button>
                        </div>
                    </form>
                    <div id="form-feedback" class="form-feedback"></div>
                </div>
            </div>
        </section>

        <!-- Team Section -->
        <section id="equipo" class="py-20">
            <div class="container mx-auto px-6">
                <h2 class="text-4xl font-bold text-center section-title">Conoce a Nuestro Equipo</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 mt-10">
                    <!-- Team Member 1 -->
                    <div class="team-card bg-white rounded-xl shadow-lg overflow-hidden text-center">
                        <img src="img/team-herrera.jpg" alt="Foto de la Dra. Sofía Herrera" class="w-full h-64 object-cover">
                        <div class="p-6">
                            <h3 class="text-xl font-semibold text-teal-600">Dra. Sofía Herrera</h3>
                            <p class="text-gray-500 mb-2">Directora y Cirujana</p>
                            <p class="text-sm text-gray-600">Con más de 15 años de experiencia, la Dra. Herrera lidera nuestro equipo con pasión y dedicación.</p>
                        </div>
                    </div>
                    <!-- Team Member 2 -->
                    <div class="team-card bg-white rounded-xl shadow-lg overflow-hidden text-center">
                        <img src="https://ui-avatars.com/api/?name=Mateo+Vidal&size=256&background=14b8a6&color=ffffff&font-size=0.4" alt="Avatar del Dr. Mateo Vidal" class="w-full h-64 object-cover">
                        <div class="p-6">
                            <h3 class="text-xl font-semibold text-teal-600">Dr. Mateo Vidal</h3>
                            <p class="text-gray-500 mb-2">Clínica General y Exóticos</p>
                            <p class="text-sm text-gray-600">Especialista en medicina interna y un apasionado por el cuidado de animales exóticos.</p>
                        </div>
                    </div>
                    <!-- Team Member 3 -->
                    <div class="team-card bg-white rounded-xl shadow-lg overflow-hidden text-center">
                        <img src="img/team-gomez.jpg" alt="Foto de la Dra. Valentina Gómez" class="w-full h-64 object-cover">
                        <div class="p-6">
                            <h3 class="text-xl font-semibold text-teal-600">Dra. Valentina Gómez</h3>
                            <p class="text-gray-500 mb-2">Dermatología y Nutrición</p>
                            <p class="text-sm text-gray-600">Ayuda a tus mascotas a sentirse bien por dentro y por fuera con sus planes de nutrición y cuidado de la piel.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Testimonials Section -->
        <section id="testimonios" class="py-20 bg-gray-100">
            <div class="container mx-auto px-6">
                <h2 class="text-4xl font-bold text-center section-title">Lo que dicen nuestros clientes</h2>
                <div class="relative max-w-3xl mx-auto mt-10">
                    <div id="testimonial-container" class="overflow-hidden">
                        <div id="testimonial-slider" class="flex transition-transform duration-500 ease-in-out">
                            <!-- Testimonial 1 -->
                            <div class="testimonial-card flex-shrink-0 w-full bg-white p-8 rounded-xl shadow-lg text-center">
                                <img src="img/testimonial-1.png" alt="Avatar de Martina Pérez" class="w-20 h-20 rounded-full mx-auto mb-4">
                                <p class="text-gray-600 italic mb-4">"La atención en VitalCan es insuperable. Se nota que aman lo que hacen. Mi perro Rocky siempre sale feliz de sus controles. ¡Totalmente recomendados!"</p>
                                <h4 class="font-semibold text-teal-600">Martina Pérez</h4>
                                <p class="text-sm text-gray-500">Dueña de Rocky</p>
                            </div>
                            <!-- Testimonial 2 -->
                             <div class="testimonial-card flex-shrink-0 w-full bg-white p-8 rounded-xl shadow-lg text-center">
                                <img src="https://rakkotech.uy/Referencia/35/img/testimonial-2.png" alt="Avatar de Javier Gutiérrez" class="w-20 h-20 rounded-full mx-auto mb-4">
                                <p class="text-gray-600 italic mb-4">"Tuvimos una urgencia de madrugada y nos salvaron. El equipo de guardia fue increíblemente profesional y empático. Eternamente agradecido."</p>
                                <h4 class="font-semibold text-teal-600">Javier Gutiérrez</h4>
                                <p class="text-sm text-gray-500">Dueño de Luna</p>
                            </div>
                            <!-- Testimonial 3 -->
                             <div class="testimonial-card flex-shrink-0 w-full bg-white p-8 rounded-xl shadow-lg text-center">
                                <img src="https://ui-avatars.com/api/?name=Carla+Romano&size=80&background=a78bfa&color=ffffff" alt="Avatar de Carla Romano" class="w-20 h-20 rounded-full mx-auto mb-4">
                                <p class="text-gray-600 italic mb-4">"El mejor servicio de peluquería canina de Montevideo. Mi caniche siempre queda impecable y, lo más importante, tranquilo durante todo el proceso."</p>
                                <h4 class="font-semibold text-teal-600">Carla Romano</h4>
                                <p class="text-sm text-gray-500">Dueña de Tobi</p>
                            </div>
                        </div>
                    </div>
                    <button id="prev-testimonial" class="absolute top-1/2 left-0 -translate-y-1/2 -translate-x-12 bg-white p-2 rounded-full shadow-md text-teal-500 hover:bg-gray-200 text-2xl"><i class="fas fa-chevron-left"></i></button>
                    <button id="next-testimonial" class="absolute top-1/2 right-0 -translate-y-1/2 translate-x-12 bg-white p-2 rounded-full shadow-md text-teal-500 hover:bg-gray-200 text-2xl"><i class="fas fa-chevron-right"></i></button>
                </div>
            </div>
        </section>

        <!-- Contact & Location Section -->
        <section id="contacto" class="py-20">
            <div class="container mx-auto px-6">
                <h2 class="text-4xl font-bold text-center section-title">Contáctanos</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-12 mt-10 items-center">
                    <div>
                        <h3 class="text-2xl font-semibold mb-4 text-teal-600">Visítanos en Pocitos</h3>
                        <p class="mb-4 text-gray-600">Estamos ubicados en una zona accesible para tu comodidad. ¡Te esperamos!</p>
                        <div class="space-y-4">
                            <p class="flex items-center"><i class="fas fa-map-marker-alt text-teal-500 w-6 mr-2"></i> Av. Brasil 2785, Pocitos, Montevideo</p>
                            <p class="flex items-center"><i class="fas fa-phone text-teal-500 w-6 mr-2"></i> <a href="tel:+59827091234" class="hover:underline">(+598) 2709 1234</a></p>
                            <p class="flex items-center"><i class="fas fa-mobile-alt text-red-500 w-6 mr-2 font-bold"></i> <span class="font-bold text-red-500">Urgencias:</span> <a href="tel:+598099123456" class="hover:underline ml-1 text-gray-800">(+598) 099 123 456</a></p>
                            <p class="flex items-start"><i class="fas fa-clock text-teal-500 w-6 mr-2 mt-1"></i> <span><span class="font-semibold">Lunes a Viernes:</span> 9:00 - 20:00<br><span class="font-semibold">Sábados:</span> 9:00 - 14:00</span></p>
                        </div>
                    </div>
                    <div class="rounded-xl overflow-hidden shadow-2xl h-96">
                        <iframe 
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3271.933339831518!2d-56.15109288476255!3d-34.90812298038164!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x959f8101f3651c3b%3A0x1649363a8425d742!2sAv.%20Brasil%202785%2C%2011300%20Montevideo%2C%20Departamento%20de%20Montevideo%2C%20Uruguay!5e0!3m2!1ses-419!2suy!4v1678886451234" 
                            width="100%" 
                            height="100%" 
                            style="border:0;" 
                            allowfullscreen="" 
                            loading="lazy" 
                            referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white pt-10 pb-6">
        <div class="container mx-auto px-6 text-center">
            <h3 class="text-2xl font-bold text-teal-400 mb-2">VitalCan</h3>
            <p class="mb-6">Tu veterinaria de confianza en Montevideo.</p>
            <div class="flex justify-center space-x-6 mb-6">
                <a href="#" class="text-2xl hover:text-teal-400 transition"><i class="fab fa-facebook-f"></i></a>
                <a href="#" class="text-2xl hover:text-teal-400 transition"><i class="fab fa-instagram"></i></a>
                <a href="#" class="text-2xl hover:text-teal-400 transition"><i class="fab fa-whatsapp"></i></a>
            </div>
            <p class="text-sm text-gray-400">&copy; <span id="year"></span> VitalCan Montevideo. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>

</body>
</html>