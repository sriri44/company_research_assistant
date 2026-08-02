import { Info, MessageSquare, Plus, Settings } from "lucide-react";
import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import { AboutPanel } from "@/components/common/AboutPanel";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { useConversationStore } from "@/hooks/useConversationStore";
import { cn } from "@/utils/cn";

export interface SidebarProps {
  onNavigate?: () => void;
}

/** The Research/Settings shell sidebar. "Recent Session" is intentionally
 * singular and non-persisted — it reflects only the in-memory
 * conversation for this visit, per the "temporary only" spec. */
export function Sidebar({ onNavigate }: SidebarProps) {
  const [aboutOpen, setAboutOpen] = useState(false);
  const navigate = useNavigate();
  const messages = useConversationStore((state) => state.messages);
  const sessionStatus = useConversationStore((state) => state.sessionStatus);
  const resetConversation = useConversationStore((state) => state.reset);

  const sessionLabel = messages.find((message) => message.role === "user")?.content ?? null;

  const handleNewResearch = () => {
    resetConversation();
    navigate("/research");
    onNavigate?.();
  };

  return (
    <div className="flex h-full w-full flex-col gap-6 bg-secondary/40 p-4">
      <div className="px-1">
        <Logo />
      </div>

      <Button className="w-full justify-start gap-2" onClick={handleNewResearch}>
        <Plus className="size-4" />
        New Research
      </Button>

      <div className="flex-1 overflow-y-auto scrollbar-thin">
        <p className="px-2 pb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Recent Session
        </p>
        {sessionLabel ? (
          <NavLink
            to="/research"
            onClick={onNavigate}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm transition-colors",
                isActive ? "bg-secondary text-foreground" : "text-muted-foreground hover:bg-secondary/70",
              )
            }
          >
            <MessageSquare className="size-4 shrink-0" />
            <span className="truncate">{sessionLabel}</span>
            {sessionStatus === "running" && (
              <span className="ml-auto size-1.5 shrink-0 animate-pulse rounded-full bg-primary" />
            )}
          </NavLink>
        ) : (
          <p className="px-2.5 text-sm text-muted-foreground">No active session yet.</p>
        )}
      </div>

      <div className="flex flex-col gap-1 border-t border-border pt-3">
        <NavLink
          to="/settings"
          onClick={onNavigate}
          className={({ isActive }) =>
            cn(
              "flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm font-medium transition-colors",
              isActive ? "bg-secondary text-foreground" : "text-muted-foreground hover:bg-secondary/70",
            )
          }
        >
          <Settings className="size-4" />
          Settings
        </NavLink>
        <button
          onClick={() => setAboutOpen(true)}
          className="flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm font-medium text-muted-foreground
            transition-colors hover:bg-secondary/70"
        >
          <Info className="size-4" />
          About
        </button>
      </div>

      <AboutPanel open={aboutOpen} onClose={() => setAboutOpen(false)} />
    </div>
  );
}
