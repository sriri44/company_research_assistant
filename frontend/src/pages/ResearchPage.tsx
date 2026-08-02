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

  const scrollRef = useAutoScroll<HTMLDivElement>([messages.length, isTyping, sessionStatus]);
  const title = messages.find((message) => message.role === "user")?.content ?? "New Research";
  const hasStarted = sessionStatus !== "idle";

  return (
    <div className="flex h-full flex-col">
      <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-3 sm:px-6">
        <div className="min-w-0">
          <h1 className="truncate text-sm font-semibold">{title}</h1>
          <div className="mt-0.5">
            <StatusIndicator status={sessionStatus} />
          </div>
        </div>
        <PdfDownloadButton enabled={sessionStatus === "complete" && Boolean(result)} />
      </header>

      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin">
        <div className="mx-auto w-full max-w-3xl space-y-6 px-4 py-6 sm:px-6">
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
        </div>
      </div>

      <div className="border-t border-border p-4 sm:p-6">
        <div className="mx-auto w-full max-w-3xl">
          <PromptInput />
        </div>
      </div>
    </div>
  );
}
