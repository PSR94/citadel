import { notFound } from "next/navigation";

import { PageShell, Panel, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export default async function DocumentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const document = await api.document(id).catch(() => null);
  if (!document) {
    notFound();
  }

  return (
    <PageShell
      eyebrow="Document"
      title={document.title}
      description="Document metadata, content chunks, and source path for citation inspection."
    >
      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Panel className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-slate-400">{document.id}</div>
              <div className="text-xl font-semibold text-white">Metadata</div>
            </div>
            <StatusPill status="grounded" />
          </div>
          <div className="grid gap-2 text-sm text-slate-300">
            <div>Owner team: {document.owner_team ?? "Unknown"}</div>
            <div>Domain: {document.domain ?? "Unknown"}</div>
            <div>Version: {document.version}</div>
            <div>Source: {document.source_path}</div>
            <div>Access scope: {document.access_scope}</div>
          </div>
        </Panel>
        <Panel className="space-y-4">
          <div className="text-xl font-semibold text-white">Chunks</div>
          <div className="space-y-3">
            {document.chunks.map((chunk) => (
              <div key={chunk.id} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="mb-2 text-xs uppercase tracking-[0.2em] text-slate-500">Chunk {chunk.ordinal}</div>
                <p className="text-sm leading-7 text-slate-200">{chunk.text}</p>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </PageShell>
  );
}

