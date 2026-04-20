---
doc_id: DOC-SEC-001
title: Privileged Production Access Policy
version: "5.0"
owner_team: Security Operations
domain: security
systems:
  - Access Broker
  - Citadel Gateway
policies:
  - POL-SEC-003
references:
  - DOC-SEC-002
  - DOC-POL-001
---

# Privileged Production Access Policy

This policy governs privileged production access for infrastructure, data stores, and control plane services.

## Core requirements

- all privileged production access must be brokered through Access Broker
- standing administrator accounts are prohibited for human operators
- approval requires the operator's manager and the active Security Operations approver for high-risk systems
- session recording is mandatory for shell or console access to production
- break-glass sessions expire after sixty minutes unless re-approved

## High-risk systems

High-risk systems include authentication gateways, billing pipelines, incident tooling, and stores containing customer profile or retention metadata.

## Exceptions

Exceptions require written approval from Security Operations and Privacy Engineering. Approved exceptions must cite the retention category and expiry date.

## Related procedures

If privileged credentials are suspected to be exposed during an incident, the [Security Incident Response Playbook](../security/security-incident-response-playbook.md) and the [Severity 1 Escalation Runbook](../platform/sev1-escalation-runbook.md) both apply.

