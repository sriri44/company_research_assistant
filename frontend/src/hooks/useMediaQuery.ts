import { useEffect, useState } from "react";

/** Tracks a CSS media query's match state, used to drive responsive
 * behavior (e.g. collapsing the sidebar into a drawer on smaller
 * screens) from JS rather than duplicating breakpoints in Tailwind-only
 * conditional rendering. */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    const handleChange = () => setMatches(mediaQuery.matches);
    handleChange();
    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, [query]);

  return matches;
}
