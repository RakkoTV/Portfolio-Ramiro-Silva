// app.js - Lógica principal del juego Wordle Uruguayo
import { palabrasWordle } from './words.js';

// Estado del juego
const gameState = {
  currentRow: 0,
  currentTile: 0,
  gameOver: false,
  solution: '',
  solutionDefinition: '',
  guesses: [],
  keyboardState: {},
  hintsUsed: 0,
  stats: {
    gamesPlayed: 0,
    gamesWon: 0,
    currentStreak: 0,
    maxStreak: 0,
    hintsUsed: 0,
    guessDistribution: {
      1: 0,
      2: 0,
      3: 0,
      4: 0,
      5: 0,
      6: 0
    },
    lastPlayed: null,
    lastCompleted: null
  }
};

// Elementos DOM
const gameBoard = document.getElementById('game-board');
const keyboard = document.getElementById('keyboard');
const toast = document.getElementById('toast');
const instructionsModal = document.getElementById('instructions-modal');
const statsModal = document.getElementById('stats-modal');
const gameOverModal = document.getElementById('game-over-modal');
const btnInfo = document.getElementById('btn-info');
const btnStats = document.getElementById('btn-stats');
const btnTheme = document.getElementById('btn-theme');
const shareButton = document.getElementById('share-button');
const gameOverShareButton = document.getElementById('game-over-share-button');

// Inicialización del juego
function initGame() {
  loadStats();
  loadTheme();
  checkNewDay();
  setupEventListeners();
  setupHintSystem();
  
  // Mostrar instrucciones si es la primera vez que juega
  if (!localStorage.getItem('wordleUruguayoPlayed')) {
    localStorage.setItem('wordleUruguayoPlayed', 'true');
    showInstructions();
  }
}

// Cargar estadísticas desde localStorage
function loadStats() {
  const savedStats = localStorage.getItem('wordleUruguayoStats');
  if (savedStats) {
    gameState.stats = JSON.parse(savedStats);
  }
  updateStatsDisplay();
}

// Guardar estadísticas en localStorage
function saveStats() {
  localStorage.setItem('wordleUruguayoStats', JSON.stringify(gameState.stats));
  updateStatsDisplay();
}

function setupHintSystem() {
  const hintDefinition = document.getElementById('hint-definition');
  hintDefinition.style.display = 'none';
}

function showHint() {
  const hintModal = document.getElementById('hint-modal');
  const hintDefinition = document.getElementById('hint-definition');
  const confirmHint = document.getElementById('confirm-hint');

  if (confirmHint.textContent === 'Mostrar pista') {
    gameState.hintsUsed++;
    gameState.stats.hintsUsed++;
    hintDefinition.textContent = gameState.solutionDefinition;
    hintDefinition.style.display = 'block';
    confirmHint.textContent = 'Cerrar';
    showToast('¡Has usado una pista! Esto afectará tu puntuación.', 2000);
    saveStats();
  } else {
    hintModal.style.display = 'none';
    confirmHint.textContent = 'Mostrar pista';
    hintDefinition.style.display = 'none';
  }
}

// Actualizar visualización de estadísticas
function updateStatsDisplay() {
  document.getElementById('games-played').textContent = gameState.stats.gamesPlayed;
  document.getElementById('summary-games-played').textContent = gameState.stats.gamesPlayed;
  
  const winPercentage = gameState.stats.gamesPlayed > 0 
    ? Math.round((gameState.stats.gamesWon / gameState.stats.gamesPlayed) * 100) 
    : 0;
  document.getElementById('win-percentage').textContent = winPercentage;
  document.getElementById('summary-win-percentage').textContent = winPercentage;
  
  document.getElementById('current-streak').textContent = gameState.stats.currentStreak;
  document.getElementById('summary-current-streak').textContent = gameState.stats.currentStreak;
  
  document.getElementById('max-streak').textContent = gameState.stats.maxStreak;
  
  // Actualizar distribución de intentos
  const guessDistribution = document.getElementById('guess-distribution');
  guessDistribution.innerHTML = '';
  
  const maxGuesses = Math.max(...Object.values(gameState.stats.guessDistribution), 1);
  
  for (let i = 1; i <= 6; i++) {
    const count = gameState.stats.guessDistribution[i];
    const percentage = Math.round((count / maxGuesses) * 100);
    
    const row = document.createElement('div');
    row.className = 'guess-row';
    
    const label = document.createElement('div');
    label.className = 'guess-label';
    label.textContent = i;
    
    const bar = document.createElement('div');
    bar.className = 'guess-bar';
    bar.style.width = `${Math.max(percentage, 5)}%`;
    bar.textContent = count;
    
    row.appendChild(label);
    row.appendChild(bar);
    guessDistribution.appendChild(row);
  }
  
  // Actualizar cuenta regresiva
  updateCountdown();
}

// Verificar si es un nuevo día y reiniciar el juego
function checkNewDay() {
  const today = new Date().toLocaleDateString();
  const lastPlayed = gameState.stats.lastPlayed;
  
  if (lastPlayed !== today) {
    // Es un nuevo día, reiniciar el juego
    resetGame();
    gameState.stats.lastPlayed = today;
    saveStats();
  } else {
    // Cargar el juego guardado
    loadGameState();
  }
}

// Reiniciar el juego con una nueva palabra
function resetGame() {
  gameState.currentRow = 0;
  gameState.currentTile = 0;
  gameState.gameOver = false;
  gameState.guesses = [];
  gameState.keyboardState = {};
  
  // Seleccionar una palabra aleatoria
  const randomIndex = Math.floor(Math.random() * palabrasWordle.length);
  gameState.solution = palabrasWordle[randomIndex].palabra;
  gameState.solutionDefinition = palabrasWordle[randomIndex].definicion;
  
  // Limpiar el tablero
  const tiles = document.querySelectorAll('.tile');
  tiles.forEach(tile => {
    tile.textContent = '';
    tile.setAttribute('data-state', 'empty');
  });
  
  // Reiniciar el teclado
  const keys = document.querySelectorAll('.key');
  keys.forEach(key => {
    key.removeAttribute('data-state');
  });
  
  // Guardar el estado inicial
  saveGameState();
}

// Guardar el estado actual del juego
function saveGameState() {
  const gameStateData = {
    currentRow: gameState.currentRow,
    currentTile: gameState.currentTile,
    gameOver: gameState.gameOver,
    solution: gameState.solution,
    guesses: gameState.guesses,
    keyboardState: gameState.keyboardState
  };
  
  localStorage.setItem('wordleUruguayoGameState', JSON.stringify(gameStateData));
}

// Cargar el estado guardado del juego
function loadGameState() {
  const savedState = localStorage.getItem('wordleUruguayoGameState');
  
  if (savedState) {
    const parsedState = JSON.parse(savedState);
    
    gameState.currentRow = parsedState.currentRow;
    gameState.currentTile = parsedState.currentTile;
    gameState.gameOver = parsedState.gameOver;
    gameState.solution = parsedState.solution;
    gameState.guesses = parsedState.guesses;
    gameState.keyboardState = parsedState.keyboardState;
    
    // Restaurar el tablero
    for (let row = 0; row < gameState.guesses.length; row++) {
      const guess = gameState.guesses[row];
      for (let col = 0; col < guess.length; col++) {
        const tile = getTileElement(row, col);
        const letter = guess[col];
        const state = getLetterState(letter, col, gameState.solution);
        
        tile.textContent = letter;
        tile.setAttribute('data-state', state);
      }
    }
    
    // Restaurar el teclado
    for (const [key, state] of Object.entries(gameState.keyboardState)) {
      const keyElement = document.querySelector(`.key[data-key="${key}"]`);
      if (keyElement) {
        keyElement.setAttribute('data-state', state);
      }
    }
    
    // Si el juego ya terminó, mostrar el modal correspondiente
    if (gameState.gameOver) {
      const won = gameState.guesses.length > 0 && 
                 gameState.guesses[gameState.guesses.length - 1].join('') === gameState.solution;
      
      setTimeout(() => {
        showGameOverModal(won);
      }, 1500);
    }
  } else {
    // No hay estado guardado, iniciar un nuevo juego
    resetGame();
  }
}

// Configurar event listeners
function setupEventListeners() {
  // Configurar el botón de pista
  const btnHint = document.getElementById('btn-hint');
  const hintModal = document.getElementById('hint-modal');
  const confirmHint = document.getElementById('confirm-hint');
  const cancelHint = document.getElementById('cancel-hint');
  const closeHint = hintModal.querySelector('.close-button');

  btnHint.addEventListener('click', () => {
    if (!gameState.gameOver) {
      hintModal.style.display = 'block';
    }
  });

  confirmHint.addEventListener('click', showHint);

  cancelHint.addEventListener('click', () => {
    hintModal.style.display = 'none';
  });

  closeHint.addEventListener('click', () => {
    hintModal.style.display = 'none';
  });

  window.addEventListener('click', (e) => {
    if (e.target === hintModal) {
      hintModal.style.display = 'none';
    }
  });
  // Event listeners para el teclado físico
  document.addEventListener('keydown', handleKeyPress);
  
  // Event listeners para el teclado virtual
  keyboard.addEventListener('click', (e) => {
    if (e.target.classList.contains('key')) {
      const key = e.target.getAttribute('data-key');
      handleKeyInput(key);
    }
  });
  
  // Event listeners para botones y modales
  btnInfo.addEventListener('click', showInstructions);
  btnStats.addEventListener('click', showStats);
  btnTheme.addEventListener('click', toggleTheme);
  
  shareButton.addEventListener('click', shareResults);
  gameOverShareButton.addEventListener('click', shareResults);
  
  // Cerrar modales
  document.querySelectorAll('.close-button').forEach(button => {
    button.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal');
      closeModal(modal);
    });
  });
  
  // Cerrar modales al hacer clic fuera
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });
}

// Manejar pulsación de tecla física
function handleKeyPress(e) {
  if (gameState.gameOver) return;
  
  const key = e.key.toUpperCase();
  
  if (key === 'ENTER') {
    handleKeyInput('ENTER');
  } else if (key === 'BACKSPACE' || key === 'DELETE') {
    handleKeyInput('BACKSPACE');
  } else if (/^[A-Z]$/.test(key)) {
    handleKeyInput(key);
  }
  e.preventDefault();
}

// Manejar input de teclado (físico o virtual)
function handleKeyInput(key) {
  if (gameState.gameOver) return;
  
  if (key === 'ENTER') {
    submitGuess();
  } else if (key === 'BACKSPACE') {
    deleteLetter();
  } else if (/^[A-ZÑ]$/.test(key) && gameState.currentTile < 5) {
    addLetter(key);
  }
}

// Añadir letra al tablero
function addLetter(letter) {
  if (gameState.currentTile < 5) {
    const tile = getTileElement(gameState.currentRow, gameState.currentTile);
    tile.textContent = letter;
    tile.setAttribute('data-state', 'active');
    
    gameState.currentTile++;
  }
}

// Borrar letra del tablero
function deleteLetter() {
  if (gameState.currentTile > 0) {
    gameState.currentTile--;
    
    const tile = getTileElement(gameState.currentRow, gameState.currentTile);
    tile.textContent = '';
    tile.setAttribute('data-state', 'empty');
  }
}

// Enviar intento
function submitGuess() {
  if (gameState.currentTile !== 5) {
    showToast('La palabra debe tener 5 letras');
    animateRowShake(gameState.currentRow);
    return;
  }
  
  const guess = [];
  for (let i = 0; i < 5; i++) {
    const tile = getTileElement(gameState.currentRow, i);
    guess.push(tile.textContent);
  }
  
  const guessWord = guess.join('');
  
  // Verificar si la palabra está en la lista
  const isValidWord = palabrasWordle.some(word => word.palabra.toUpperCase() === guessWord);
  
  if (!isValidWord) {
    showToast('Palabra no válida');
    animateRowShake(gameState.currentRow);
  }
  
  // Evaluar el intento
  gameState.guesses.push(guess);
  
  // Animar revelación de las letras
  revealRow(gameState.currentRow, guess);
  
  // Verificar si ganó
  if (guessWord === gameState.solution) {
    gameState.gameOver = true;
    
    // Actualizar estadísticas
    gameState.stats.gamesPlayed++;
    gameState.stats.gamesWon++;
    gameState.stats.currentStreak++;
    gameState.stats.maxStreak = Math.max(gameState.stats.maxStreak, gameState.stats.currentStreak);
    gameState.stats.guessDistribution[gameState.currentRow + 1]++;
    gameState.stats.lastCompleted = new Date().toLocaleDateString();
    
    saveStats();
    saveGameState();
    
    // Mostrar modal de victoria después de la animación
    setTimeout(() => {
      showGameOverModal(true);
    }, 1500);
    
    return;
  }
  
  // Verificar si perdió (usó todos los intentos)
  if (gameState.currentRow === 5) {
    gameState.gameOver = true;
    
    // Actualizar estadísticas
    gameState.stats.gamesPlayed++;
    gameState.stats.currentStreak = 0;
    gameState.stats.lastCompleted = new Date().toLocaleDateString();
    
    saveStats();
    saveGameState();
    
    // Mostrar modal de derrota después de la animación
    setTimeout(() => {
      showGameOverModal(false);
    }, 1500);
    
    return;
  }
  
  // Continuar al siguiente intento
  gameState.currentRow++;
  gameState.currentTile = 0;
  
  saveGameState();
}

// Revelar fila con animación
function revealRow(row, guess) {
  const solution = gameState.solution;
  
  for (let i = 0; i < 5; i++) {
    const tile = getTileElement(row, i);
    const letter = guess[i];
    
    // Retrasar la revelación de cada letra
    setTimeout(() => {
      const state = getLetterState(letter, i, solution);
      
      // Actualizar el estado de la tecla en el teclado
      updateKeyboardState(letter, state);
      
      // Animar la revelación
      tile.setAttribute('data-animation', 'flip-in');
      
      setTimeout(() => {
        tile.setAttribute('data-state', state);
        tile.setAttribute('data-animation', 'flip-out');
        
        setTimeout(() => {
          tile.removeAttribute('data-animation');
        }, 250);
      }, 250);
      
    }, i * 500);
  }
}

// Determinar el estado de una letra (correct, present, absent)
function getLetterState(letter, position, solution) {
  solution = solution.toUpperCase();
  if (solution[position] === letter) {
    return 'correct';
  }
  
  if (solution.includes(letter)) {
    // Contar cuántas veces aparece la letra en la solución
    const letterCount = solution.split('').filter(l => l === letter).length;
    
    // Contar cuántas veces ya hemos marcado esta letra como correcta o presente
    let markedCount = 0;
    for (let i = 0; i < 5; i++) {
      const currentLetter = getTileElement(gameState.currentRow, i).textContent;
      if (currentLetter === letter) {
        if (i < position && (solution[i] === letter || markedCount < letterCount)) {
          markedCount++;
        } else if (i === position && markedCount < letterCount) {
          return 'present';
        }
      }
    }
    
    return markedCount < letterCount ? 'present' : 'absent';
  }
  
  return 'absent';
}

// Actualizar el estado de las teclas del teclado
function updateKeyboardState(letter, state) {
  const keyElement = document.querySelector(`.key[data-key="${letter}"]`);
  
  if (keyElement) {
    const currentState = keyElement.getAttribute('data-state');
    
    // Solo actualizar si el nuevo estado es mejor que el actual
    if (!currentState || 
        (currentState === 'absent' && (state === 'present' || state === 'correct')) ||
        (currentState === 'present' && state === 'correct')) {
      
      keyElement.setAttribute('data-state', state);
      gameState.keyboardState[letter] = state;
    }
  }
}

// Animar fila con efecto de sacudida
function animateRowShake(row) {
  const rowElement = document.querySelectorAll('.board-row')[row];
  rowElement.classList.add('shake');
  
  setTimeout(() => {
    rowElement.classList.remove('shake');
  }, 500);
}

// Obtener elemento tile por coordenadas
function getTileElement(row, col) {
  return document.querySelectorAll('.board-row')[row].querySelectorAll('.tile')[col];
}

// Mostrar mensaje toast
function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}

// Mostrar modal de instrucciones
function showInstructions() {
  instructionsModal.style.display = 'flex';
}

// Mostrar modal de estadísticas
function showStats() {
  updateStatsDisplay();
  statsModal.style.display = 'flex';
}

// Mostrar modal de fin de juego
function showGameOverModal(won) {
  const titleElement = document.getElementById('game-result-title');
  const correctWordElement = document.getElementById('correct-word');
  const definitionElement = document.getElementById('word-definition');
  
  // Buscar la definición de la palabra
  const wordData = palabrasWordle.find(word => word.palabra === gameState.solution);
  
  if (won) {
    titleElement.textContent = 'Awesome!';
  } else {
    titleElement.textContent = 'Too Bad!';
  }
  
  correctWordElement.textContent = gameState.solution;
  definitionElement.textContent = wordData ? wordData.definicion : '';
  
  updateStatsDisplay();
  gameOverModal.style.display = 'flex';
}

// Cerrar modal
function closeModal(modal) {
  modal.style.display = 'none';
}

// Compartir resultados
function shareResults() {
  if (!gameState.gameOver) return;
  
  const won = gameState.guesses.length > 0 && 
             gameState.guesses[gameState.guesses.length - 1].join('') === gameState.solution;
  
  let resultText = `Wordle Uruguayo ${won ? gameState.guesses.length : 'X'}/6\n\n`;
  
  // Generar emojis para cada intento
  for (let i = 0; i < gameState.guesses.length; i++) {
    const guess = gameState.guesses[i];
    let rowEmojis = '';
    
    for (let j = 0; j < 5; j++) {
      const letter = guess[j];
      const state = getLetterState(letter, j, gameState.solution);
      
      if (state === 'correct') {
        rowEmojis += '🟩';
      } else if (state === 'present') {
        rowEmojis += '🟨';
      } else {
        rowEmojis += '⬛';
      }
    }
    
    resultText += rowEmojis + '\n';
  }
  
  // Añadir enlace al juego
  resultText += '\nhttps://wordleuruguayo.com';
  
  // Copiar al portapapeles
  navigator.clipboard.writeText(resultText)
    .then(() => {
      showToast('Resultados copiados al portapapeles');
    })
    .catch(() => {
      showToast('No se pudo copiar al portapapeles');
    });
}

// Actualizar cuenta regresiva para la próxima palabra
function updateCountdown() {
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(0, 0, 0, 0);
  
  const timeRemaining = tomorrow - now;
  
  const hours = Math.floor(timeRemaining / (1000 * 60 * 60));
  const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
  
  const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  
  document.getElementById('countdown').textContent = formattedTime;
  document.getElementById('game-over-countdown').textContent = formattedTime;
  
  setTimeout(updateCountdown, 1000);
}

// Cargar tema (claro/oscuro)
function loadTheme() {
  const darkMode = localStorage.getItem('wordleUruguayoDarkMode') === 'true';
  document.body.classList.toggle('dark-theme', darkMode);
}

// Alternar entre tema claro y oscuro
function toggleTheme() {
  const isDarkMode = document.body.classList.toggle('dark-theme');
  localStorage.setItem('wordleUruguayoDarkMode', isDarkMode);
}

// Iniciar el juego cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', initGame);
