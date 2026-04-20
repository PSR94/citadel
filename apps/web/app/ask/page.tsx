import { PageShell } from "@citadel/ui";
import { AskWorkbench } from "@/features/ask/ask-workbench";

export default function AskPage() {
  return (
    <PageShell
      eyebrow="Ask"
      title="Query the corpus with retrieval traces left on."
      description="CITADEL exposes grounded answer segments, chunk citations, graph expansion notes, and per-stage timings instead of hiding the retrieval chain behind a single response bubble."
    >
      <AskWorkbench />
    </PageShell>
  );
}

