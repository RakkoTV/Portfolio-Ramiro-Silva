<!DOCTYPE html>
<html lang="es" class="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juego de Memoria</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="css/styles.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-purple-950 via-indigo-950 to-slate-950 dark:bg-gradient-to-br dark:from-slate-100 dark:via-indigo-100 dark:to-purple-100">
    <div id="app" class="flex flex-col items-center justify-center min-h-screen p-4 space-y-8">
        <div class="flex items-center justify-between w-full max-w-4xl px-4">
            <button id="theme-toggle" class="p-2 text-indigo-200 dark:text-indigo-800 bg-indigo-950/80 dark:bg-white/80 border border-indigo-700 dark:border-indigo-300 rounded-lg hover:bg-indigo-900 dark:hover:bg-indigo-50 hover:border-indigo-500 dark:hover:border-indigo-400 transition-all duration-300">
                <svg id="theme-toggle-dark-icon" class="w-5 h-5 hidden" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
                <svg id="theme-toggle-light-icon" class="w-5 h-5 hidden" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"></path>
                </svg>
            </button>
        </div>
        <div class="text-center space-y-4">
            <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-300 via-pink-300 to-indigo-300 dark:from-purple-600 dark:via-pink-600 dark:to-indigo-600 text-transparent bg-clip-text">
                Juego de Memoria
            </h1>
            <p class="text-indigo-200 dark:text-indigo-800" id="matches">Parejas encontradas: 0 de 6</p>
        </div>
        <div id="game-board" class="grid grid-cols-3 gap-4 md:gap-6 p-6 rounded-xl bg-indigo-950/50 dark:bg-white/50 backdrop-blur-sm">
        </div>
        <button id="reset-button" 
                class="px-4 py-2 text-indigo-200 dark:text-indigo-800 bg-indigo-950 dark:bg-white/80 border border-indigo-700 dark:border-indigo-300 rounded-lg hover:bg-indigo-900 dark:hover:bg-indigo-50 hover:border-indigo-500 dark:hover:border-indigo-400 hover:text-indigo-100 dark:hover:text-indigo-900 transition-all duration-300">
            Iniciar Nuevo Juego
        </button>
    </div>
    <script src="js/game.js"></script>
    <script src="js/theme.js"></script>
</body>
</html>