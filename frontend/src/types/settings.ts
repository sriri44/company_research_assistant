// Settings page types. Everything here is local/mock — persisted to
// localStorage via useSettingsStore, never sent to a backend.

export interface ModelOption {
  id: string;
  name: string;
  provider: string;
  description: string;
  badge?: "fast" | "balanced" | "powerful";
}

export interface ApplicantInfo {
  applicantName: string;
  applicantEmail: string;
}

export interface DiscordConfig {
  webhookUrl: string;
  channelName: string;
}
