import type { ReactNode } from "react";

import type { MessageRole } from "@/types/chat";
import { cn } from "@/utils/cn";

export interface ChatBubbleProps {
  role: MessageRole;
  children: ReactNode;
}

/** Pure visual shell for a single chat turn — role-based alignment and
 * color, no animation/state of its own (see `Message.tsx` for that). */
export function ChatBubble({ role, children }: ChatBubbleProps) {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        // Percentage cap keeps bubbles from touching the edge on small
        // screens; the lg:max-w-2xl hard cap keeps long AI text at a
        // comfortable reading measure even in the wider 1100px container
        // (research result cards use the full width instead — see
        // ResearchSummary).
        "max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed sm:max-w-[75%] lg:max-w-2xl",
        isUser
          ? "rounded-tr-sm bg-primary text-primary-foreground"
          : "rounded-tl-sm border border-border bg-card text-card-foreground",
      )}
    >
      {children}
    </div>
  );
}
