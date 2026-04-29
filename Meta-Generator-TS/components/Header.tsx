
import React from 'react';
import { TranslationSet } from '../lib/translations.ts';

interface HeaderProps {
  characterName: string;
  setCharacterName: (name: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
  t: TranslationSet;
}

const Header: React.FC<HeaderProps> = ({ characterName, setCharacterName, onGenerate, isLoading, t }) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate();
  };

  return (
    <header className="text-center mb-8">
      <h1 className="text-5xl md:text-6xl font-bold font-orbitron neon-text mb-4">
        {t.title}
      </h1>
      <p className="text-lg text-cyan-200 max-w-2xl mx-auto font-light">
        {t.subtitle}
      </p>
      <form onSubmit={handleSubmit} className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4 max-w-xl mx-auto">
        <input
          type="text"
          value={characterName}
          onChange={(e) => setCharacterName(e.target.value)}
          placeholder={t.placeholder}
          disabled={isLoading}
          className="w-full sm:w-2/3 px-4 py-3 bg-slate-800/70 border border-cyan-400/50 rounded-md focus:ring-2 focus:ring-cyan-300 focus:border-cyan-300 transition duration-300 text-white placeholder-gray-400 font-orbitron"
        />
        <button
          type="submit"
          disabled={isLoading || !characterName}
          className="w-full sm:w-auto btn-primary px-8 py-3 rounded-md text-lg font-bold text-white transition-transform duration-200"
        >
          {isLoading ? t.buttonLoading : t.button}
        </button>
      </form>
    </header>
  );
};

export default Header;
