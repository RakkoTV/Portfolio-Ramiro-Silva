
import React from 'react';
import { languages, Language } from '../lib/translations.ts';

interface LanguageSwitcherProps {
  language: Language;
  setLanguage: (lang: Language) => void;
}

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ language, setLanguage }) => {
  const switchLanguage = () => {
    const currentIndex = languages.indexOf(language);
    const nextIndex = (currentIndex + 1) % languages.length;
    setLanguage(languages[nextIndex]);
  };

  return (
    <div className="absolute top-4 right-4 z-20">
      <button
        onClick={switchLanguage}
        className="glass-card flex items-center justify-center gap-2 px-3 py-2 rounded-md border border-cyan-400/30 hover:border-cyan-400 transition-all duration-300"
        aria-label={`Change language, current is ${language}`}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-cyan-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9V3m0 18a9 9 0 009-9m-9 9a9 9 0 00-9-9" />
        </svg>
        <span className="font-orbitron text-cyan-300 font-bold text-sm">{language}</span>
      </button>
    </div>
  );
};

export default LanguageSwitcher;
