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
        "max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed sm:max-w-[75%]",
        isUser
          ? "rounded-tr-sm bg-primary text-primary-foreground"
          : "rounded-tl-sm border border-border bg-card text-card-foreground",
      )}
    >
      {children}
    </div>
  );
}
