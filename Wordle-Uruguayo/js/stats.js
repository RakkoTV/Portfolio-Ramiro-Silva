// stats.js - Manejo de estadísticas para Wordle Uruguayo

// Estructura de estadísticas
const defaultStats = {
  gamesPlayed: 0,
  gamesWon: 0,
  currentStreak: 0,
  maxStreak: 0,
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
};

// Cargar estadísticas desde localStorage
export function loadStats() {
  const savedStats = localStorage.getItem('wordleUruguayoStats');
  if (savedStats) {
    return JSON.parse(savedStats);
  }
  return { ...defaultStats };
}

// Guardar estadísticas en localStorage
export function saveStats(stats) {
  localStorage.setItem('wordleUruguayoStats', JSON.stringify(stats));
}

// Actualizar estadísticas después de un juego
export function updateStats(stats, won, attempts) {
  const updatedStats = { ...stats };
  
  // Actualizar contadores básicos
  updatedStats.gamesPlayed++;
  
  if (won) {
    updatedStats.gamesWon++;
    updatedStats.currentStreak++;
    updatedStats.guessDistribution[attempts]++;
  } else {
    updatedStats.currentStreak = 0;
  }
  
  // Actualizar mejor racha
  updatedStats.maxStreak = Math.max(updatedStats.maxStreak, updatedStats.currentStreak);
  
  // Actualizar fechas
  updatedStats.lastPlayed = new Date().toLocaleDateString();
  if (won || !won) { // Siempre actualizar lastCompleted cuando termina un juego
    updatedStats.lastCompleted = new Date().toLocaleDateString();
  }
  
  return updatedStats;
}

// Actualizar visualización de estadísticas en la interfaz
export function updateStatsDisplay(stats) {
  // Actualizar contadores básicos
  document.getElementById('games-played').textContent = stats.gamesPlayed;
  document.getElementById('summary-games-played').textContent = stats.gamesPlayed;
  
  // Calcular y actualizar porcentaje de victorias
  const winPercentage = stats.gamesPlayed > 0 
    ? Math.round((stats.gamesWon / stats.gamesPlayed) * 100) 
    : 0;
  document.getElementById('win-percentage').textContent = winPercentage;
  document.getElementById('summary-win-percentage').textContent = winPercentage;
  
  // Actualizar rachas
  document.getElementById('current-streak').textContent = stats.currentStreak;
  document.getElementById('summary-current-streak').textContent = stats.currentStreak;
  document.getElementById('max-streak').textContent = stats.maxStreak;
  
  // Actualizar distribución de intentos
  updateGuessDistribution(stats.guessDistribution);
}

// Actualizar gráfico de distribución de intentos
function updateGuessDistribution(distribution) {
  const guessDistribution = document.getElementById('guess-distribution');
  guessDistribution.innerHTML = '';
  
  // Encontrar el valor máximo para escalar las barras
  const maxGuesses = Math.max(...Object.values(distribution), 1);
  
  // Crear una barra para cada número de intentos
  for (let i = 1; i <= 6; i++) {
    const count = distribution[i];
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
}

// Verificar si es un nuevo día para reiniciar el juego
export function isNewDay(lastPlayed) {
  const today = new Date().toLocaleDateString();
  return lastPlayed !== today;
}

// Generar texto para compartir resultados
export function generateShareText(guesses, solution, won) {
  let resultText = `Wordle Uruguayo ${won ? guesses.length : 'X'}/6\n\n`;
  
  // Generar emojis para cada intento
  for (const guess of guesses) {
    let rowEmojis = '';
    
    for (let i = 0; i < guess.length; i++) {
      const letter = guess[i];
      const state = getLetterState(letter, i, solution);
      
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
  
  return resultText;
}

// Determinar el estado de una letra (correct, present, absent)
function getLetterState(letter, position, solution) {
  if (solution[position] === letter) {
    return 'correct';
  }
  
  if (solution.includes(letter)) {
    return 'present';
  }
  
  return 'absent';
}

// Actualizar cuenta regresiva para la próxima palabra
export function updateCountdown() {
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
  
  return formattedTime;
}
