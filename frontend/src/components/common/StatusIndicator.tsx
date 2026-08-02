import type { ResearchSessionStatus } from "@/types/research";
import { cn } from "@/utils/cn";

const STATUS_CONFIG: Record<ResearchSessionStatus, { label: string; dotClass: string }> = {
  idle: { label: "Idle", dotClass: "bg-muted-foreground" },
  running: { label: "Researching…", dotClass: "bg-warning animate-pulse" },
  complete: { label: "Complete", dotClass: "bg-success" },
  error: { label: "Failed", dotClass: "bg-destructive" },
};

export interface StatusIndicatorProps {
  status: ResearchSessionStatus;
}

export function StatusIndicator({ status }: StatusIndicatorProps) {
  const config = STATUS_CONFIG[status];

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-secondary/60 px-2.5 py-1 text-xs font-medium text-muted-foreground">
      <span className={cn("size-1.5 rounded-full", config.dotClass)} aria-hidden="true" />
      {config.label}
    </span>
  );
}
