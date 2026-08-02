import { Check, ChevronDown, Cpu } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useSettingsStore } from "@/hooks/useSettingsStore";
import { MOCK_MODELS } from "@/utils/mockData/models";

const BADGE_VARIANT = {
  fast: "success",
  balanced: "default",
  powerful: "warning",
} as const;

export interface ModelSelectorProps {
  compact?: boolean;
}

/** Reused on both the Research prompt bar and the Settings page — a
 * single source of truth for "which mock model is selected." */
export function ModelSelector({ compact = false }: ModelSelectorProps) {
  const selectedModelId = useSettingsStore((state) => state.selectedModelId);
  const setSelectedModelId = useSettingsStore((state) => state.setSelectedModelId);
  const selected = MOCK_MODELS.find((model) => model.id === selectedModelId) ?? MOCK_MODELS[0];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size={compact ? "sm" : "default"} className="gap-2">
          <Cpu className="size-4 text-muted-foreground" />
          <span className={compact ? "max-w-[7rem] truncate" : ""}>{selected.name}</span>
          <ChevronDown className="size-3.5 text-muted-foreground" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="w-72">
        <DropdownMenuLabel>Model</DropdownMenuLabel>
        {MOCK_MODELS.map((model) => (
          <DropdownMenuItem key={model.id} onSelect={() => setSelectedModelId(model.id)}>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{model.name}</span>
                {model.badge && (
                  <Badge variant={BADGE_VARIANT[model.badge]} className="capitalize">
                    {model.badge}
                  </Badge>
                )}
              </div>
              <p className="text-xs text-muted-foreground">{model.description}</p>
            </div>
            {model.id === selectedModelId && <Check className="size-4 shrink-0 text-primary" />}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
