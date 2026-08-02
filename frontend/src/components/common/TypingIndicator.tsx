import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

const DOT_TRANSITION = (delay: number) => ({
  duration: 0.9,
  repeat: Infinity,
  ease: "easeInOut" as const,
  delay,
});

/** The "assistant is thinking" indicator shown between pipeline steps. */
export function TypingIndicator() {
  return (
    <div className="flex items-center gap-3" role="status" aria-label="Assistant is typing">
      <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
        <Sparkles className="size-4" />
      </span>
      <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm border border-border bg-card px-4 py-3.5">
        {[0, 1, 2].map((index) => (
          <motion.span
            key={index}
            className="size-1.5 rounded-full bg-muted-foreground"
            animate={{ y: ["0%", "-40%", "0%"] }}
            transition={DOT_TRANSITION(index * 0.15)}
          />
        ))}
      </div>
    </div>
  );
}
