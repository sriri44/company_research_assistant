// Mirrors backend/app/models/competitor.py

export interface Competitor {
  name: string;
  domain: string;
  similarityScore: number;
  summary: string | null;
  marketPosition?: string | null;
}
