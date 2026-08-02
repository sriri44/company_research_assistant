// Conversation UI types for the Research page. Entirely local/mock state —
// no backend message format to mirror yet.

export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: string;
}
