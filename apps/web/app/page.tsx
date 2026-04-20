import { DatabaseZap, FileCheck2, GanttChartSquare, ShieldCheck } from "lucide-react";

import { sampleQueries } from "@citadel/config";
import { MetricCard, PageShell, Panel, SectionHeading, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export default async function HomePage() {
  const [documents, providers, evals] = await Promise.all([
    api.documents().catch(() => []),
    api.providers().catch(() => []),
    api.evals().catch(() => []),
  ]);

  const healthyProviders = providers.filter((provider) => provider.status === "healthy").length;
  const latestEval = evals[0];

  return (
    <PageShell
      eyebrow="Overview"
      title="Grounded enterprise retrieval, tuned for operators instead of demos."
      description="CITADEL combines lexical search, dense similarity, graph-aware expansion, reranking, and strict citation assembly. It keeps evidence visible even when providers are degraded and surfaces eval posture as a first-class product concern."
    >
      <div className="grid gap-4 lg:grid-cols-4">
        <MetricCard
          label="Corpus"
          value={`${documents.length}`}
          detail="Seeded platform, security, onboarding, privacy, ADR, and policy documents."
          icon={<FileCheck2 className="size-4" />}
        />
        <MetricCard
          label="Providers"
          value={`${healthyProviders}/${providers.length || 7}`}
          detail="Dependency health is persisted and visible to operators."
          icon={<DatabaseZap className="size-4" />}
        />
        <MetricCard
          label="Latest Eval"
          value={latestEval?.status ?? "not run"}
          detail="Eval gates track retrieval recall, citation coverage, and unsupported claim rate."
          icon={<GanttChartSquare className="size-4" />}
        />
        <MetricCard
          label="Governance"
          value="strict"
          detail="Citations are required for grounded output; unsafe tool-like requests are policy-noted."
          icon={<ShieldCheck className="size-4" />}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.9fr]">
        <Panel className="space-y-6">
          <SectionHeading
            kicker="Query lifecycle"
            title="What happens on each ask"
            body="Normalize, retrieve across lexical and dense channels, expand through the document graph, rerank, then assemble evidence-bound answer segments."
          />
          <div className="grid gap-3 md:grid-cols-2">
            {[
              "Query normalization and bounded rewrite",
              "Hybrid retrieval with lexical and dense lanes",
              "Graph expansion through references, policies, and owners",
              "Cross-encoder reranking when available",
              "Citation assembly and unsupported-claim suppression",
              "Trace-first operator diagnostics",
            ].map((item) => (
              <div key={item} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 text-sm text-slate-300">
                {item}
              </div>
            ))}
          </div>
        </Panel>

        <Panel className="space-y-4">
          <SectionHeading
            kicker="Prompt set"
            title="Representative operator queries"
            body="The seeded corpus is coherent enough to make retrieval traces and graph expansion useful."
          />
          <div className="space-y-3">
            {sampleQueries.map((query) => (
              <div key={query} className="rounded-2xl border border-white/10 bg-slate-900/80 p-4 text-sm text-slate-200">
                {query}
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_1fr]">
        <Panel className="space-y-4">
          <SectionHeading
            kicker="Live system"
            title="Current operator posture"
            body="This surface is bound to the backend instead of mocked status cards."
          />
          <div className="grid gap-3 md:grid-cols-2">
            {providers.slice(0, 6).map((provider) => (
              <div key={provider.name} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3">
                <div>
                  <div className="font-medium text-white">{provider.name}</div>
                  <div className="text-sm text-slate-400">{provider.kind}</div>
                </div>
                <StatusPill status={provider.status} />
              </div>
            ))}
          </div>
        </Panel>

        <Panel className="space-y-4">
          <SectionHeading
            kicker="Collection design"
            title="Source coverage in the seeded corpus"
            body="The sample corpus mirrors platform engineering and governance material rather than filler text."
          />
          <div className="flex flex-wrap gap-2">
            {["Platform", "Security", "ADR", "Onboarding", "Policies", "Privacy"].map((domain) => (
              <span key={domain} className="rounded-full border border-cyan-200/20 bg-cyan-200/10 px-3 py-1 text-sm text-cyan-50">
                {domain}
              </span>
            ))}
          </div>
        </Panel>
      </div>
    </PageShell>
  );
}

