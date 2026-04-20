---
doc_id: DOC-PLAT-002
title: Deployment Rollback Runbook
version: "2.4"
owner_team: Deployment Platform
domain: platform
systems:
  - Citadel Gateway
  - Rollout Controller
  - Service Catalog
policies:
  - POL-SEC-002
references:
  - DOC-PLAT-001
  - DOC-ADR-006
---

# Deployment Rollback Runbook

The Deployment Platform team owns the rollback runbook, automation hooks, and approval trail for production reversion events.

## Preconditions

- confirm the last green deployment artifact in the release registry
- verify the target service owner has approved the rollback if data shape changes are involved
- freeze non-essential deploys in the shared environment

## Standard rollback

1. Use Rollout Controller to pin traffic to the previous stable release.
2. Validate health checks, saturation, and error budgets for ten minutes.
3. If the service depends on the Identity Gateway, confirm authentication traffic remains healthy because the legacy auth proxy was retired in [ADR-006](../adr/adr-006-identity-gateway.md).
4. Re-enable queued deploys only after the incident commander clears the freeze.

## Ownership

The Deployment Platform team executes the rollback. The product or service team that owns the impacted service approves data migrations and validates domain-specific recovery checks.

## Audit requirements

Store rollback actor, approving owner, artifact digest, and post-check evidence in the deployment audit log.

