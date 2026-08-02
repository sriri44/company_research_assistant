import { motion } from "framer-motion";
import { AlertTriangle, Building2, Calendar, MapPin, Phone, ShieldCheck, Users } from "lucide-react";
import { memo } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import type { CompanyProfile } from "@/types/research";

interface MetaItem {
  icon: typeof Phone;
  label: string;
  value: string;
}

function buildMetaItems(company: CompanyProfile): MetaItem[] {
  const candidates: Array<{ icon: typeof Phone; label: string; value: string | null | undefined }> = [
    { icon: Phone, label: "Phone", value: company.phone },
    { icon: MapPin, label: "Address", value: company.address },
    { icon: Calendar, label: "Founded", value: company.founded },
    { icon: MapPin, label: "Headquarters", value: company.headquarters },
    { icon: Users, label: "Employees", value: company.employeeCount },
  ];
  return candidates.filter((item): item is MetaItem => Boolean(item.value));
}

export interface CompanyCardProps {
  company: CompanyProfile;
  confidence?: number | null;
}

/** The resolved company overview — the anchor card at the top of every
 * completed research result. Meta chips (phone, address, founded, ...)
 * only render when the AI actually found that data — real crawled
 * content is often incomplete, unlike the old mock profiles. */
function CompanyCardImpl({ company, confidence }: CompanyCardProps) {
  const metaItems = buildMetaItems(company);
  const confidencePct = typeof confidence === "number" ? Math.round(confidence * 100) : null;

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
      <Card>
        <CardHeader className="flex-row items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <span className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <Building2 className="size-5" />
            </span>
            <div>
              <h3 className="text-lg font-semibold tracking-tight">{company.name}</h3>
              <p className="text-sm text-muted-foreground">{company.domain}</p>
            </div>
          </div>
          <div className="flex flex-wrap items-center justify-end gap-2">
            {company.industry && <Badge variant="secondary">{company.industry}</Badge>}
            {confidencePct !== null && (
              <Badge variant={confidencePct >= 60 ? "success" : "warning"} className="gap-1">
                <ShieldCheck className="size-3" />
                {confidencePct}% confidence
              </Badge>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-5">
          <p className="text-sm leading-relaxed text-muted-foreground">{company.summary}</p>

          {metaItems.length > 0 && (
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {metaItems.map(({ icon: Icon, label, value }) => (
                <div key={label} className="flex items-center gap-2 rounded-lg bg-secondary/60 px-3 py-2">
                  <Icon className="size-4 shrink-0 text-muted-foreground" />
                  <div className="min-w-0">
                    <p className="text-[11px] uppercase tracking-wide text-muted-foreground">{label}</p>
                    <p className="truncate text-sm font-medium">{value}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {company.painPoints.length > 0 && (
            <div>
              <div className="mb-2 flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                <AlertTriangle className="size-3.5" />
                Key Pain Points
              </div>
              <ul className="space-y-1.5">
                {company.painPoints.map((point) => (
                  <li key={point} className="flex gap-2 text-sm text-muted-foreground">
                    <span className="mt-1.5 size-1 shrink-0 rounded-full bg-muted-foreground" />
                    {point}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

export const CompanyCard = memo(CompanyCardImpl);
