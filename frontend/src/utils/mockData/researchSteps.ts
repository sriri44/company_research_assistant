// Defines the mock research pipeline shown in the progress Timeline.
// Mirrors the conceptual pipeline in docs/ARCHITECTURE.md §8 — purely
// presentational here, driven by useConversationStore's simulated timing.

import type { ResearchStepId } from "@/types/research";

export const RESEARCH_STEP_DEFINITIONS: Array<{
  id: ResearchStepId;
  label: string;
  description: string;
}> = [
  { id: "resolve", label: "Searching…", description: "Looking up the company" },
  { id: "search", label: "Website found", description: "Confirming official web presence" },
  { id: "crawl", label: "Crawling…", description: "Extracting content from the company site" },
  { id: "analyze", label: "AI Analysis…", description: "Summarizing findings and key signals" },
  { id: "competitors", label: "Competitors…", description: "Identifying and ranking competitors" },
  {
    id: "opportunities",
    label: "Growth Opportunities…",
    description: "Scoring AI Growth Opportunities™",
  },
  { id: "report", label: "Completed", description: "Research finished" },
];
