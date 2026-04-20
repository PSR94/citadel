# Threat Model Notes

## MAESTRO-informed concerns

- Model misuse: prompt-injection-style retrieval requests that attempt unsafe actions
- Asset exposure: source documents may contain sensitive policy or operational content
- Execution boundary: retrieval debugging must not become arbitrary tool execution
- Response integrity: unsupported claims must not appear as grounded truth
- Traceability: operator actions and ingestion runs need durable records
- Operational resilience: degraded dependencies should fail visible, not silent

## LINDDUN-informed privacy concerns

- Linkability: document access and query logs can reveal patterns about internal work
- Identifiability: future corpora may contain named personnel or customer identifiers
- Non-repudiation: audit records are useful, but retention and access boundaries must be controlled
- Detectability: status and provider pages should not leak secrets
- Disclosure of information: source-level access control hooks need enforcement in real deployments
- Unawareness: operators should know when evidence is insufficient or providers are unavailable
- Non-compliance: retention categories and exception flows need explicit governance owners

