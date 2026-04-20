---
doc_id: DOC-SEC-002
title: Security Incident Response Playbook
version: "4.1"
owner_team: Security Operations
domain: security
systems:
  - Access Broker
  - Incident Hub
policies:
  - POL-SEC-003
  - POL-PRIV-001
references:
  - DOC-SEC-001
  - DOC-PLAT-001
---

# Security Incident Response Playbook

Use this playbook for suspected compromise, credential theft, unauthorized access, or confirmed exfiltration.

## Severity linkage

Any confirmed or suspected compromise of privileged production credentials is managed as Severity 1 until containment and credential rotation are complete.

## Response steps

1. declare the incident in Incident Hub
2. isolate impacted credentials or workloads
3. preserve logs, access broker approvals, and session recordings
4. notify Privacy Engineering if regulated personal data could be implicated
5. complete containment, eradication, and recovery review

## Evidence retention

Security incident records, approval traces, and response artifacts follow the [Data Retention Standard](../policies/data-retention-standard.md) unless a documented exception has been granted.

