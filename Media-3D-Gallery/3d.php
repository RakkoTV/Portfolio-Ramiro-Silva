<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página 3D - Inspiración GTA VI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&display=swap');
        body {
            font-family: 'Chakra Petch', sans-serif;
            margin: 0;
            background-color: #000;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding-top: 80px; /* Space for fixed nav */
            box-sizing: border-box;
            text-align: center;
            background-image: url('https://media.rockstargames.com/rockstargames-newsite/img/global/games/fob/640/grandtheftautovi.jpg'); /* Example background, replace with a suitable one */
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .main-nav {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 15px 0;
            width: 100%;
            text-align: center;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            border-bottom: 2px solid #ff0055; /* GTA VI inspired pink/magenta */
        }
        .nav-link {
            color: #fff;
            text-decoration: none;
            margin: 0 20px;
            font-size: 1.3em;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 5px;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }
        .nav-link:hover,
        .nav-link.active-nav {
            background-color: #ff0055;
            color: #000;
            box-shadow: 0 0 15px #ff0055;
        }
        .content-container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 15px;
            margin-top: 50px;
            max-width: 800px;
            width: 90%;
            box-shadow: 0 0 25px rgba(255, 0, 85, 0.5);
        }
        h1 {
            color: #ff0055; /* GTA VI inspired pink/magenta */
            font-weight: 700;
            font-size: 3em;
            text-shadow: 2px 2px 0px #000, 3px 3px 0px rgba(255,255,255,0.2);
            margin-bottom: 20px;
            letter-spacing: 2px;
        }
        p {
            font-size: 1.3em;
            line-height: 1.7;
            margin-bottom: 30px;
            color: #f0f0f0;
        }
        .cta-link {
            display: inline-block;
            color: #000;
            background-color: #ff0055;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.2em;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 2px solid #ff0055;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .cta-link:hover {
            background-color: #fff;
            color: #ff0055;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 0, 85, 0.4);
        }
    </style>
</head>
<body>
    <nav class="main-nav">
        <a href="index.php" class="nav-link">Reproductor</a>
        <a href="3d.php" class="nav-link active-nav">Página 3D</a>
    </nav>
    <div class="content-container">
        <h1>BIENVENIDO A LA AVENTURA 3D</h1>
        <p>Explora un nuevo mundo de posibilidades. Esta sección está en construcción, ¡pero pronto traerá experiencias increíbles inspiradas en los universos más audaces!</p>
        <a href="index.php" class="cta-link">Volver al Reproductor</a>
    </div>
</body>
</html>