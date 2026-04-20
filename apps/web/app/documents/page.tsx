import Link from "next/link";

import { PageShell, Panel, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export default async function DocumentsPage() {
  const documents = await api.documents().catch(() => []);
  return (
    <PageShell
      eyebrow="Documents"
      title="Source library"
      description="Every answer segment in CITADEL resolves back to concrete source chunks. This view exposes the underlying document inventory, owners, and domains."
    >
      <div className="grid gap-4 xl:grid-cols-2">
        {documents.map((document) => (
          <Link key={document.id} href={`/documents/${document.id}`} className="block">
            <Panel className="h-full space-y-4 transition hover:-translate-y-0.5 hover:border-cyan-300/30">
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="text-lg font-medium text-white">{document.title}</div>
                  <div className="text-sm text-slate-400">{document.id}</div>
                </div>
                <StatusPill status="grounded" />
              </div>
              <div className="grid gap-2 text-sm text-slate-300">
                <div>Owner: {document.owner_team ?? "Unassigned"}</div>
                <div>Domain: {document.domain ?? "Unknown"}</div>
                <div>Version: {document.version}</div>
                <div>Source type: {document.source_type}</div>
              </div>
            </Panel>
          </Link>
        ))}
      </div>
    </PageShell>
  );
}

