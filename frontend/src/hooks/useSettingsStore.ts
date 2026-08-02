import { create } from "zustand";
import { persist } from "zustand/middleware";

import { DEFAULT_MODEL_ID } from "@/utils/mockData/models";

interface SettingsState {
  selectedModelId: string;
  applicantName: string;
  applicantEmail: string;
  discordWebhookUrl: string;
  discordChannel: string;
  lastSavedAt: string | null;
  setSelectedModelId: (modelId: string) => void;
  saveSettings: (values: {
    applicantName: string;
    applicantEmail: string;
    discordWebhookUrl: string;
    discordChannel: string;
  }) => void;
}

/** All settings are local-only and persisted to localStorage — there is
 * no backend to save to yet (see docs/ROADMAP.md). `saveSettings` exists
 * to make that explicit at the call site rather than mutating fields
 * ad hoc. */
export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      selectedModelId: DEFAULT_MODEL_ID,
      applicantName: "",
      applicantEmail: "",
      discordWebhookUrl: "",
      discordChannel: "",
      lastSavedAt: null,
      setSelectedModelId: (modelId) => set({ selectedModelId: modelId }),
      saveSettings: (values) =>
        set({
          ...values,
          lastSavedAt: new Date().toISOString(),
        }),
    }),
    { name: "research-assistant-settings" },
  ),
);
