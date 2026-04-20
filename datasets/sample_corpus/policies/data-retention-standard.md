---
doc_id: DOC-POL-001
title: Data Retention Standard
version: "6.0"
owner_team: Governance Engineering
domain: policies
systems:
  - Incident Hub
  - Audit Vault
policies:
  - POL-PRIV-001
references:
  - DOC-PRIV-002
  - DOC-SEC-001
  - DOC-PLAT-001
---

# Data Retention Standard

This standard defines minimum retention periods, exception handling, and deletion obligations for operational and regulated records.

## Default retention classes

- incident records: seven years
- privileged access approvals and session recordings: seven years
- onboarding approvals: three years after separation or contract end
- routine operational telemetry: ninety days unless mapped to an approved exception

## Exception process

Exceptions to the standard must be documented in the retention exception register, approved by Governance Engineering and Privacy Engineering, and include an expiry date.

## Related documents

Retention exceptions are described in the [Retention Exception Handling Guide](../privacy/data-retention-exceptions.md).

