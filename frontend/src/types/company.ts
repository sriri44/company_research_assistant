// Mirrors backend/app/models/company.py

export interface Company {
  id: string;
  name: string;
  domain: string;
  aliases: string[];
  industry: string | null;
  description: string | null;
  resolvedAt: string | null;
}
