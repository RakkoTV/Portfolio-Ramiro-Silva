<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Character Forge AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="matrix-background"></canvas>
    <div class="container">
        <header>
            <h1>Character Forge AI</h1>
            <div class="input-group">
                <input type="text" id="character-name" placeholder="Enter character name...">
                <button id="generate-btn">Generate</button>
            </div>
        </header>
        <main>
            <div id="loader" class="hidden">
                <div class="spinner"></div>
                <p>Forging your character...</p>
            </div>
            <div id="error" class="hidden">
                <h3>Error</h3>
                <p></p>
            </div>
            <div id="character-sheet" class="hidden">
                <!-- Character sheet will be populated by JavaScript -->
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>