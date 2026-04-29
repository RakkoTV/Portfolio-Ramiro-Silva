document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('matrix-background');
    const ctx = canvas.getContext('2d');

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = document.body.scrollHeight;

    const columns = Math.floor(width / 20);
    const ypos = Array(columns).fill(0);
    const chars = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789'.split('');

    function matrix() {
        ctx.fillStyle = 'rgba(10, 10, 26, 0.05)';
        ctx.fillRect(0, 0, width, height);

        ctx.fillStyle = '#00bfff';
        ctx.font = '15pt monospace';

        ypos.forEach((y, ind) => {
            const text = chars[Math.floor(Math.random() * chars.length)];
            const x = ind * 20;
            ctx.fillText(text, x, y);

            if (y > 100 + Math.random() * 10000) {
                ypos[ind] = 0;
            } else {
                ypos[ind] = y + 20;
            }
        });
    }

    setInterval(matrix, 60);

    const generateBtn = document.getElementById('generate-btn');
    const characterNameInput = document.getElementById('character-name');
    const loader = document.getElementById('loader');
    const errorDiv = document.getElementById('error');
    const characterSheetDiv = document.getElementById('character-sheet');

    generateBtn.addEventListener('click', async () => {
        const name = characterNameInput.value.trim();
        if (!name) {
            showError('Please enter a character name.');
            return;
        }

        showLoader(true);
        showError(null);
        hideCharacterSheet();

        try {
            const response = await fetch('generate.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `name=${encodeURIComponent(name)}&language=EN`,
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'Failed to generate character.');
            }

            const data = await response.json();
            displayCharacter(data);

        } catch (err) {
            showError(err.message);
        } finally {
            showLoader(false);
        }
    });

    function showLoader(show) {
        loader.classList.toggle('hidden', !show);
    }

    function showError(message) {
        if (message) {
            errorDiv.classList.remove('hidden');
            errorDiv.querySelector('p').textContent = message;
        } else {
            errorDiv.classList.add('hidden');
        }
    }

    function hideCharacterSheet() {
        characterSheetDiv.classList.add('hidden');
    }

    function displayCharacter(character) {
        characterSheetDiv.classList.remove('hidden');
        characterSheetDiv.innerHTML = `
            <h2>${character.name}</h2>
            <img src="${character.portraitUrl}" alt="Portrait of ${character.name}" style="width:100%;max-width:300px;height:auto;border-radius:5px;margin-bottom:1rem;">
            <h3>Backstory</h3>
            <p>${character.backstory.replace(/\n/g, '<br>')}</p>
            <h3>Abilities</h3>
            <ul>
                ${character.abilities.map(ability => `<li><strong>${ability.name}:</strong> ${ability.description}</li>`).join('')}
            </ul>
        `;
    }
});