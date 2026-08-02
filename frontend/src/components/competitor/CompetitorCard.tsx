import { motion } from "framer-motion";
import { Swords } from "lucide-react";
import { memo } from "react";

import { Card, CardContent } from "@/components/ui/card";
import type { Competitor } from "@/types/competitor";

export interface CompetitorCardProps {
  competitor: Competitor;
  index?: number;
}

/** One competitor row/card — similarity score rendered as a compact
 * progress bar for quick visual scanning across a grid. Memoized since
 * these render in a grid that shouldn't re-render on unrelated page state
 * changes (e.g. typing in the prompt input). */
function CompetitorCardImpl({ competitor, index = 0 }: CompetitorCardProps) {
  const similarityPct = Math.round(competitor.similarityScore * 100);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06 }}
    >
      <Card className="h-full transition-shadow hover:shadow-soft-lg">
        <CardContent className="flex h-full flex-col gap-3 p-5">
          <div className="flex items-center gap-2.5">
            <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
              <Swords className="size-4" />
            </span>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">{competitor.name}</p>
              <p className="truncate text-xs text-muted-foreground">{competitor.domain}</p>
            </div>
          </div>

          {competitor.summary && (
            <p className="flex-1 text-sm text-muted-foreground">{competitor.summary}</p>
          )}

          <div>
            <div className="mb-1 flex items-center justify-between text-xs text-muted-foreground">
              <span>Similarity</span>
              <span className="font-medium text-foreground">{similarityPct}%</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-secondary">
              <motion.div
                className="h-full rounded-full bg-primary"
                initial={{ width: 0 }}
                animate={{ width: `${similarityPct}%` }}
                transition={{ duration: 0.6, delay: 0.2 + index * 0.06, ease: "easeOut" }}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export const CompetitorCard = memo(CompetitorCardImpl);
