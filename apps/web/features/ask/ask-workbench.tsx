"use client";

import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { LoaderCircle, Search } from "lucide-react";
import { useState } from "react";

import { sampleQueries } from "@citadel/config";
import { Panel, SectionHeading, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export function AskWorkbench() {
  const [query, setQuery] = useState(sampleQueries[0]);
  const mutation = useMutation({
    mutationFn: api.ask,
  });

  return (
    <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
      <Panel className="space-y-5">
        <SectionHeading
          kicker="Ask"
          title="Evidence-first retrieval"
          body="Ask directly against the seeded enterprise corpus. The UI exposes answer segments, citations, timing, and graph-expansion notes from the same run."
        />
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault();
            mutation.mutate(query);
          }}
        >
          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="min-h-40 w-full rounded-3xl border border-white/10 bg-slate-900/80 p-4 text-base text-white outline-none ring-0 transition placeholder:text-slate-500 focus:border-cyan-300/40"
            placeholder="Ask about policies, owners, incident response, or architecture decisions."
          />
          <div className="flex flex-wrap gap-2">
            {sampleQueries.map((sample) => (
              <button
                key={sample}
                type="button"
                onClick={() => setQuery(sample)}
                className="rounded-full border border-white/10 px-3 py-2 text-xs text-slate-300 transition hover:bg-white/5 hover:text-white"
              >
                {sample}
              </button>
            ))}
          </div>
          <button
            type="submit"
            className="inline-flex items-center gap-2 rounded-full bg-cyan-300 px-5 py-3 text-sm font-medium text-slate-950 transition hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={mutation.isPending}
          >
            {mutation.isPending ? <LoaderCircle className="size-4 animate-spin" /> : <Search className="size-4" />}
            Run grounded query
          </button>
        </form>
      </Panel>

      <div className="space-y-6">
        {!mutation.data && !mutation.isPending ? (
          <Panel className="space-y-3">
            <SectionHeading
              kicker="Trace"
              title="No run yet"
              body="Run a query to inspect answer segments, citations, evidence chunks, graph notes, and stage timings."
            />
          </Panel>
        ) : null}

        {mutation.error ? (
          <Panel className="border-rose-400/25 bg-rose-400/10 text-rose-50">
            <div className="text-sm">Query failed. Check API availability and dependency status.</div>
          </Panel>
        ) : null}

        {mutation.data ? (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="space-y-6"
          >
            <Panel className="space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-xs uppercase tracking-[0.24em] text-slate-500">Grounded Answer</div>
                  <div className="mt-1 text-2xl font-semibold tracking-tight text-white">Run {mutation.data.run_id}</div>
                </div>
                <StatusPill status={mutation.data.status} />
              </div>
              <div className="space-y-4">
                {mutation.data.answer.map((segment, index) => (
                  <div key={`${segment.text}-${index}`} className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                    <p className="text-sm leading-7 text-slate-100">{segment.text}</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {segment.citations.map((citation) => (
                        <span
                          key={citation.chunk_id}
                          className="rounded-full border border-cyan-200/20 bg-cyan-200/10 px-3 py-1 text-xs text-cyan-50"
                        >
                          {citation.document_id}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </Panel>

            <div className="grid gap-6 xl:grid-cols-2">
              <Panel className="space-y-4">
                <SectionHeading
                  kicker="Evidence"
                  title="Supporting chunks"
                  body="Retrieved evidence remains visible even if generation becomes unavailable."
                />
                <div className="space-y-3">
                  {mutation.data.evidence.map((chunk) => (
                    <div key={chunk.chunk_id} className="rounded-2xl border border-white/10 bg-slate-900/80 p-4">
                      <div className="mb-2 flex items-center justify-between">
                        <div>
                          <div className="font-medium text-white">{chunk.document_title}</div>
                          <div className="text-xs uppercase tracking-[0.2em] text-slate-500">{chunk.document_id}</div>
                        </div>
                        <div className="text-xs text-slate-400">fusion {chunk.scores.fusion?.toFixed?.(2) ?? chunk.scores.fusion}</div>
                      </div>
                      <p className="text-sm leading-6 text-slate-300">{chunk.text}</p>
                    </div>
                  ))}
                </div>
              </Panel>

              <Panel className="space-y-4">
                <SectionHeading
                  kicker="Trace"
                  title="Retrieval diagnostics"
                  body="Operator-facing visibility into graph expansion, stage timings, and policy notes."
                />
                <div className="space-y-3">
                  <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                    <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Stage timings</div>
                    <div className="mt-3 grid gap-2">
                      {Object.entries(mutation.data.debug.stage_timings_ms).map(([stage, value]) => (
                        <div key={stage} className="flex items-center justify-between text-sm text-slate-300">
                          <span>{stage}</span>
                          <span>{value.toFixed(2)} ms</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                    <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Graph expansion</div>
                    <div className="mt-3 space-y-2 text-sm text-slate-300">
                      {mutation.data.debug.graph_expansion.length ? (
                        mutation.data.debug.graph_expansion.map((item, index) => (
                          <div key={index} className="rounded-2xl border border-white/10 bg-slate-950/80 p-3">
                            {String(item.source_node)} → {String(item.related_document_id)} ({String(item.relation)})
                          </div>
                        ))
                      ) : (
                        <div className="text-slate-500">No graph expansion applied for this run.</div>
                      )}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                    <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Policy notes</div>
                    <div className="mt-3 space-y-2 text-sm text-slate-300">
                      {mutation.data.debug.policy_notes.map((note) => (
                        <div key={note}>{note}</div>
                      ))}
                    </div>
                  </div>
                </div>
              </Panel>
            </div>
          </motion.div>
        ) : null}
      </div>
    </div>
  );
}

