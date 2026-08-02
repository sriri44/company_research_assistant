import { create } from "zustand";

import { ApiError } from "@/services/api";
import { mapResearchResponse } from "@/services/researchMapper";
import { researchService } from "@/services/researchService";
import type { ChatMessage } from "@/types/chat";
import type { ResearchResult, ResearchSessionStatus, ResearchStep, ResearchStepId } from "@/types/research";
import { delay } from "@/utils/delay";
import { RESEARCH_STEP_DEFINITIONS } from "@/utils/mockData/researchSteps";

import { useSettingsStore } from "./useSettingsStore";

// The real backend is a single synchronous call with no stage-by-stage
// streaming (see docs/API_DESIGN.md) — these durations only pace the
// progress timeline while we wait. The final step never completes on a
// timer; it completes only when the real response arrives (or snaps
// forward immediately if the response beats the clock).
const STEP_PACE_MS: Record<ResearchStepId, number> = {
  resolve: 900,
  search: 1200,
  crawl: 6000,
  analyze: 5000,
  competitors: 1500,
  opportunities: 1500,
  report: 400,
};

function freshSteps(): ResearchStep[] {
  return RESEARCH_STEP_DEFINITIONS.map((definition) => ({ ...definition, status: "pending" }));
}

function completedSteps(): ResearchStep[] {
  return RESEARCH_STEP_DEFINITIONS.map((definition) => ({ ...definition, status: "complete" }));
}

function newMessage(role: ChatMessage["role"], content: string): ChatMessage {
  return { id: crypto.randomUUID(), role, content, createdAt: new Date().toISOString() };
}

interface ConversationState {
  messages: ChatMessage[];
  steps: ResearchStep[];
  sessionStatus: ResearchSessionStatus;
  result: ResearchResult | null;
  isTyping: boolean;
  error: string | null;
  startResearch: (query: string) => Promise<void>;
  reset: () => void;
}

// Imperative handles (abort controller, step-pacing timer) — not
// reactive state, kept outside the store like any other subscription.
let activeAbortController: AbortController | null = null;
let stepTimer: ReturnType<typeof setTimeout> | null = null;

function clearStepTimer(): void {
  if (stepTimer !== null) {
    clearTimeout(stepTimer);
    stepTimer = null;
  }
}

/** Deliberately not persisted — the sidebar's "Recent Session" is
 * temporary-only per spec, cleared on reload. `startResearch` calls the
 * real POST /api/v1/research endpoint; starting a new search cancels any
 * request already in flight. */
export const useConversationStore = create<ConversationState>((set) => ({
  messages: [],
  steps: freshSteps(),
  sessionStatus: "idle",
  result: null,
  isTyping: false,
  error: null,

  startResearch: async (query: string) => {
    const trimmed = query.trim();
    if (!trimmed) return;

    activeAbortController?.abort();
    clearStepTimer();
    const controller = new AbortController();
    activeAbortController = controller;
    const { signal } = controller;

    set((state) => ({
      messages: [...state.messages, newMessage("user", trimmed)],
      sessionStatus: "running",
      result: null,
      error: null,
      steps: freshSteps(),
      isTyping: true,
    }));

    await delay(500);
    if (signal.aborted) return;
    set((state) => ({
      isTyping: false,
      messages: [
        ...state.messages,
        newMessage("assistant", `Starting research on "${trimmed}"...`),
      ],
    }));

    const stepIds = RESEARCH_STEP_DEFINITIONS.map((definition) => definition.id);
    const paceSteps = (index: number): void => {
      if (signal.aborted || index >= stepIds.length - 1) return; // last step completes with the response, not the clock
      set((state) => ({
        steps: state.steps.map((step) => (step.id === stepIds[index] ? { ...step, status: "active" } : step)),
      }));
      stepTimer = setTimeout(() => {
        set((state) => ({
          steps: state.steps.map((step) => (step.id === stepIds[index] ? { ...step, status: "complete" } : step)),
        }));
        paceSteps(index + 1);
      }, STEP_PACE_MS[stepIds[index]]);
    };
    paceSteps(0);

    const model = useSettingsStore.getState().selectedModelId;

    try {
      const response = await researchService.startResearch({ query: trimmed, model, signal });
      if (signal.aborted) return;
      clearStepTimer();

      if (response.status === "failed") {
        set({
          sessionStatus: "error",
          isTyping: false,
          steps: completedSteps(),
          result: null,
          error: response.summary ?? "Research could not be completed for this company.",
        });
        set((state) => ({
          messages: [
            ...state.messages,
            newMessage("assistant", response.summary ?? "Research could not be completed."),
          ],
        }));
        return;
      }

      const result = mapResearchResponse(response);
      set({ steps: completedSteps() });
      set((state) => ({
        result,
        sessionStatus: "complete",
        error: null,
        messages: [
          ...state.messages,
          newMessage(
            "assistant",
            `Research complete for ${result.company.name}. Here's the summary, competitor landscape, and ${result.opportunities.length} AI Growth Opportunities™ I found.`,
          ),
        ],
      }));
    } catch (error) {
      if (signal.aborted) return;
      clearStepTimer();
      const message = error instanceof ApiError ? error.message : "Something went wrong. Please try again.";
      set((state) => ({
        sessionStatus: "error",
        isTyping: false,
        result: null,
        error: message,
        messages: [...state.messages, newMessage("assistant", message)],
      }));
    }
  },

  reset: () => {
    activeAbortController?.abort();
    clearStepTimer();
    set({
      messages: [],
      steps: freshSteps(),
      sessionStatus: "idle",
      result: null,
      isTyping: false,
      error: null,
    });
  },
}));
