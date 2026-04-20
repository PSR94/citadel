---
doc_id: DOC-PRIV-002
title: Retention Exception Handling Guide
version: "1.5"
owner_team: Privacy Engineering
domain: privacy
systems:
  - Audit Vault
  - Case Ledger
policies:
  - POL-PRIV-001
references:
  - DOC-POL-001
  - DOC-SEC-001
---

# Retention Exception Handling Guide

Use this guide when data must be retained longer than the default standard or deleted earlier to satisfy legal or contractual obligations.

## When exceptions are valid

- active litigation hold
- regulator-directed preservation
- customer contract with a shorter deletion window
- security investigation requiring extended evidence preservation

## Required approvals

Every exception requires Governance Engineering approval, Privacy Engineering approval, and a recorded expiry date. Security-originated exceptions additionally require Security Operations sign-off.

## Traceability

Document the originating policy, related case identifier, requested duration, and expiry review owner in Case Ledger.

