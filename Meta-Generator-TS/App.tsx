
import React, { useState, useCallback } from 'react';
import { CharacterData } from './types.ts';
import { generateCharacterDetails, generateImage } from './services/geminiService.ts';
import Header from './components/Header.tsx';
import CharacterSheet from './components/CharacterSheet.tsx';
import MatrixBackground from './components/MatrixBackground.tsx';
import Loader from './components/Loader.tsx';
import LanguageSwitcher from './components/LanguageSwitcher.tsx';
import { translations, Language } from './lib/translations.ts';

const App: React.FC = () => {
  const [characterName, setCharacterName] = useState<string>('');
  const [characterData, setCharacterData] = useState<CharacterData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<Language>('EN');
  const [portraitSeed, setPortraitSeed] = useState<number | null>(null);

  const t = translations[language];

  const handleGenerate = useCallback(async () => {
    if (!characterName.trim()) {
      setError(t.errorNoName);
      return;
    }
    setIsLoading(true);
    setError(null);
    setCharacterData(null);
    setPortraitSeed(null);

    try {
      const details = await generateCharacterDetails(characterName, language);
      
      const portraitPrompt = `Sci-fi fantasy concept art, highly detailed digital painting of a character named ${characterName}. ${details.backstory.substring(0, 150)}. Epic, cinematic, intricate details.`;
      const portraitResult = await generateImage(portraitPrompt);
      const portraitImage = portraitResult.imageBytes;
      setPortraitSeed(portraitResult.seed ?? null);

      const newCharacter: CharacterData = {
        name: characterName,
        ...details,
        portraitUrl: `data:image/jpeg;base64,${portraitImage}`,
      };

      setCharacterData(newCharacter);

    } catch (err) {
      console.error('Generation failed:', err);
      setError(t.errorDefault);
    } finally {
      setIsLoading(false);
    }
  }, [characterName, t, language]);

  return (
    <div className="relative min-h-screen w-full flex flex-col items-center p-4 sm:p-6 lg:p-8 font-sans bg-[#0a0a1a]">
      <MatrixBackground />
      <LanguageSwitcher language={language} setLanguage={setLanguage} />
      <div className="relative z-10 w-full max-w-7xl mx-auto">
        <Header
          characterName={characterName}
          setCharacterName={setCharacterName}
          onGenerate={handleGenerate}
          isLoading={isLoading}
          t={t}
        />

        <main className="mt-8">
          {isLoading && (
            <div className="flex flex-col items-center justify-center glass-card p-8 rounded-lg">
              <Loader />
              <p className="mt-4 text-lg text-cyan-300 font-orbitron animate-pulse">
                {t.forgingMessage}
              </p>
            </div>
          )}

          {error && (
            <div className="glass-card p-6 rounded-lg border border-red-500 text-center">
              <h3 className="text-xl font-bold text-red-400">{t.errorTitle}</h3>
              <p className="mt-2 text-red-300">{error}</p>
            </div>
          )}

          {characterData && !isLoading && (
            <CharacterSheet character={characterData} t={t} portraitSeed={portraitSeed} />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;