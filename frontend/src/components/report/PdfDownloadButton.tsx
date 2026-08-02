import { FileDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { useToastStore } from "@/hooks/useToastStore";

export interface PdfDownloadButtonProps {
  /** Enabled once research has completed successfully — actual PDF
   * generation is a later phase (see docs/ROADMAP.md Phase 6), so
   * clicking it while enabled shows a "coming soon" toast rather than
   * calling a backend endpoint that doesn't exist yet. */
  enabled?: boolean;
}

export function PdfDownloadButton({ enabled = false }: PdfDownloadButtonProps) {
  const showToast = useToastStore((state) => state.showToast);

  const handleClick = () => {
    showToast({
      title: "PDF export coming soon",
      description: "This report's PDF download will be available in a future update.",
    });
  };

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span tabIndex={enabled ? undefined : 0}>
          <Button
            variant="outline"
            size="sm"
            disabled={!enabled}
            onClick={handleClick}
            className="gap-2"
          >
            <FileDown className="size-4" />
            Export PDF
          </Button>
        </span>
      </TooltipTrigger>
      <TooltipContent>
        {enabled ? "PDF generation is coming in a future update." : "Available once research completes."}
      </TooltipContent>
    </Tooltip>
  );
}
