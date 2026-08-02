// Mirrors backend/app/models/opportunity.py — AI Growth Opportunities(tm)

export type ImpactLevel = "low" | "medium" | "high";
export type ComplexityLevel = "low" | "medium" | "high";

export interface Opportunity {
  title: string;
  description: string;
  category: string;
  impact: ImpactLevel;
  complexity: ComplexityLevel;
  priorityScore: number;
  estimatedRoi?: string | null;
}
