import { FileDown } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { useToastStore } from "@/hooks/useToastStore";
import { ApiError } from "@/services/api";
import { reportService } from "@/services/reportService";

export interface PdfDownloadButtonProps {
  /** The completed research session's report id — GET /api/v1/report/{id}/pdf
   * is called with this. `null` while research is running/hasn't started. */
  reportId?: string | null;
  /** Enabled once research has completed successfully. */
  enabled?: boolean;
}

export function PdfDownloadButton({ reportId = null, enabled = false }: PdfDownloadButtonProps) {
  const showToast = useToastStore((state) => state.showToast);
  const [isGenerating, setIsGenerating] = useState(false);

  const canDownload = enabled && Boolean(reportId) && !isGenerating;

  const handleClick = async () => {
    if (!reportId || isGenerating) return;

    setIsGenerating(true);
    try {
      await reportService.downloadPdf(reportId);
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "Something went wrong while generating the PDF.";
      showToast({
        title: "Couldn't generate PDF",
        description: message,
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const tooltipText = isGenerating
    ? "Generating PDF…"
    : enabled
      ? "Download this report as a PDF."
      : "Available once research completes.";

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span tabIndex={canDownload || enabled ? undefined : 0}>
          <Button
            variant="outline"
            size="sm"
            disabled={!canDownload}
            onClick={handleClick}
            className="gap-2"
          >
            {isGenerating ? <Spinner size={14} label="Generating PDF" /> : <FileDown className="size-4" />}
            {isGenerating ? "Generating PDF…" : "Export PDF"}
          </Button>
        </span>
      </TooltipTrigger>
      <TooltipContent>{tooltipText}</TooltipContent>
    </Tooltip>
  );
}
