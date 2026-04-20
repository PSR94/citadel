import { PageShell, Panel, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";
import { EvalsConsole } from "@/features/evals/evals-console";

export default async function EvalsPage() {
  const evals = await api.evals().catch(() => []);
  return (
    <PageShell
      eyebrow="Evals"
      title="Eval gates as product surface, not afterthought."
      description="CITADEL tracks retrieval recall, citation coverage, unsupported-claim rate, and failures by case. Thresholds can fail CI and are also visible to the operator UI."
    >
      <EvalsConsole evals={evals} />
      <Panel className="space-y-4">
        <div className="text-xl font-semibold text-white">Recent runs</div>
        <div className="space-y-3">
          {evals.length ? (
            evals.map((evalRun) => (
              <div key={evalRun.id} className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.03] p-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="font-medium text-white">{evalRun.id}</div>
                  <div className="text-sm text-slate-400">{evalRun.profile}</div>
                </div>
                <div className="grid gap-2 text-sm text-slate-300 sm:grid-flow-col sm:items-center sm:gap-6">
                  <div>recall@10 {evalRun.metrics.retrieval_recall_at_10?.toFixed?.(3) ?? "n/a"}</div>
                  <div>unsupported {evalRun.metrics.unsupported_claim_rate?.toFixed?.(3) ?? "n/a"}</div>
                  <StatusPill status={evalRun.status} />
                </div>
              </div>
            ))
          ) : (
            <div className="text-sm text-slate-500">No eval runs have been recorded yet.</div>
          )}
        </div>
      </Panel>
    </PageShell>
  );
}

