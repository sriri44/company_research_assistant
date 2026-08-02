import { motion } from "framer-motion";
import { Link2, Sparkles, Swords } from "lucide-react";

import { CompanyCard } from "@/components/company/CompanyCard";
import { CompetitorCard } from "@/components/competitor/CompetitorCard";
import { OpportunityGrid } from "@/components/opportunities/OpportunityGrid";
import type { ResearchResult } from "@/types/research";

export interface ResearchSummaryProps {
  result: ResearchResult;
}

/** The full completed-research view: company overview, competitor grid,
 * AI Growth Opportunities™, and the crawled sources the analysis drew
 * from, in that order. */
export function ResearchSummary({ result }: ResearchSummaryProps) {
  return (
    <div className="space-y-8">
      <CompanyCard company={result.company} confidence={result.confidence} />

      <section aria-labelledby="competitors-heading">
        <h3 id="competitors-heading" className="mb-3 flex items-center gap-2 text-sm font-semibold">
          <Swords className="size-4 text-muted-foreground" />
          Competitor Landscape
        </h3>
        {result.competitors.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {result.competitors.map((competitor, index) => (
              <CompetitorCard key={competitor.domain || competitor.name} competitor={competitor} index={index} />
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            No competitors could be confidently identified from the available content.
          </p>
        )}
      </section>

      <section aria-labelledby="opportunities-heading">
        <h3 id="opportunities-heading" className="mb-3 flex items-center gap-2 text-sm font-semibold">
          <Sparkles className="size-4 text-primary" />
          AI Growth Opportunities™
        </h3>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          <OpportunityGrid opportunities={result.opportunities} />
        </motion.div>
      </section>

      {result.sources.length > 0 && (
        <section aria-labelledby="sources-heading">
          <h3 id="sources-heading" className="mb-3 flex items-center gap-2 text-sm font-semibold">
            <Link2 className="size-4 text-muted-foreground" />
            Sources
          </h3>
          <ul className="space-y-1">
            {result.sources.map((source) => (
              <li key={source} className="truncate">
                <a
                  href={source}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-muted-foreground underline-offset-2 hover:text-primary hover:underline"
                >
                  {source}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
