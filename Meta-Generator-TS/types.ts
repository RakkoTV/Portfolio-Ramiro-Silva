
export interface Ability {
  name: string;
  description: string;
}

export interface CharacterDetails {
  backstory: string;
  abilities: Ability[];
}

export interface CharacterData extends CharacterDetails {
  name: string;
  portraitUrl: string;
}
