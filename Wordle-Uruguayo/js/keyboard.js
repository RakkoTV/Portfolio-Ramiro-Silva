// keyboard.js - Manejo del teclado virtual para Wordle Uruguayo

// Función para inicializar el teclado
export function initKeyboard(handleKeyInput) {
  // Obtener el elemento del teclado
  const keyboard = document.getElementById('keyboard');
  
  // Añadir event listener para el teclado virtual
  keyboard.addEventListener('click', (e) => {
    if (e.target.classList.contains('key')) {
      const key = e.target.getAttribute('data-key');
      handleKeyInput(key);
      
      // Añadir efecto visual de pulsación
      e.target.classList.add('pressed');
      setTimeout(() => {
        e.target.classList.remove('pressed');
      }, 100);
    }
  });
  
  // Añadir event listener para el teclado físico
  document.addEventListener('keydown', (e) => {
    let key = e.key.toUpperCase();
    
    // Mapear teclas especiales
    if (key === 'ENTER') {
      handleKeyInput('ENTER');
      highlightKey('ENTER');
    } else if (key === 'BACKSPACE' || key === 'DELETE') {
      handleKeyInput('BACKSPACE');
      highlightKey('BACKSPACE');
    } else if (/^[A-ZÑ]$/.test(key)) {
      handleKeyInput(key);
      highlightKey(key);
    }
  });
}

// Función para resaltar una tecla cuando se presiona en el teclado físico
function highlightKey(key) {
  const keyElement = document.querySelector(`.key[data-key="${key}"]`);
  if (keyElement) {
    keyElement.classList.add('pressed');
    setTimeout(() => {
      keyElement.classList.remove('pressed');
    }, 100);
  }
}

// Función para actualizar el estado visual de las teclas
export function updateKeyState(letter, state) {
  const keyElement = document.querySelector(`.key[data-key="${letter}"]`);
  
  if (keyElement) {
    const currentState = keyElement.getAttribute('data-state');
    
    // Solo actualizar si el nuevo estado es mejor que el actual
    if (!currentState || 
        (currentState === 'absent' && (state === 'present' || state === 'correct')) ||
        (currentState === 'present' && state === 'correct')) {
      
      keyElement.setAttribute('data-state', state);
      return true;
    }
  }
  
  return false;
}

// Función para reiniciar el estado del teclado
export function resetKeyboard() {
  const keys = document.querySelectorAll('.key');
  keys.forEach(key => {
    key.removeAttribute('data-state');
  });
}

// Función para deshabilitar el teclado
export function disableKeyboard() {
  const keys = document.querySelectorAll('.key');
  keys.forEach(key => {
    key.setAttribute('disabled', 'true');
    key.classList.add('disabled');
  });
}

// Función para habilitar el teclado
export function enableKeyboard() {
  const keys = document.querySelectorAll('.key');
  keys.forEach(key => {
    key.removeAttribute('disabled');
    key.classList.remove('disabled');
  });
}
