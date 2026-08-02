import { motion } from "framer-motion";
import { Check } from "lucide-react";

import type { ResearchStep } from "@/types/research";
import { cn } from "@/utils/cn";

export interface ProgressStepProps {
  step: ResearchStep;
  isLast: boolean;
}

/** One row in the research pipeline Timeline: status icon + connecting
 * line + label/description. Animates from pending -> active -> complete. */
export function ProgressStep({ step, isLast }: ProgressStepProps) {
  const isComplete = step.status === "complete";
  const isActive = step.status === "active";

  return (
    <li className="relative flex gap-3 pb-6 last:pb-0">
      {!isLast && (
        <span
          className={cn(
            "absolute left-[11px] top-6 h-[calc(100%-1.25rem)] w-px transition-colors duration-500",
            isComplete ? "bg-primary" : "bg-border",
          )}
          aria-hidden="true"
        />
      )}

      <motion.span
        className={cn(
          "relative flex size-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors",
          isComplete && "border-primary bg-primary text-primary-foreground",
          isActive && "border-primary bg-background text-primary",
          step.status === "pending" && "border-border bg-background text-muted-foreground",
        )}
        animate={isActive ? { scale: [1, 1.12, 1] } : { scale: 1 }}
        transition={isActive ? { duration: 1.4, repeat: Infinity, ease: "easeInOut" } : undefined}
      >
        {isComplete ? (
          <Check className="size-3.5" />
        ) : (
          <span
            className={cn("size-2 rounded-full bg-current", isActive && "animate-pulse")}
            aria-hidden="true"
          />
        )}
      </motion.span>

      <div className="flex-1 pt-0.5">
        <p
          className={cn(
            "text-sm font-medium transition-colors",
            step.status === "pending" ? "text-muted-foreground" : "text-foreground",
          )}
        >
          {step.label}
        </p>
        <p className="text-xs text-muted-foreground">{step.description}</p>
      </div>
    </li>
  );
}
