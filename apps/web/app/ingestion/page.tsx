import { PageShell } from "@citadel/ui";
import { IngestionConsole } from "@/features/ingestion/ingestion-console";

export default function IngestionPage() {
  return (
    <PageShell
      eyebrow="Ingestion"
      title="Seed, upload, and reindex without leaving the product shell."
      description="Ingestion runs capture parsing, chunk production, and graph synchronization. The current baseline supports markdown, text, JSON, and PDF-capable parsing on the backend."
    >
      <IngestionConsole />
    </PageShell>
  );
}

