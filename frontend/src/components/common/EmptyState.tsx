import { motion } from "framer-motion";
import { Building2, Rocket, Sparkles } from "lucide-react";

import { useConversationStore } from "@/hooks/useConversationStore";

const SUGGESTIONS = [
  { label: "Research Microsoft", icon: Building2 },
  { label: "Research Tesla", icon: Rocket },
  { label: "Research Stripe", icon: Sparkles },
];

/** Shown before the first message — sets expectations and offers one-tap
 * demo suggestions instead of a blank textbox. */
export function EmptyState() {
  const startResearch = useConversationStore((state) => state.startResearch);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex h-full flex-col items-center justify-center gap-6 px-4 text-center"
    >
      <span className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
        <Sparkles className="size-6" />
      </span>
      <div className="space-y-2">
        <h2 className="text-xl font-semibold tracking-tight">Who should I research?</h2>
        <p className="max-w-sm text-sm text-muted-foreground">
          Enter a company name or website below, or try one of these sample companies.
        </p>
      </div>
      <div className="flex flex-wrap justify-center gap-2">
        {SUGGESTIONS.map(({ label, icon: Icon }) => (
          <button
            key={label}
            onClick={() => startResearch(label.replace("Research ", ""))}
            className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-4 py-2
              text-sm font-medium shadow-soft transition-colors hover:border-primary/40 hover:bg-accent
              hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2
              focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
          >
            <Icon className="size-4 text-muted-foreground" />
            {label}
          </button>
        ))}
      </div>
    </motion.div>
  );
}
