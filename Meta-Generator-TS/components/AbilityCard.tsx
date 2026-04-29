
import React, { useState } from 'react';
import { Ability } from '../types.ts';
import { generateImage } from '../services/geminiService.ts';
import Loader from './Loader.tsx';
import { TranslationSet } from '../lib/translations.ts';

interface AbilityCardProps {
  ability: Ability;
  characterDescription: string;
  t: TranslationSet;
  seed: number | null;
}

const AbilityCard: React.FC<AbilityCardProps> = ({ ability, characterDescription, t, seed }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [abilityImageUrl, setAbilityImageUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleVisualize = async () => {
    if (abilityImageUrl) {
        setIsModalOpen(true);
        return;
    }
    
    setIsGenerating(true);
    setError(null);
    try {
      const prompt = `Dynamic action scene, digital painting style. ${characterDescription}. The ability being used is called "${ability.name}". Visual effect description: ${ability.description}. Cinematic lighting, high energy.`;
      const imageResult = await generateImage(prompt, seed ?? undefined);
      setAbilityImageUrl(`data:image/jpeg;base64,${imageResult.imageBytes}`);
      setIsModalOpen(true);
    } catch (err) {
      console.error('Ability image generation failed:', err);
      setError(t.visualizeError);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <>
      <div 
        className="glass-card p-4 rounded-lg border border-cyan-500/30 hover:border-cyan-400 hover:bg-cyan-900/40 transition-all duration-300 cursor-pointer group"
        onClick={handleVisualize}
      >
        <h4 className="font-bold font-orbitron text-lg text-cyan-300 group-hover:text-white">{ability.name}</h4>
        <p className="text-sm text-gray-300 mt-1 font-light">{ability.description}</p>
        {isGenerating && 
            <div className="mt-2 flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-t-transparent border-cyan-300 rounded-full animate-spin"></div>
                <span className="text-xs text-cyan-300">{t.visualizing}</span>
            </div>
        }
        {error && <p className="text-xs text-red-400 mt-2">{error}</p>}
      </div>

      {isModalOpen && abilityImageUrl && (
        <div 
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setIsModalOpen(false)}
        >
          <div 
            className="relative glass-card p-2 md:p-4 rounded-xl max-w-2xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="overflow-hidden rounded-lg">
                <img src={abilityImageUrl} alt={`Visualization of ${ability.name}`} className="w-full h-auto rounded-lg animate-ken-burns" />
            </div>
            <h3 className="font-orbitron text-xl md:text-2xl text-center mt-4 text-cyan-200 neon-text">{ability.name}</h3>
            <p className="text-center text-gray-300 text-sm md:text-base mt-1">{ability.description}</p>
            <button
                onClick={() => setIsModalOpen(false)}
                className="absolute -top-4 -right-4 bg-red-500 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl font-bold border-2 border-white/50 hover:bg-red-400 transition-all"
                aria-label="Close"
            >
                &times;
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default AbilityCard;