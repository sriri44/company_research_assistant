import { motion } from "framer-motion";
import { Sparkles, User } from "lucide-react";

import { ChatBubble } from "@/components/common/ChatBubble";
import type { ChatMessage } from "@/types/chat";
import { cn } from "@/utils/cn";

export interface MessageProps {
  message: ChatMessage;
}

/** A single animated conversation turn: avatar + ChatBubble, aligned by
 * role, with a spring entrance so new messages feel alive without being
 * distracting. */
export function Message({ message }: MessageProps) {
  const isUser = message.role === "user";

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 380, damping: 32 }}
      className={cn("flex items-start gap-3", isUser && "flex-row-reverse")}
    >
      <span
        className={cn(
          "flex size-8 shrink-0 items-center justify-center rounded-full",
          isUser ? "bg-secondary text-secondary-foreground" : "bg-primary text-primary-foreground",
        )}
        aria-hidden="true"
      >
        {isUser ? <User className="size-4" /> : <Sparkles className="size-4" />}
      </span>
      <ChatBubble role={message.role}>{message.content}</ChatBubble>
    </motion.div>
  );
}
