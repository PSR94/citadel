---
doc_id: DOC-ADR-001
title: ADR-001 Legacy Auth Proxy
version: "1.0"
owner_team: Identity Platform
domain: adr
systems:
  - Legacy Auth Proxy
references: []
superseded_by:
  - DOC-ADR-006
---

# ADR-001 Legacy Auth Proxy

The original platform used a shared auth proxy in front of service backends. It simplified SSO integration but introduced central latency and brittle routing rules.

## Status

Superseded by ADR-006 Identity Gateway.

