import { AnimatePresence, motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";

import { Logo } from "@/components/common/Logo";
import { Sidebar } from "@/components/common/Sidebar";
import { Button } from "@/components/ui/button";

/** Shell for /research and /settings: a persistent sidebar on desktop,
 * a slide-in drawer (with backdrop, Escape-to-close) on tablet/mobile. */
export function AppLayout() {
  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    if (!drawerOpen) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setDrawerOpen(false);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [drawerOpen]);

  return (
    <div className="flex h-dvh overflow-hidden bg-background">
      <aside className="hidden w-64 shrink-0 border-r border-border md:block">
        <Sidebar />
      </aside>

      <AnimatePresence>
        {drawerOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-background/60 backdrop-blur-sm md:hidden"
              onClick={() => setDrawerOpen(false)}
              aria-hidden="true"
            />
            <motion.aside
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "spring", stiffness: 340, damping: 34 }}
              className="fixed inset-y-0 left-0 z-50 w-72 border-r border-border bg-background md:hidden"
            >
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setDrawerOpen(false)}
                aria-label="Close sidebar"
                className="absolute right-2 top-2 z-10"
              >
                <X className="size-4" />
              </Button>
              <Sidebar onNavigate={() => setDrawerOpen(false)} />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <div className="flex min-h-0 min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center gap-3 border-b border-border px-4 md:hidden">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setDrawerOpen(true)}
            aria-label="Open sidebar"
          >
            <Menu className="size-5" />
          </Button>
          <Logo iconOnly />
        </header>

        {/* min-h-0 is load-bearing here: without it, a flex child defaults
            to min-height:auto and won't shrink below its content's
            intrinsic height, so long research results push this element
            (and the whole page) taller than the viewport instead of
            scrolling inside ResearchPage's own scroll area. */}
        <main className="min-h-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
