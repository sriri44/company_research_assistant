import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button";

const STEPS = [
  {
    number: "01",
    title: "Enter a company",
    description: "Type a company name or website — Microsoft, Tesla, Stripe, or your own target.",
  },
  {
    number: "02",
    title: "Watch it research",
    description: "Follow the live progress timeline as it searches, crawls, and analyzes.",
  },
  {
    number: "03",
    title: "Get ranked insights",
    description: "Review the summary, competitors, and AI Growth Opportunities™ — export when ready.",
  },
];

export function LandingHowItWorks() {
  return (
    <section id="how-it-works" className="border-t border-border bg-secondary/30 py-20">
      <div className="container">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
            Three steps to a full research report
          </h2>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
          {STEPS.map((step, index) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-80px" }}
              transition={{ delay: index * 0.1, duration: 0.4 }}
              className="relative"
            >
              <span className="text-4xl font-bold text-primary/20">{step.number}</span>
              <h3 className="mt-3 text-base font-semibold">{step.title}</h3>
              <p className="mt-1.5 text-sm text-muted-foreground">{step.description}</p>
            </motion.div>
          ))}
        </div>

        <div className="mt-14 flex justify-center">
          <Button asChild size="lg" className="gap-2">
            <Link to="/research">
              Try it now
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
