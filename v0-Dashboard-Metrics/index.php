<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .dark { background: linear-gradient(to bottom right, #000000, #1e293b); color: #f1f5f9; }
        .light { background: linear-gradient(to bottom right, #f1f5f9, #e2e8f0); color: #1e293b; }
        .particle-canvas { position: absolute; width: 100%; height: 100%; opacity: 0.3; }
    </style>
</head>
<body class="dark min-h-screen relative overflow-hidden" id="mainBody">
    <canvas id="particleCanvas" class="particle-canvas"></canvas>

    <div class="container mx-auto px-4 py-8 relative z-10">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-2xl font-bold">System Dashboard</h1>
            <div class="flex items-center gap-4">
                <span id="currentTime" class="text-lg"></span>
                <button id="themeToggle" class="p-2 rounded-full hover:bg-slate-800">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                </button>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-slate-800/50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">System Status</h3>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div id="systemStatus" class="h-full bg-green-500" style="width: 85%"></div>
                </div>
            </div>

            <div class="bg-slate-800/50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">CPU Usage</h3>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div id="cpuUsage" class="h-full bg-blue-500" style="width: 42%"></div>
                </div>
            </div>

            <div class="bg-slate-800/50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">Memory Usage</h3>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div id="memoryUsage" class="h-full bg-purple-500" style="width: 68%"></div>
                </div>
            </div>

            <div class="bg-slate-800/50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">Network Status</h3>
                <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div id="networkStatus" class="h-full bg-yellow-500" style="width: 92%"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Particle effect
        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        const particleCount = 100;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3 + 1;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.color = `rgba(${Math.floor(Math.random() * 100) + 100}, ${Math.floor(Math.random() * 100) + 150}, ${Math.floor(Math.random() * 55) + 200}, ${Math.random() * 0.5 + 0.2})`;
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });

            requestAnimationFrame(animate);
        }

        animate();

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        // Update time
        function updateTime() {
            const now = new Date();
            document.getElementById('currentTime').textContent = now.toLocaleTimeString();
        }

        setInterval(updateTime, 1000);
        updateTime();

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        const mainBody = document.getElementById('mainBody');
        let isDark = true;

        themeToggle.addEventListener('click', () => {
            isDark = !isDark;
            mainBody.className = isDark ? 'dark min-h-screen relative overflow-hidden' : 'light min-h-screen relative overflow-hidden';
            themeToggle.innerHTML = isDark ? 
                '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>' :
                '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>';
        });

        // Update metrics
        async function updateMetrics() {
            try {
                const response = await fetch('get_metrics.php');
                const data = await response.json();
                
                document.getElementById('systemStatus').style.width = `${data.system_status}%`;
                document.getElementById('cpuUsage').style.width = `${data.cpu_usage}%`;
                document.getElementById('memoryUsage').style.width = `${data.memory_usage}%`;
                document.getElementById('networkStatus').style.width = `${data.network_status}%`;
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        setInterval(updateMetrics, 3000);
        updateMetrics();
    </script>
</body>
</html>