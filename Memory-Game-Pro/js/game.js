const icons = [
    { name: 'heart', color: 'text-rose-400' },
    { name: 'star', color: 'text-amber-400' },
    { name: 'sun', color: 'text-yellow-400' },
    { name: 'moon', color: 'text-purple-400' },
    { name: 'cloud', color: 'text-sky-400' },
    { name: 'flower', color: 'text-emerald-400' }
];

class MemoryGame {
    constructor() {
        this.cards = [];
        this.flippedCards = [];
        this.matches = 0;
        this.isChecking = false;
        this.gameBoard = document.getElementById('game-board');
        this.matchesText = document.getElementById('matches');
        this.resetButton = document.getElementById('reset-button');
        this.resetButton.addEventListener('click', () => this.resetGame());
        this.initializeGame();
    }

    createCards() {
        const cards = [];
        icons.forEach((icon, index) => {
            cards.push(
                { id: index * 2, icon: icon.name, color: icon.color, isMatched: false },
                { id: index * 2 + 1, icon: icon.name, color: icon.color, isMatched: false }
            );
        });
        return cards.sort(() => Math.random() - 0.5);
    }

    createCardElement(card, index) {
        const cardElement = document.createElement('div');
        cardElement.className = 'perspective-1000';
        cardElement.innerHTML = `
            <div class="relative w-24 h-24 md:w-32 md:h-32 cursor-pointer transform-style-3d transition-all duration-300 bg-indigo-950 dark:bg-white border border-indigo-800 dark:border-indigo-300 hover:border-indigo-600 dark:hover:border-indigo-400 hover:bg-indigo-900/80 dark:hover:bg-indigo-50 rounded-lg"
                 data-index="${index}">
                <div class="absolute inset-0 bg-gradient-to-br from-transparent via-indigo-500/5 to-white/5 dark:via-indigo-500/10 dark:to-purple-500/10"></div>
                <div class="icon-container absolute inset-0 flex items-center justify-center backface-hidden" style="transform: rotateY(180deg)">
                    <svg class="w-12 h-12 ${card.color} dark:opacity-90" data-icon="${card.icon}"></svg>
                </div>
            </div>
        `;
        cardElement.querySelector('.relative').addEventListener('click', () => this.handleCardClick(index));
        return cardElement;
    }

    handleCardClick(clickedIndex) {
        if (this.isChecking || this.cards[clickedIndex].isMatched) return;
        if (this.flippedCards.includes(clickedIndex)) return;
        if (this.flippedCards.length === 2) return;

        const cardElement = this.gameBoard.children[clickedIndex].querySelector('.relative');
        cardElement.style.transform = 'rotateY(180deg)';
        cardElement.classList.remove('bg-indigo-950');
        cardElement.classList.add('bg-indigo-800/50');

        this.flippedCards.push(clickedIndex);

        if (this.flippedCards.length === 2) {
            this.isChecking = true;
            const [firstIndex, secondIndex] = this.flippedCards;
            const firstCard = this.cards[firstIndex];
            const secondCard = this.cards[secondIndex];

            if (firstCard.icon === secondCard.icon) {
                setTimeout(() => {
                    this.handleMatch(firstIndex, secondIndex);
                }, 500);
            } else {
                setTimeout(() => {
                    this.resetFlippedCards();
                }, 1000);
            }
        }
    }

    handleMatch(firstIndex, secondIndex) {
        const firstCard = this.gameBoard.children[firstIndex].querySelector('.relative');
        const secondCard = this.gameBoard.children[secondIndex].querySelector('.relative');

        firstCard.classList.add('bg-indigo-900/50', 'border-indigo-400/50');
        secondCard.classList.add('bg-indigo-900/50', 'border-indigo-400/50');

        this.cards[firstIndex].isMatched = true;
        this.cards[secondIndex].isMatched = true;
        this.matches++;
        this.matchesText.textContent = `Parejas encontradas: ${this.matches} de ${this.cards.length / 2}`;

        if (this.matches === this.cards.length / 2) {
            setTimeout(() => {
                alert('¡Felicitaciones! ¡Has encontrado todas las parejas! 🎉');
            }, 500);
        }

        this.flippedCards = [];
        this.isChecking = false;
    }

    resetFlippedCards() {
        this.flippedCards.forEach(index => {
            const cardElement = this.gameBoard.children[index].querySelector('.relative');
            cardElement.style.transform = 'rotateY(0deg)';
            cardElement.classList.remove('bg-indigo-800/50');
            cardElement.classList.add('bg-indigo-950');
        });
        this.flippedCards = [];
        this.isChecking = false;
    }

    resetGame() {
        this.cards = this.createCards();
        this.flippedCards = [];
        this.matches = 0;
        this.isChecking = false;
        this.matchesText.textContent = `Parejas encontradas: ${this.matches} de ${this.cards.length / 2}`;
        this.renderBoard();
    }

    renderBoard() {
        this.gameBoard.innerHTML = '';
        this.cards.forEach((card, index) => {
            const cardElement = this.createCardElement(card, index);
            this.gameBoard.appendChild(cardElement);
        });
        this.loadIcons();
    }

    loadIcons() {
        const iconPaths = {
            heart: 'M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z',
            star: 'M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z',
            sun: 'M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z',
            moon: 'M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z',
            cloud: 'M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z',
            flower: 'M12 18c.714 0 1.37-.25 1.886-.666A2.987 2.987 0 0015 15c0-.707-.25-1.362-.666-1.878A2.98 2.98 0 0012 12a2.98 2.98 0 00-1.886.666A2.987 2.987 0 009 15c0 .707.25 1.362.666 1.878A2.98 2.98 0 0012 18zm0 2a5 5 0 01-5-5c0-1.1.354-2.122.955-2.955C8.878 11.354 9.9 11 11 11c1.1 0 2.122.354 2.955.955C14.646 12.878 15 13.9 15 15c0 1.1-.354 2.122-.955 2.955C13.122 18.646 12.1 19 11 19zm-1-8V7h2v4h-2zm0 12v-4h2v4h-2zm8-6h-4v-2h4v2zM7 15H3v-2h4v2zm8.364-8.364l-2.828 2.828-1.414-1.414 2.828-2.828 1.414 1.414zM7.05 16.95l-2.828 2.828-1.414-1.414 2.828-2.828 1.414 1.414zm9.9 0l2.828 2.828-1.414 1.414-2.828-2.828 1.414-1.414zM7.05 7.05L4.222 4.222 5.636 2.808l2.828 2.828-1.414 1.414z'
        };

        document.querySelectorAll('svg[data-icon]').forEach(svg => {
            const iconName = svg.getAttribute('data-icon');
            if (iconPaths[iconName]) {
                svg.setAttribute('viewBox', '0 0 24 24');
                svg.setAttribute('fill', 'none');
                svg.setAttribute('stroke', 'currentColor');
                svg.setAttribute('stroke-width', '1.5');
                svg.setAttribute('stroke-linecap', 'round');
                svg.setAttribute('stroke-linejoin', 'round');
                svg.innerHTML = `<path d="${iconPaths[iconName]}"></path>`;
            }
        });
    }

    initializeGame() {
        this.cards = this.createCards();
        this.renderBoard();
    }
}

// Iniciar el juego cuando se cargue la página
document.addEventListener('DOMContentLoaded', () => {
    new MemoryGame();
});