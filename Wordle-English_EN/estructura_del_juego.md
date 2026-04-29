# Diseño de la Estructura del Juego Wordle Uruguayo

## Tecnologías a utilizar
- HTML5, CSS3 y JavaScript para el desarrollo frontend
- Responsive design para adaptarse a dispositivos móviles y de escritorio
- LocalStorage para guardar estadísticas del jugador

## Estructura de archivos
```
wordle_uruguayo/
├── index.html              # Página principal del juego
├── css/
│   ├── style.css           # Estilos principales
│   └── animations.css      # Animaciones para las letras y teclado
├── js/
│   ├── app.js              # Lógica principal del juego
│   ├── words.js            # Base de datos de palabras uruguayas
│   ├── keyboard.js         # Manejo del teclado virtual
│   └── stats.js            # Manejo de estadísticas del jugador
├── assets/
│   ├── fonts/              # Fuentes personalizadas
│   ├── images/             # Imágenes e iconos
│   └── sounds/             # Efectos de sonido (opcional)
└── README.md               # Documentación del proyecto
```

## Funcionalidades principales

### 1. Mecánica del juego
- El jugador tiene 6 intentos para adivinar una palabra de 5 letras
- Después de cada intento, se muestra retroalimentación visual:
  - Verde: Letra correcta en posición correcta
  - Amarillo: Letra correcta en posición incorrecta
  - Gris: Letra no está en la palabra

### 2. Interfaz de usuario
- Cuadrícula de 6 filas x 5 columnas para los intentos
- Teclado virtual en pantalla
- Botón de instrucciones
- Botón para ver estadísticas
- Botón para compartir resultados
- Modo oscuro/claro (toggle)

### 3. Características especiales
- Diccionario de palabras exclusivamente uruguayas
- Tooltip con definición de la palabra al finalizar el juego
- Animaciones para las letras al ser ingresadas
- Mensaje de felicitación con temática uruguaya al ganar

### 4. Estadísticas del jugador
- Número de juegos jugados
- Porcentaje de victorias
- Racha actual de victorias
- Mejor racha
- Distribución de intentos (histograma)

### 5. Almacenamiento local
- Guardar progreso del juego actual
- Guardar estadísticas del jugador
- Guardar preferencias (modo oscuro/claro)

### 6. Características adicionales (opcionales)
- Compartir resultados en redes sociales
- Palabra del día (cambia cada 24 horas)
- Modo de juego ilimitado (palabras aleatorias)
- Pistas contextuales sobre la cultura uruguaya

## Flujo del juego
1. El jugador carga la página
2. Se selecciona una palabra aleatoria del diccionario uruguayo
3. El jugador introduce letras usando el teclado físico o virtual
4. Después de cada palabra completa, se muestra la retroalimentación
5. El juego termina cuando:
   - El jugador adivina la palabra (victoria)
   - El jugador agota los 6 intentos (derrota)
6. Se muestra la palabra correcta y su significado
7. Se actualizan las estadísticas
8. Se ofrece la opción de jugar de nuevo o compartir resultados

## Consideraciones de diseño
- Paleta de colores inspirada en la bandera uruguaya (azul, blanco, amarillo del sol)
- Tipografía clara y legible
- Diseño minimalista y moderno
- Animaciones sutiles para mejorar la experiencia de usuario
- Mensajes y textos en español con modismos uruguayos
