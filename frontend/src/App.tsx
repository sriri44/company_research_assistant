import { AnimatePresence } from "framer-motion";
import { lazy, Suspense } from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import { PageTransition } from "@/components/common/PageTransition";
import { ToastViewport } from "@/components/common/Toast";
import { Spinner } from "@/components/ui/spinner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useThemeSync } from "@/hooks/useThemeSync";
import { AppLayout } from "@/layouts/AppLayout";
import { MarketingLayout } from "@/layouts/MarketingLayout";

// Route-level code splitting: each page (and its dependencies — react-hook-form,
// the radix-based Settings controls, etc.) ships in its own chunk instead of
// bloating the initial bundle. See docs/ROADMAP.md-adjacent perf notes in the
// final delivery summary.
const LandingPage = lazy(() => import("@/pages/LandingPage"));
const ResearchPage = lazy(() => import("@/pages/ResearchPage"));
const SettingsPage = lazy(() => import("@/pages/SettingsPage"));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage"));

function RouteFallback() {
  return (
    <div className="flex h-[60vh] items-center justify-center">
      <Spinner size={22} label="Loading page" />
    </div>
  );
}

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route element={<MarketingLayout />}>
          <Route
            path="/"
            element={
              <PageTransition>
                <LandingPage />
              </PageTransition>
            }
          />
          <Route
            path="*"
            element={
              <PageTransition>
                <NotFoundPage />
              </PageTransition>
            }
          />
        </Route>

        <Route element={<AppLayout />}>
          <Route
            path="/research"
            element={
              <PageTransition>
                <ResearchPage />
              </PageTransition>
            }
          />
          <Route
            path="/settings"
            element={
              <PageTransition>
                <SettingsPage />
              </PageTransition>
            }
          />
        </Route>
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  useThemeSync();

  return (
    <TooltipProvider delayDuration={150}>
      <Suspense fallback={<RouteFallback />}>
        <AnimatedRoutes />
      </Suspense>
      <ToastViewport />
    </TooltipProvider>
  );
}
