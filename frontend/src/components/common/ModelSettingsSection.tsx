import { Check } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useSettingsStore } from "@/hooks/useSettingsStore";
import { MOCK_MODELS } from "@/utils/mockData/models";
import { cn } from "@/utils/cn";

const BADGE_VARIANT = { fast: "success", balanced: "default", powerful: "warning" } as const;

export function ModelSettingsSection() {
  const selectedModelId = useSettingsStore((state) => state.selectedModelId);
  const setSelectedModelId = useSettingsStore((state) => state.setSelectedModelId);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Default Model</CardTitle>
        <CardDescription>Used for new research sessions. Applied instantly.</CardDescription>
      </CardHeader>
      <CardContent>
        <div role="radiogroup" aria-label="Default model" className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {MOCK_MODELS.map((model) => {
            const isActive = model.id === selectedModelId;
            return (
              <button
                key={model.id}
                role="radio"
                aria-checked={isActive}
                onClick={() => setSelectedModelId(model.id)}
                className={cn(
                  "flex items-start gap-3 rounded-xl border p-4 text-left transition-colors",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                  "focus-visible:ring-offset-background",
                  isActive
                    ? "border-primary bg-accent"
                    : "border-border bg-background hover:bg-secondary/60",
                )}
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold">{model.name}</span>
                    {model.badge && (
                      <Badge variant={BADGE_VARIANT[model.badge]} className="capitalize">
                        {model.badge}
                      </Badge>
                    )}
                  </div>
                  <p className="mt-0.5 text-xs text-muted-foreground">{model.provider}</p>
                  <p className="mt-1.5 text-xs text-muted-foreground">{model.description}</p>
                </div>
                {isActive && <Check className="size-4 shrink-0 text-primary" />}
              </button>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
