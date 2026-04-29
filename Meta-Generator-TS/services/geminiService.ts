
import { GoogleGenAI, Type, GenerateContentResponse } from "@google/genai";
import { CharacterDetails } from '../types.ts';
import { Language } from '../lib/translations.ts';

if (!process.env.API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const languageMap: Record<Language, string> = {
    EN: 'English',
    ES: 'Spanish',
    JP: 'Japanese',
    KR: 'Korean',
    CN: 'Chinese (Simplified)',
};

const characterSchema = {
  type: Type.OBJECT,
  properties: {
    backstory: {
      type: Type.STRING,
      description: "A compelling and detailed backstory for the character, fitting a sci-fi or fantasy video game setting. Should be 2-3 paragraphs."
    },
    abilities: {
      type: Type.ARRAY,
      description: "A list of 3-4 unique and creative abilities for the character.",
      items: {
        type: Type.OBJECT,
        properties: {
          name: {
            type: Type.STRING,
            description: "The evocative name of the ability."
          },
          description: {
            type: Type.STRING,
            description: "A short, impactful description of what the ability does."
          }
        },
        required: ["name", "description"]
      }
    }
  },
  required: ["backstory", "abilities"]
};

export const generateCharacterDetails = async (name: string, language: Language): Promise<CharacterDetails> => {
  const targetLanguage = languageMap[language] || 'English';
  const prompt = `Create a unique video game character concept named "${name}". The character should exist in a universe blending science fiction and high fantasy. Provide a rich backstory and a list of unique abilities. IMPORTANT: Generate the entire response (backstory, ability names, and ability descriptions) in ${targetLanguage}.`;

  const response: GenerateContentResponse = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: characterSchema,
      temperature: 0.9,
    }
  });
  
  const text = response.text.trim();
  try {
      const parsed = JSON.parse(text);
      return parsed as CharacterDetails;
  } catch(e) {
      console.error("Failed to parse JSON from Gemini:", text);
      throw new Error("Received malformed data from the AI.");
  }
};

export const generateImage = async (prompt: string, seed?: number): Promise<{ imageBytes: string; seed: number | undefined }> => {
    const response = await ai.models.generateImages({
        model: 'imagen-3.0-generate-002',
        prompt: prompt,
        config: {
          numberOfImages: 1,
          outputMimeType: 'image/jpeg',
          aspectRatio: '3:4',
          seed: seed,
        },
    });

    if (response.generatedImages && response.generatedImages.length > 0) {
        const generatedImage = response.generatedImages[0];
        return {
            imageBytes: generatedImage.image.imageBytes,
            seed: (generatedImage as any).seed, // Use 'as any' as a temporary workaround for the type definition issue
        };
    }

    throw new Error("Image generation failed to produce an image.");
};
