import { ArrowUp } from "lucide-react";
import { useForm } from "react-hook-form";

import { ModelSelector } from "@/components/common/ModelSelector";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useConversationStore } from "@/hooks/useConversationStore";

interface PromptFormValues {
  query: string;
}

/** The bottom composer: model selector + auto-submitting textarea + send
 * button. Enter sends, Shift+Enter inserts a newline. Disabled entirely
 * while a research run is in progress. */
export function PromptInput() {
  const startResearch = useConversationStore((state) => state.startResearch);
  const isRunning = useConversationStore((state) => state.sessionStatus === "running");

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PromptFormValues>({ defaultValues: { query: "" } });

  const onSubmit = handleSubmit(({ query }) => {
    if (isRunning) return;
    startResearch(query);
    reset();
  });

  const { ref: registerRef, ...queryField } = register("query", {
    required: true,
    maxLength: { value: 200, message: "Keep it under 200 characters." },
  });

  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-2">
      <div className="flex items-end gap-2 rounded-2xl border border-input bg-card p-2 shadow-soft focus-within:ring-2 focus-within:ring-ring">
        <Textarea
          {...queryField}
          ref={registerRef}
          rows={1}
          disabled={isRunning}
          placeholder="Enter a company name or website (e.g. Stripe, tesla.com)..."
          aria-label="Company name or website"
          className="max-h-32 min-h-10 flex-1 border-0 bg-transparent p-2 shadow-none focus-visible:ring-0
            focus-visible:ring-offset-0"
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSubmit();
            }
          }}
        />
        <Button type="submit" size="icon" disabled={isRunning} aria-label="Send research request">
          <ArrowUp className="size-4" />
        </Button>
      </div>
      <div className="flex items-center justify-between px-1">
        <ModelSelector compact />
        {errors.query && <p className="text-xs text-destructive">{errors.query.message ?? "Required"}</p>}
      </div>
    </form>
  );
}
