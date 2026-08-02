import { useEffect, useRef, type RefObject } from "react";

/** Keeps a scroll container pinned to its bottom whenever `deps` change
 * (new message, typing indicator toggling, etc.) — the standard chat-UI
 * auto-scroll behavior. */
export function useAutoScroll<T extends HTMLElement>(deps: unknown[]): RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    node.scrollTo({ top: node.scrollHeight, behavior: "smooth" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return ref;
}
