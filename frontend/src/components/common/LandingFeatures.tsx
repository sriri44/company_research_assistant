import { motion } from "framer-motion";
import { Globe, Sparkles, Swords, TrendingUp } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";

const FEATURES = [
  {
    icon: Globe,
    title: "Search & Crawl",
    description: "Automatically finds and reads a company's web presence — no manual research needed.",
  },
  {
    icon: Sparkles,
    title: "AI Analysis",
    description: "Summarizes what a company does, its market position, and key operational pain points.",
  },
  {
    icon: Swords,
    title: "Competitor Intelligence",
    description: "Identifies and ranks the competitors that matter most, with similarity scoring.",
  },
  {
    icon: TrendingUp,
    title: "AI Growth Opportunities™",
    description: "Ranks automation ideas by business impact, complexity, and priority — ready to act on.",
  },
];

export function LandingFeatures() {
  return (
    <section id="features" className="container py-20">
      <div className="mx-auto max-w-2xl text-center">
        <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
          Everything you need, in one report
        </h2>
        <p className="mt-3 text-balance text-muted-foreground">
          One pipeline, four categories of insight — built for teams who need answers fast.
        </p>
      </div>

      <div className="mt-12 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {FEATURES.map(({ icon: Icon, title, description }, index) => (
          <motion.div
            key={title}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ delay: index * 0.08, duration: 0.4 }}
          >
            <Card className="h-full transition-shadow hover:shadow-soft-lg">
              <CardContent className="p-6">
                <span className="flex size-11 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Icon className="size-5" />
                </span>
                <h3 className="mt-4 text-sm font-semibold">{title}</h3>
                <p className="mt-1.5 text-sm text-muted-foreground">{description}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
