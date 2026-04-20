"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { Panel, SectionHeading, StatusPill } from "@citadel/ui";
import { api } from "@/lib/api";

export function IngestionConsole() {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({
    mutationFn: api.reindex,
  });
  const uploadMutation = useMutation({
    mutationFn: api.upload,
  });
  const latestRun = uploadMutation.data ?? mutation.data;

  return (
    <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
      <Panel className="space-y-5">
        <SectionHeading
          kicker="Ingestion"
          title="Rebuild indexes from the corpus"
          body="The ingestion path parses markdown, text, JSON, and PDF-capable inputs, rebuilds chunks, refreshes the local retrieval index, and syncs graph payloads."
        />
        <div className="space-y-4">
          <button
            type="button"
            onClick={() => mutation.mutate()}
            className="rounded-full bg-cyan-300 px-5 py-3 text-sm font-medium text-slate-950 transition hover:bg-cyan-200"
          >
            Reindex corpus
          </button>
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-4">
            <label className="mb-3 block text-sm text-slate-300">Upload a document for ingestion</label>
            <input
              type="file"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              className="w-full rounded-2xl border border-white/10 bg-slate-950/80 p-3 text-sm text-slate-300"
            />
            <button
              type="button"
              disabled={!file || uploadMutation.isPending}
              onClick={() => file && uploadMutation.mutate(file)}
              className="mt-4 rounded-full border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Upload and ingest
            </button>
          </div>
        </div>
      </Panel>
      <Panel className="space-y-4">
        <SectionHeading
          kicker="Recent run"
          title="Latest ingestion result"
          body="Runs are generated from the real ingest endpoint and reflect actual parsing and index refresh work."
        />
        {latestRun ? (
          <div className="space-y-3 text-sm text-slate-200">
            <div className="flex items-center justify-between">
              <span>Run ID</span>
              <span>{latestRun.id}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Status</span>
              <StatusPill status={latestRun.status} />
            </div>
            <div className="flex items-center justify-between">
              <span>Documents</span>
              <span>{latestRun.processed_documents}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Chunks</span>
              <span>{latestRun.processed_chunks}</span>
            </div>
            {"uploaded_file" in latestRun.summary ? (
              <div className="flex items-center justify-between">
                <span>Uploaded file</span>
                <span>{String(latestRun.summary.uploaded_file)}</span>
              </div>
            ) : null}
          </div>
        ) : (
          <div className="text-sm text-slate-500">No ingestion run started from this session yet.</div>
        )}
      </Panel>
    </div>
  );
}

