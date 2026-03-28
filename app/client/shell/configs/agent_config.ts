import { EnhancedAgentAppConfig, ToolAssignments } from "./types.js";

const agents = {
  "nl2graphDB_agent": {
    model: "xai.grok-4-fast-reasoning",
    temperature: 0.7,
    name: "nl2graphDB_agent",
    systemPrompt: "Tu es un agent expert pour traduire des questions metier LIMAGRAIN Vegetable Seeds en requetes PGQL exploitables sur les donnees filieres, logistiques, qualite et tracabilite.",
    toolsEnabled: ["talk2DB", "semantic_search"]
  },
  "rag_agent": {
    model: "openai.gpt-oss-120b",
    temperature: 0.7,
    name: "rag_agent",
    systemPrompt: "Tu es un agent expert en recherche semantique et en generation augmentee pour retrouver des informations LIMAGRAIN Vegetable Seeds sur les filieres semences, les operations, la qualite, la tracabilite et les lancements.",
    toolsEnabled: ["talk2DB", "semantic_search"]
  },
  "ui_assembly_agent": {
    model: "xai.grok-4-fast-reasoning",
    temperature: 0.7,
    name: "ui_assembly_agent",
    systemPrompt: "Tu construis des interfaces dynamiques en francais pour des cas d usage LIMAGRAIN Vegetable Seeds: coordination de campagne, pilotage logistique, qualite, tracabilite, export et suivi des marques.",
    toolsEnabled: []
  }
};

const toolAssignments: ToolAssignments = {
  "talk2DB": "nl2graphDB_agent",
  "semantic_search": "nl2graphDB_agent",
};

export const agentConfig: EnhancedAgentAppConfig = {
  agents,
  toolAssignments
};
