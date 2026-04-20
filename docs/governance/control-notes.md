# Governance Control Notes

CITADEL is not claiming certification or compliance. The repository is structured so a deployment team can map controls to a real environment.

## Control posture

- RBAC-ready actor model and route dependency seams
- audit event persistence for ingestion and query activity
- provider health visibility without secret exposure
- source-level access scope field on documents for future enforcement
- explicit insufficient-evidence mode to suppress unsupported output
- policy service for bounded unsafe request handling notes

## Framework alignment

- NIST AI RMF: govern, map, measure, manage through evals, audit, and operator visibility
- ISO 42001 awareness: documented policies, evaluation flows, and runtime monitoring seams
- EU AI Act awareness: transparency, provenance, and risk controls matter more than model novelty
- SOC 2 mindset: traceability, least privilege hooks, and change visibility
- GDPR and HIPAA extensibility mindset: privacy-aware storage boundaries and role-based future enforcement

