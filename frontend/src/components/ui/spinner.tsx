import { Loader2 } from "lucide-react";

import { cn } from "@/utils/cn";

export interface SpinnerProps {
  className?: string;
  size?: number;
  label?: string;
}

/** The app's single Loader primitive — every loading state (buttons,
 * page fallback, pipeline steps) renders this rather than a bespoke
 * spinner. */
export function Spinner({ className, size = 16, label = "Loading" }: SpinnerProps) {
  return (
    <span role="status" aria-label={label} className="inline-flex">
      <Loader2 className={cn("animate-spin text-current", className)} size={size} />
      <span className="sr-only">{label}</span>
    </span>
  );
}
