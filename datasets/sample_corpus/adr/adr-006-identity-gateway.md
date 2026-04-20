---
doc_id: DOC-ADR-006
title: ADR-006 Identity Gateway
version: "1.3"
owner_team: Identity Platform
domain: adr
systems:
  - Identity Gateway
  - Citadel Gateway
references:
  - DOC-ADR-001
  - DOC-SEC-001
supersedes:
  - DOC-ADR-001
---

# ADR-006 Identity Gateway

ADR-006 replaced the legacy auth proxy with the Identity Gateway. The new path centralizes policy enforcement while keeping token validation close to the edge ingress tier.

## Decision

The Identity Platform team adopted a gateway model with signed downstream identity context, service ownership boundaries, and audited privileged admin APIs.

## Consequences

- deployment rollback checks must validate Identity Gateway health
- privileged admin routes are treated as high-risk systems under the Privileged Production Access Policy
- new services integrate through gateway-issued workload identity instead of sidecar auth proxy hops

