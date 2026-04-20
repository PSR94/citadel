import { PageShell, Panel, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export default async function StatusPage() {
  const [health, readiness, dependencies] = await Promise.all([
    api.health().catch(() => null),
    api.readiness().catch(() => null),
    api.dependencies().catch(() => []),
  ]);

  return (
    <PageShell
      eyebrow="Status"
      title="Dependency health, readiness, and operator confidence."
      description="The status surface is bound to backend health checks for storage, graph, reranker, cache, and generation posture."
    >
      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <Panel className="space-y-4">
          <div className="text-xl font-semibold text-white">Service readiness</div>
          <div className="space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between">
              <span>App health</span>
              <StatusPill status={health?.status ?? "degraded"} />
            </div>
            <div className="flex items-center justify-between">
              <span>Readiness</span>
              <StatusPill status={readiness?.status ?? "degraded"} />
            </div>
            <div className="flex items-center justify-between">
              <span>Indexed documents</span>
              <span>{readiness?.documents ?? 0}</span>
            </div>
          </div>
        </Panel>
        <Panel className="space-y-4">
          <div className="text-xl font-semibold text-white">Dependency health</div>
          <div className="grid gap-3 md:grid-cols-2">
            {dependencies.map((dependency) => (
              <div key={dependency.name} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div className="mb-3 flex items-center justify-between">
                  <div>
                    <div className="font-medium text-white">{dependency.name}</div>
                    <div className="text-sm text-slate-400">{dependency.kind}</div>
                  </div>
                  <StatusPill status={dependency.status} />
                </div>
                <div className="text-xs text-slate-500">
                  {dependency.latency_ms ? `${dependency.latency_ms.toFixed(1)} ms` : "Latency unavailable"}
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </PageShell>
  );
}

