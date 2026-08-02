import { motion } from "framer-motion";
import type { ReactNode } from "react";

const VARIANTS = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
};

/** Wraps a route's page content with a subtle, professional fade/slide —
 * used inside <AnimatePresence mode="wait"> at the router level.
 *
 * `flex h-full min-h-0 flex-col` makes this div a transparent passthrough
 * for height instead of an unstyled box that shrinks to content: without
 * it, this sits between <main> and the page's own `h-full` root, breaking
 * the height chain so pages like ResearchPage can't constrain their own
 * height and scroll internally. Harmless on MarketingLayout, where `main`
 * has no fixed height and the percentage simply resolves to auto. */
export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={VARIANTS}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.2, ease: "easeOut" }}
      className="flex h-full min-h-0 flex-1 flex-col"
    >
      {children}
    </motion.div>
  );
}
