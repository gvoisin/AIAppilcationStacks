import { LLMConfig } from "./types.js";

export const chatConfig: LLMConfig = {
  model: "openai.gpt-4.1",
  temperature: 0.7,
  name: "assistant_limagrain",
  systemPrompt: "Tu es un assistant IA LIMAGRAIN Vegetable Seeds. Tu aides les equipes a analyser les filieres de semences potageres, la logistique, la qualite, la tracabilite, les campagnes et les alertes operationnelles. Reponds en francais avec des formulations claires, concretes et orientees metier.",
  toolsEnabled: []
};
