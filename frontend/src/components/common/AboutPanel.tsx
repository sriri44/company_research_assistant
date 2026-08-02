import { AnimatePresence, motion } from "framer-motion";
import { Sparkles, X } from "lucide-react";
import { useEffect } from "react";

import { Button } from "@/components/ui/button";

export interface AboutPanelProps {
  open: boolean;
  onClose: () => void;
}

/** A lightweight, dependency-free modal (no radix Dialog needed for a
 * single static info panel) — Escape-to-close, backdrop click, focus
 * returns to the trigger implicitly since we don't steal it. */
export function AboutPanel({ open, onClose }: AboutPanelProps) {
  useEffect(() => {
    if (!open) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-background/60 backdrop-blur-sm"
            onClick={onClose}
            aria-hidden="true"
          />
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby="about-panel-title"
            initial={{ opacity: 0, scale: 0.96, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 8 }}
            transition={{ type: "spring", stiffness: 380, damping: 32 }}
            className="fixed left-1/2 top-1/2 z-50 w-[calc(100%-2rem)] max-w-md -translate-x-1/2 -translate-y-1/2
              rounded-xl border border-border bg-card p-6 text-card-foreground shadow-soft-lg"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <Sparkles className="size-5" />
                </span>
                <div>
                  <h2 id="about-panel-title" className="text-sm font-semibold">
                    AI Company Research Assistant
                  </h2>
                  <p className="text-xs text-muted-foreground">Frontend demo build — v0.1.0</p>
                </div>
              </div>
              <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close about panel">
                <X className="size-4" />
              </Button>
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              Enter a company name or website and this app walks through search, crawling, AI
              analysis, competitor mapping, and{" "}
              <span className="font-medium text-foreground">AI Growth Opportunities™</span> —
              ranked automation ideas with estimated impact, complexity, and priority. This build
              runs entirely on mock data; no requests leave your browser.
            </p>
            <Button className="mt-5 w-full" onClick={onClose}>
              Got it
            </Button>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
