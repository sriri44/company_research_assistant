import { useEffect, useRef, type RefObject } from "react";

/** Keeps a bottom "sentinel" element scrolled into view smoothly whenever
 * `deps` change (new message, typing indicator toggling, research
 * finishing, etc.) — the standard chat-UI auto-scroll pattern used by
 * ChatGPT/Perplexity. Attach the returned ref to an empty element placed
 * *after* the last piece of content in the scrollable area.
 *
 * Deferred one frame via `requestAnimationFrame` so it runs after the
 * browser has laid out the new content — no `setTimeout` guesswork about
 * how long that takes. */
export function useAutoScroll<T extends HTMLElement>(deps: unknown[]): RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      ref.current?.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    });
    return () => cancelAnimationFrame(frame);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return ref;
}
