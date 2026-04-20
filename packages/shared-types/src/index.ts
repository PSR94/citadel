import { z } from "zod";

export const citationSchema = z.object({
  chunk_id: z.string(),
  document_id: z.string(),
  document_title: z.string(),
  span: z.string(),
  score: z.number(),
});

export const answerSegmentSchema = z.object({
  text: z.string(),
  citations: z.array(citationSchema),
  supported: z.boolean(),
});

export const evidenceChunkSchema = z.object({
  chunk_id: z.string(),
  document_id: z.string(),
  document_title: z.string(),
  text: z.string(),
  scores: z.record(z.number()),
  source_path: z.string(),
  metadata: z.record(z.unknown()).default({}),
});

export const chatResponseSchema = z.object({
  run_id: z.string(),
  status: z.enum(["grounded", "insufficient_evidence", "provider_unavailable"]),
  answer: z.array(answerSegmentSchema),
  citations: z.array(citationSchema),
  evidence: z.array(evidenceChunkSchema),
  grounding: z.object({
    citation_coverage: z.number(),
    unsupported_claims: z.number(),
    insufficient_evidence: z.boolean(),
    rationale: z.array(z.string()),
  }),
  debug: z.object({
    normalized_query: z.string(),
    rewritten_queries: z.array(z.string()),
    graph_expansion: z.array(z.record(z.unknown())),
    stage_timings_ms: z.record(z.number()),
    policy_notes: z.array(z.string()),
  }),
  provider: z.record(z.unknown()),
});

export const documentSummarySchema = z.object({
  id: z.string(),
  title: z.string(),
  version: z.string(),
  owner_team: z.string().nullable(),
  domain: z.string().nullable(),
  source_type: z.string(),
  access_scope: z.string(),
  metadata: z.record(z.unknown()),
  updated_at: z.string(),
});

export const evalSummarySchema = z.object({
  id: z.string(),
  profile: z.string(),
  status: z.string(),
  metrics: z.record(z.number()),
  created_at: z.string(),
  completed_at: z.string().nullable(),
});

export type ChatResponse = z.infer<typeof chatResponseSchema>;
export type DocumentSummary = z.infer<typeof documentSummarySchema>;
export type EvalSummary = z.infer<typeof evalSummarySchema>;

