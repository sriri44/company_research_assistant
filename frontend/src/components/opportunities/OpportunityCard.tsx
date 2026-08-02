import { motion } from "framer-motion";
import { Gauge, LineChart, TrendingUp, Zap } from "lucide-react";
import { memo } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { ComplexityLevel, ImpactLevel, Opportunity } from "@/types/opportunity";
import { cn } from "@/utils/cn";

// Full static class strings — Tailwind's JIT scanner only picks up
// literal class names, so these must never be built with template
// literals (e.g. `bg-${x}/10`) or they'll be missing from the build.
const IMPACT_STYLE: Record<ImpactLevel, string> = {
  high: "bg-success/10 text-success",
  medium: "bg-warning/10 text-warning",
  low: "bg-secondary text-secondary-foreground",
};

const COMPLEXITY_STYLE: Record<ComplexityLevel, string> = {
  low: "bg-success/10 text-success",
  medium: "bg-warning/10 text-warning",
  high: "bg-destructive/10 text-destructive",
};

const RADIUS = 20;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

function PriorityGauge({ score }: { score: number }) {
  const offset = CIRCUMFERENCE * (1 - score / 100);

  return (
    <div className="relative flex size-14 shrink-0 items-center justify-center">
      <svg viewBox="0 0 48 48" className="size-14 -rotate-90">
        <circle cx="24" cy="24" r={RADIUS} className="fill-none stroke-secondary" strokeWidth="4" />
        <motion.circle
          cx="24"
          cy="24"
          r={RADIUS}
          className="fill-none stroke-primary"
          strokeWidth="4"
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          initial={{ strokeDashoffset: CIRCUMFERENCE }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.8, ease: "easeOut", delay: 0.15 }}
        />
      </svg>
      <span className="absolute text-sm font-semibold tabular-nums">{score}</span>
    </div>
  );
}

export interface OpportunityCardProps {
  opportunity: Opportunity;
  index?: number;
}

/** The flagship AI Growth Opportunities™ card — priority score as a
 * circular gauge for instant visual weight, impact/complexity as
 * color-coded badges beneath the description. Memoized (see
 * CompetitorCard for why). */
function OpportunityCardImpl({ opportunity, index = 0 }: OpportunityCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08 }}
    >
      <Card className="h-full border-primary/10 bg-gradient-to-b from-accent/40 to-card transition-shadow hover:shadow-soft-lg">
        <CardContent className="flex h-full flex-col gap-4 p-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <Badge variant="outline" className="mb-2">
                {opportunity.category}
              </Badge>
              <h4 className="text-sm font-semibold leading-snug">{opportunity.title}</h4>
            </div>
            <PriorityGauge score={opportunity.priorityScore} />
          </div>

          <p className="flex-1 text-sm text-muted-foreground">{opportunity.description}</p>

          {opportunity.estimatedRoi && (
            <div className="flex items-start gap-1.5 rounded-lg bg-success/5 px-2.5 py-2 text-xs text-success">
              <LineChart className="mt-0.5 size-3.5 shrink-0" />
              <span>{opportunity.estimatedRoi}</span>
            </div>
          )}

          <div className="flex flex-wrap items-center gap-2 border-t border-border pt-3">
            <span
              className={cn(
                "inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium",
                IMPACT_STYLE[opportunity.impact],
              )}
            >
              <TrendingUp className="size-3.5" />
              {opportunity.impact} impact
            </span>
            <span
              className={cn(
                "inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium",
                COMPLEXITY_STYLE[opportunity.complexity],
              )}
            >
              <Zap className="size-3.5" />
              {opportunity.complexity} complexity
            </span>
            <span className="ml-auto inline-flex items-center gap-1 text-xs font-medium text-muted-foreground">
              <Gauge className="size-3.5" />
              Priority {opportunity.priorityScore}/100
            </span>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export const OpportunityCard = memo(OpportunityCardImpl);
