import { OpportunityCard } from "@/components/opportunities/OpportunityCard";
import type { Opportunity } from "@/types/opportunity";

export interface OpportunityGridProps {
  opportunities: Opportunity[];
}

/** Ranked highest-priority-first grid of AI Growth Opportunities™ cards. */
export function OpportunityGrid({ opportunities }: OpportunityGridProps) {
  const sorted = [...opportunities].sort((a, b) => b.priorityScore - a.priorityScore);

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {sorted.map((opportunity, index) => (
        <OpportunityCard key={opportunity.title} opportunity={opportunity} index={index} />
      ))}
    </div>
  );
}
