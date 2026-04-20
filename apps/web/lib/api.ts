import {
  chatResponseSchema,
  documentSummarySchema,
  evalSummarySchema,
} from "@citadel/shared-types";
import { z } from "zod";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export const dependencySchema = z.object({
  name: z.string(),
  kind: z.string(),
  status: z.string(),
  latency_ms: z.number().nullable(),
  details: z.record(z.unknown()),
  checked_at: z.string().or(z.date()),
});

export const documentDetailSchema = z.object({
  id: z.string(),
  title: z.string(),
  version: z.string(),
  owner_team: z.string().nullable(),
  domain: z.string().nullable(),
  source_type: z.string(),
  access_scope: z.string(),
  metadata: z.record(z.unknown()),
  updated_at: z.string(),
  source_path: z.string(),
  chunks: z.array(
    z.object({
      id: z.string(),
      document_id: z.string(),
      ordinal: z.number(),
      text: z.string(),
      token_count: z.number(),
      metadata: z.record(z.unknown()),
    }),
  ),
});

export const publicConfigSchema = z.object({
  app_name: z.string(),
  domain: z.string(),
  retrieval: z.record(z.unknown()),
  generation: z.record(z.unknown()),
  governance: z.record(z.unknown()),
});

export const healthSchema = z.object({
  status: z.string(),
  service: z.string().optional(),
  environment: z.string().optional(),
  checked_at: z.string().or(z.date()),
});

export const readinessSchema = z.object({
  status: z.string(),
  documents: z.number(),
  local_index_ready: z.boolean(),
  checked_at: z.string().or(z.date()),
});

export const evalDetailSchema = evalSummarySchema.extend({
  details: z.record(z.unknown()),
});

async function request<T>(path: string, schema: z.ZodSchema<T>, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!response.ok) {
    throw new Error(`${path} failed: ${response.status}`);
  }
  return schema.parse(await response.json());
}

export const api = {
  health: () => request("/health", healthSchema),
  readiness: () => request("/health/readiness", readinessSchema),
  dependencies: () => request("/health/dependencies", z.array(dependencySchema)),
  documents: () => request("/api/v1/documents", z.array(documentSummarySchema)),
  document: (id: string) => request(`/api/v1/documents/${id}`, documentDetailSchema),
  providers: () => request("/api/v1/providers", z.array(dependencySchema)),
  config: () => request("/api/v1/config/public", publicConfigSchema),
  evals: () => request("/api/v1/evals", z.array(evalSummarySchema)),
  eval: (id: string) => request(`/api/v1/evals/${id}`, evalDetailSchema),
  ask: (query: string) =>
    request("/api/v1/chat/query/debug", chatResponseSchema, {
      method: "POST",
      body: JSON.stringify({ query, debug: true }),
    }),
  runEval: () =>
    request("/api/v1/evals/run", evalDetailSchema, {
      method: "POST",
      body: JSON.stringify({ profile: "ci" }),
    }),
  upload: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${apiBase}/api/v1/ingest/upload`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`/api/v1/ingest/upload failed: ${response.status}`);
    }
    return z
      .object({
        id: z.string(),
        trigger: z.string(),
        status: z.string(),
        processed_documents: z.number(),
        processed_chunks: z.number(),
        error_count: z.number(),
        summary: z.record(z.unknown()),
        created_at: z.string(),
        completed_at: z.string().nullable(),
      })
      .parse(await response.json());
  },
  reindex: () =>
    request(
      "/api/v1/ingest/reindex",
      z.object({
        id: z.string(),
        trigger: z.string(),
        status: z.string(),
        processed_documents: z.number(),
        processed_chunks: z.number(),
        error_count: z.number(),
        summary: z.record(z.unknown()),
        created_at: z.string(),
        completed_at: z.string().nullable(),
      }),
      { method: "POST" },
    ),
};
