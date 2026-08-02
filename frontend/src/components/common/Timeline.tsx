import { motion } from "framer-motion";
import { memo } from "react";

import { ProgressStep } from "@/components/common/ProgressStep";
import type { ResearchStep } from "@/types/research";

export interface TimelineProps {
  steps: ResearchStep[];
}

/** The research pipeline progress card shown while a session runs.
 * Memoized so it only re-renders when `steps` actually changes, not on
 * unrelated ResearchPage state updates (e.g. typing in the prompt). */
function TimelineImpl({ steps }: TimelineProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-md rounded-2xl border border-border bg-card p-5 shadow-soft"
    >
      <p className="mb-4 text-xs font-medium uppercase tracking-wide text-muted-foreground">
        Research Progress
      </p>
      <ol>
        {steps.map((step, index) => (
          <ProgressStep key={step.id} step={step} isLast={index === steps.length - 1} />
        ))}
      </ol>
    </motion.div>
  );
}

export const Timeline = memo(TimelineImpl);
