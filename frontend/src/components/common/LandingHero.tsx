import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

import { OpportunityCard } from "@/components/opportunities/OpportunityCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Opportunity } from "@/types/opportunity";

// A single hand-authored illustrative example for the hero preview card —
// marketing copy, not a research result, so it's kept separate from (and
// isn't affected by) the real API integration.
const previewOpportunity: Opportunity = {
  title: "Automated Fraud Pattern Detection",
  description:
    "Continuously surface emerging fraud patterns across your transaction network faster than static rule sets allow.",
  category: "AI Growth Opportunity",
  impact: "high",
  complexity: "high",
  priorityScore: 90,
  estimatedRoi: "Reduced chargeback losses within the first quarter",
};

export function LandingHero() {
  return (
    <section className="relative overflow-hidden">
      <div
        className="pointer-events-none absolute inset-x-0 -top-40 -z-10 h-[36rem] bg-[radial-gradient(circle_at_50%_0%,hsl(var(--primary)/0.16),transparent_65%)]"
        aria-hidden="true"
      />

      <div className="container grid grid-cols-1 items-center gap-12 py-20 md:py-28 lg:grid-cols-[1.1fr_0.9fr]">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <Badge variant="secondary" className="mb-5">
            <Sparkles className="size-3.5" />
            AI-Powered Company Research
          </Badge>
          <h1 className="text-balance text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Research any company <span className="text-primary">in seconds.</span>
          </h1>
          <p className="mt-5 max-w-lg text-balance text-lg text-muted-foreground">
            Enter a name or website and get an instant company summary, competitor landscape, and
            ranked <span className="font-medium text-foreground">AI Growth Opportunities™</span> —
            no spreadsheets, no manual digging.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Button asChild size="lg" className="gap-2">
              <Link to="/research">
                Start Research
                <ArrowRight className="size-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <a href="#how-it-works">See how it works</a>
            </Button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.94, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15, ease: "easeOut" }}
          className="relative mx-auto w-full max-w-sm"
        >
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
          >
            <OpportunityCard opportunity={previewOpportunity} />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
