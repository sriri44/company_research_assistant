import { Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

import { cn } from "@/utils/cn";

export interface LogoProps {
  className?: string;
  iconOnly?: boolean;
}

export function Logo({ className, iconOnly = false }: LogoProps) {
  return (
    <Link
      to="/"
      className={cn(
        "inline-flex items-center gap-2 rounded-md focus-visible:outline-none focus-visible:ring-2",
        "focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        className,
      )}
      aria-label="AI Company Research Assistant — home"
    >
      <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
        <Sparkles className="size-4" strokeWidth={2.25} />
      </span>
      {!iconOnly && (
        <span className="text-sm font-semibold tracking-tight">
          Research<span className="text-primary">AI</span>
        </span>
      )}
    </Link>
  );
}
