import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

import { EmptyState } from "@/components/common/EmptyState";
import { Message } from "@/components/common/Message";
import { PromptInput } from "@/components/common/PromptInput";
import { StatusIndicator } from "@/components/common/StatusIndicator";
import { Timeline } from "@/components/common/Timeline";
import { TypingIndicator } from "@/components/common/TypingIndicator";
import { PdfDownloadButton } from "@/components/report/PdfDownloadButton";
import { ResearchSummary } from "@/components/report/ResearchSummary";
import { Card, CardContent } from "@/components/ui/card";
import { useAutoScroll } from "@/hooks/useAutoScroll";
import { useConversationStore } from "@/hooks/useConversationStore";

export default function ResearchPage() {
  const messages = useConversationStore((state) => state.messages);
  const steps = useConversationStore((state) => state.steps);
  const sessionStatus = useConversationStore((state) => state.sessionStatus);
  const result = useConversationStore((state) => state.result);
  const isTyping = useConversationStore((state) => state.isTyping);
  const error = useConversationStore((state) => state.error);

  // Scrolls a bottom sentinel into view (not the container itself) — see
  // useAutoScroll's docstring for why. Fires on every event a ChatGPT/
  // Perplexity-style conversation should auto-scroll for: new message,
  // typing state, research starting/finishing, results appearing.
  const bottomAnchorRef = useAutoScroll<HTMLDivElement>([
    messages.length,
    isTyping,
    sessionStatus,
    result,
  ]);

  const title = messages.find((message) => message.role === "user")?.content ?? "New Research";
  const hasStarted = sessionStatus !== "idle";

  return (
    // min-h-0 lets this column shrink below its content's natural height
    // so the conversation area (not the whole page) is what scrolls.
    <div className="flex h-full min-h-0 flex-col">
      <header className="flex shrink-0 items-center justify-between gap-3 border-b border-border px-4 py-3 sm:px-6">
        <div className="min-w-0">
          <h1 className="truncate text-sm font-semibold">{title}</h1>
          <div className="mt-0.5">
            <StatusIndicator status={sessionStatus} />
          </div>
        </div>
        <PdfDownloadButton enabled={sessionStatus === "complete" && Boolean(result)} />
      </header>

      {/* The ONLY scrollable region on this page. overscroll-contain stops
          a scroll-to-edge here from bubbling up and rubber-banding the
          whole page (a common source of "the page scrolls weirdly" bugs
          on trackpads/mobile). pb-[120px] keeps the last card clear of
          the floating input bar below. */}
      <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain scroll-smooth scrollbar-thin">
        <div className="mx-auto w-full max-w-[1100px] space-y-6 px-4 py-6 pb-[120px] sm:px-6 lg:px-10">
          {!hasStarted && messages.length === 0 ? (
            <div className="flex h-[60vh] items-center justify-center">
              <EmptyState />
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}

              <AnimatePresence>{isTyping && <TypingIndicator key="typing" />}</AnimatePresence>

              {hasStarted && (
                <div className="flex justify-start">
                  <Timeline steps={steps} />
                </div>
              )}

              {sessionStatus === "error" && error && (
                <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
                  <Card className="border-destructive/30 bg-destructive/5">
                    <CardContent className="flex items-start gap-3 p-4">
                      <AlertTriangle className="mt-0.5 size-4 shrink-0 text-destructive" />
                      <div>
                        <p className="text-sm font-medium text-destructive">Research couldn't be completed</p>
                        <p className="mt-0.5 text-sm text-muted-foreground">{error}</p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}

              {sessionStatus === "complete" && result && <ResearchSummary result={result} />}
            </>
          )}

          {/* Auto-scroll target — kept as the very last node in the
              scrollable content so scrollIntoView lands exactly at the
              bottom regardless of what just changed above it. */}
          <div ref={bottomAnchorRef} aria-hidden="true" />
        </div>
      </div>

      {/* Sticky + backdrop-blur so the composer always stays visible and
          readable over whatever scrolls beneath it, ChatGPT/Perplexity-style. */}
      <div className="sticky bottom-0 shrink-0 border-t border-border bg-background/80 p-4 backdrop-blur-md sm:p-6">
        <div className="mx-auto w-full max-w-[1100px]">
          <PromptInput />
        </div>
      </div>
    </div>
  );
}
