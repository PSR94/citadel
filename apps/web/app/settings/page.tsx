import { PageShell, Panel } from "@citadel/ui";
import { api } from "@/lib/api";

export default async function SettingsPage() {
  const [config, providers] = await Promise.all([api.config().catch(() => null), api.providers().catch(() => [])]);
  return (
    <PageShell
      eyebrow="Settings"
      title="Public configuration and provider visibility."
      description="This page shows the current retrieval and generation posture exposed by the backend without leaking secrets or internal-only credentials."
    >
      <div className="grid gap-6 xl:grid-cols-2">
        <Panel className="space-y-4">
          <div className="text-xl font-semibold text-white">Public config</div>
          {config ? (
            <pre className="overflow-x-auto rounded-2xl border border-white/10 bg-slate-950/80 p-4 text-xs text-slate-300">
              {JSON.stringify(config, null, 2)}
            </pre>
          ) : (
            <div className="text-sm text-slate-500">Config endpoint unavailable.</div>
          )}
        </Panel>
        <Panel className="space-y-4">
          <div className="text-xl font-semibold text-white">Provider inventory</div>
          <div className="space-y-3">
            {providers.map((provider) => (
              <div key={provider.name} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 text-sm text-slate-200">
                <div className="flex items-center justify-between">
                  <span>{provider.name}</span>
                  <span className="text-slate-400">{provider.status}</span>
                </div>
                <div className="mt-2 text-xs text-slate-500">{provider.kind}</div>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </PageShell>
  );
}

