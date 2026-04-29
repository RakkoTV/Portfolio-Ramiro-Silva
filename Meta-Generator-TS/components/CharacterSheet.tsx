
import React from 'react';
import { CharacterData } from '../types.ts';
import AbilityCard from './AbilityCard.tsx';
import { TranslationSet } from '../lib/translations.ts';

interface CharacterSheetProps {
  character: CharacterData;
  t: TranslationSet;
  portraitSeed: number | null;
}

const CharacterSheet: React.FC<CharacterSheetProps> = ({ character, t, portraitSeed }) => {
  return (
    <div className="glass-card p-6 md:p-8 rounded-xl animate-fade-in">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Portrait */}
        <div className="lg:col-span-1 flex flex-col items-center">
          <h2 className="text-4xl font-bold text-center text-cyan-300 font-orbitron mb-4 neon-text">
            {character.name}
          </h2>
          <img
            src={character.portraitUrl}
            alt={`Portrait of ${character.name}`}
            className="w-full h-auto rounded-lg border-2 border-cyan-400/50 shadow-lg shadow-cyan-500/20"
          />
        </div>

        {/* Right Column: Details */}
        <div className="lg:col-span-2">
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-cyan-300 font-orbitron border-b-2 border-cyan-400/30 pb-2 mb-4">
              {t.backstoryHeader}
            </h3>
            <p className="text-gray-300 font-light leading-relaxed whitespace-pre-wrap">
              {character.backstory}
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-cyan-300 font-orbitron border-b-2 border-cyan-400/30 pb-2 mb-4">
              {t.abilitiesHeader}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {character.abilities.map((ability, index) => (
                <AbilityCard
                  key={index}
                  ability={ability}
                  characterDescription={t.abilityImagePrompt.replace('{characterName}', character.name)}
                  t={t}
                  seed={portraitSeed}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Add fade-in animation to tailwind.config.js if it existed, but here we add it in a style tag or index.html
// For simplicity, we can rely on a class that we define in index.html, but let's just use Tailwind's existing classes
// Here we'll just imagine it exists via `animate-fade-in`
const style = document.createElement('style');
style.innerHTML = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fade-in {
    animation: fadeIn 0.8s ease-out forwards;
  }
`;
document.head.appendChild(style);


export default CharacterSheet;