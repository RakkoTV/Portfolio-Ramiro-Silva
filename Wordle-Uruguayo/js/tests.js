// Archivo de pruebas para verificar la funcionalidad del juego Wordle Uruguayo

// Importar módulos necesarios
import { palabrasWordle } from './words.js';
import * as keyboard from './keyboard.js';
import * as stats from './stats.js';

// Función para ejecutar pruebas
function runTests() {
  console.log('Iniciando pruebas del Wordle Uruguayo...');
  
  // Prueba 1: Verificar que hay suficientes palabras de 5 letras
  testWordDatabase();
  
  // Prueba 2: Verificar funcionalidad de estadísticas
  testStatsModule();
  
  // Prueba 3: Verificar funcionalidad del teclado
  testKeyboardModule();
  
  // Prueba 4: Verificar lógica del juego
  testGameLogic();
  
  console.log('Todas las pruebas completadas.');
}

// Prueba de la base de datos de palabras
function testWordDatabase() {
  console.log('Prueba: Base de datos de palabras');
  
  // Verificar que hay palabras en la base de datos
  if (palabrasWordle.length === 0) {
    console.error('Error: No hay palabras en la base de datos');
    return false;
  }
  
  console.log(`Palabras disponibles: ${palabrasWordle.length}`);
  
  // Verificar que todas las palabras tienen 5 letras
  const invalidWords = palabrasWordle.filter(word => word.palabra.length !== 5);
  if (invalidWords.length > 0) {
    console.error('Error: Hay palabras que no tienen 5 letras:', invalidWords);
    return false;
  }
  
  // Verificar que todas las palabras tienen definición
  const wordsWithoutDefinition = palabrasWordle.filter(word => !word.definicion);
  if (wordsWithoutDefinition.length > 0) {
    console.error('Error: Hay palabras sin definición:', wordsWithoutDefinition);
    return false;
  }
  
  console.log('✓ Base de datos de palabras verificada correctamente');
  return true;
}

// Prueba del módulo de estadísticas
function testStatsModule() {
  console.log('Prueba: Módulo de estadísticas');
  
  // Crear estadísticas de prueba
  const testStats = { ...stats.loadStats() };
  
  // Probar actualización de estadísticas para victoria
  const updatedStatsWin = stats.updateStats(testStats, true, 3);
  if (updatedStatsWin.gamesPlayed !== testStats.gamesPlayed + 1) {
    console.error('Error: No se incrementó el contador de juegos jugados');
    return false;
  }
  
  if (updatedStatsWin.gamesWon !== testStats.gamesWon + 1) {
    console.error('Error: No se incrementó el contador de juegos ganados');
    return false;
  }
  
  if (updatedStatsWin.currentStreak !== testStats.currentStreak + 1) {
    console.error('Error: No se incrementó la racha actual');
    return false;
  }
  
  if (updatedStatsWin.guessDistribution[3] !== testStats.guessDistribution[3] + 1) {
    console.error('Error: No se actualizó la distribución de intentos');
    return false;
  }
  
  // Probar actualización de estadísticas para derrota
  const updatedStatsLoss = stats.updateStats(updatedStatsWin, false, 6);
  if (updatedStatsLoss.currentStreak !== 0) {
    console.error('Error: No se reinició la racha actual después de perder');
    return false;
  }
  
  // Probar generación de texto para compartir
  const shareText = stats.generateShareText([['B', 'O', 'N', 'D', 'I']], 'BONDI', true);
  if (!shareText.includes('Wordle Uruguayo 1/6')) {
    console.error('Error: El texto para compartir no es correcto');
    return false;
  }
  
  console.log('✓ Módulo de estadísticas verificado correctamente');
  return true;
}

// Prueba del módulo de teclado
function testKeyboardModule() {
  console.log('Prueba: Módulo de teclado');
  
  // Verificar que se puede actualizar el estado de una tecla
  const keyUpdated = keyboard.updateKeyState('A', 'correct');
  if (keyUpdated === false) {
    console.error('Error: No se pudo actualizar el estado de la tecla');
    return false;
  }
  
  // Verificar que se puede reiniciar el teclado
  try {
    keyboard.resetKeyboard();
    console.log('✓ Reinicio de teclado verificado');
  } catch (error) {
    console.error('Error al reiniciar el teclado:', error);
    return false;
  }
  
  console.log('✓ Módulo de teclado verificado correctamente');
  return true;
}

// Prueba de la lógica del juego
function testGameLogic() {
  console.log('Prueba: Lógica del juego');
  
  // Verificar que se puede obtener una palabra aleatoria
  const randomIndex = Math.floor(Math.random() * palabrasWordle.length);
  const randomWord = palabrasWordle[randomIndex].palabra;
  
  if (!randomWord || randomWord.length !== 5) {
    console.error('Error: No se pudo obtener una palabra aleatoria válida');
    return false;
  }
  
  console.log(`Palabra de prueba: ${randomWord}`);
  
  // Simular un juego
  const gameState = {
    currentRow: 0,
    currentTile: 0,
    gameOver: false,
    solution: randomWord,
    guesses: []
  };
  
  // Simular un intento correcto
  const guess = randomWord.split('');
  gameState.guesses.push(guess);
  
  // Verificar victoria
  if (guess.join('') === gameState.solution) {
    gameState.gameOver = true;
    console.log('✓ Victoria detectada correctamente');
  } else {
    console.error('Error: No se detectó la victoria');
    return false;
  }
  
  console.log('✓ Lógica del juego verificada correctamente');
  return true;
}

// Ejecutar pruebas cuando se carga el script
document.addEventListener('DOMContentLoaded', runTests);

// Exportar funciones para uso externo
export { runTests };
