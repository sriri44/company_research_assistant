// Mirrors backend/app/models/report.py

import type { Company } from "./company";
import type { Competitor } from "./competitor";
import type { Opportunity } from "./opportunity";

export type ReportStatus = "queued" | "processing" | "complete" | "failed";

export interface Report {
  id: string;
  company: Company;
  status: ReportStatus;
  summary: string | null;
  competitors: Competitor[];
  opportunities: Opportunity[];
  pdfUrl: string | null;
  createdAt: string | null;
  completedAt: string | null;
}
