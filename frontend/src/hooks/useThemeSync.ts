import { useEffect, useState } from "react";

import { useThemeStore } from "./useThemeStore";

const DARK_QUERY = "(prefers-color-scheme: dark)";

/** Applies the persisted theme preference to <html class="dark">,
 * tracking OS-level changes while in "system" mode. Call once near the
 * app root. Returns the resolved light/dark value for UI that needs to
 * display the *effective* theme (e.g. the theme toggle icon). */
export function useThemeSync(): "light" | "dark" {
  const theme = useThemeStore((state) => state.theme);
  const [resolved, setResolved] = useState<"light" | "dark">(() =>
    theme === "dark" || (theme === "system" && window.matchMedia(DARK_QUERY).matches)
      ? "dark"
      : "light",
  );

  useEffect(() => {
    const root = document.documentElement;
    const apply = (isDark: boolean) => {
      root.classList.toggle("dark", isDark);
      setResolved(isDark ? "dark" : "light");
    };

    if (theme !== "system") {
      apply(theme === "dark");
      return;
    }

    const mediaQuery = window.matchMedia(DARK_QUERY);
    apply(mediaQuery.matches);
    const handleChange = (event: MediaQueryListEvent) => apply(event.matches);
    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, [theme]);

  return resolved;
}
