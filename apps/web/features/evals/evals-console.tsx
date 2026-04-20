"use client";

import { useMutation } from "@tanstack/react-query";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";

import { Panel, SectionHeading, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";
import type { EvalSummary } from "@citadel/shared-types";

export function EvalsConsole({ evals }: { evals: EvalSummary[] }) {
  const mutation = useMutation({
    mutationFn: api.runEval,
  });
  const combined = mutation.data ? [mutation.data, ...evals] : evals;
  const chartData = combined.slice(0, 6).reverse().map((evalRun, index) => ({
    index: index + 1,
    recall: evalRun.metrics.retrieval_recall_at_10 ?? 0,
    unsupported: evalRun.metrics.unsupported_claim_rate ?? 0,
  }));

  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
      <Panel className="space-y-5">
        <SectionHeading
          kicker="CI gate"
          title="Run the evaluation harness"
          body="Eval runs score retrieval recall, citation coverage, unsupported-claim rate, and smoke health. The UI renders recent persisted runs plus any new run triggered from this session."
        />
        <button
          type="button"
          onClick={() => mutation.mutate()}
          className="rounded-full bg-cyan-300 px-5 py-3 text-sm font-medium text-slate-950 transition hover:bg-cyan-200"
        >
          Run CI profile eval
        </button>
        {mutation.data ? (
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <div className="mb-3 flex items-center justify-between">
              <div className="text-white">Latest run</div>
              <StatusPill status={mutation.data.status} />
            </div>
            <div className="grid gap-2 text-sm text-slate-300">
              {Object.entries(mutation.data.metrics).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between">
                  <span>{key}</span>
                  <span>{typeof value === "number" ? value.toFixed(3) : String(value)}</span>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </Panel>

      <Panel className="space-y-5">
        <SectionHeading
          kicker="Trend"
          title="Recent evaluation history"
          body="Trend lines stay grounded in persisted eval run data; no synthetic metrics are generated client-side."
        />
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="recall" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="#7AE7FF" stopOpacity={0.7} />
                  <stop offset="100%" stopColor="#7AE7FF" stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <XAxis dataKey="index" stroke="#8AA0B8" tickLine={false} axisLine={false} />
              <Tooltip />
              <Area type="monotone" dataKey="recall" stroke="#7AE7FF" fill="url(#recall)" />
              <Area type="monotone" dataKey="unsupported" stroke="#FF6E8A" fillOpacity={0} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Panel>
    </div>
  );
}

