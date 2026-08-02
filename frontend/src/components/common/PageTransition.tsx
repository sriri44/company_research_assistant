import { motion } from "framer-motion";
import type { ReactNode } from "react";

const VARIANTS = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
};

/** Wraps a route's page content with a subtle, professional fade/slide —
 * used inside <AnimatePresence mode="wait"> at the router level. */
export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={VARIANTS}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.2, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
