---
doc_id: DOC-PLAT-001
title: Severity 1 Escalation Runbook
version: "3.2"
owner_team: Site Reliability Engineering
domain: platform
systems:
  - Citadel Gateway
  - Edge Ingress
  - Incident Hub
policies:
  - POL-SEC-003
  - POL-PRIV-001
references:
  - DOC-PLAT-002
  - DOC-SEC-002
  - DOC-POL-001
---

# Severity 1 Escalation Runbook

Use this runbook when customer-facing availability is materially impaired, regulated data exposure is suspected, or the control plane cannot deploy or roll back safely.

## Trigger conditions

A Severity 1 incident is declared when one of the following is true:

- production request failure rate exceeds 35% for more than five minutes
- the primary customer control plane is unavailable across two regions
- privileged production credentials are suspected to be exposed
- rollback of the last safe deployment cannot be completed within fifteen minutes

## Escalation path

1. The incident commander is the active SRE primary until relieved by the VP-level delegate for platform operations.
2. The communication lead is assigned from Developer Experience unless the outage is security-originated.
3. If the event involves privileged access, the Security Operations lead joins within ten minutes and the incident remains Sev 1 until credential rotation is confirmed.
4. If customer data handling is implicated, the privacy liaison from Trust Engineering is paged immediately.

## Paging order

- page `sre-primary` and `platform-duty-manager`
- open an `#inc-sev1-*` channel in Incident Hub
- page the owning service team for the affected system
- notify Executive Response if status page degradation lasts longer than fifteen minutes

## Communication cadence

The incident commander posts an update every fifteen minutes until mitigation is complete. External status page messaging must align with the internal timeline but may omit internal topology details.

## Rollback requirement

If the failed change is linked to deployment automation, follow the [Deployment Rollback Runbook](../platform/deployment-rollback-runbook.md). The Deployment Platform team owns rollback tooling, while the affected service owner approves data-destructive reversions.

## Evidence and audit

Record the declaration time, paging timestamps, responder changes, containment actions, and final mitigation decision in Incident Hub. Retain the incident record for seven years under the [Data Retention Standard](../policies/data-retention-standard.md).

