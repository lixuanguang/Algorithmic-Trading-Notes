---
key: s6-fix
pathways: [model-governance-controls, research-engineering-validation]
version: FIX Trading Community, Online Specification, as catalogued. Copy used: the Orchestra repository files OrchestraFIXLatest.xml (FIX Latest EP312, created 2026-09-08) and FIXTSession.xml (FIX.5.0SP2 EP247, 2019-05-16) at commit cd24169 of github.com/FIXTradingCommunity/orchestrations, retrieved 2026-10-17; documentation extracted by script
sections: messages OrderStatusRequest (H), OrderMassStatusRequest (AF), ExecutionReport (8), ResendRequest (2), SequenceReset (4); fields OrdStatus (39), ExecType (150), PossDupFlag (43), PossResend (97), OrigSendingTime (122), GapFillFlag (123), OrdStatusReqID (790), MassStatusReqID (584); OrdStatus and ExecType code sets
read:
status: draft
---

Prepared on 2026-10-17 by the source verification (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `mech:order-state-reconciliation`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- ExecutionReport carries the recipient's view of order state (OrdStatus) and the message purpose (ExecType); precedence table with Pending Cancel and Pending Replace highest.
- Status requests return ExecType = I reports; resends carry PossDupFlag; SequenceReset with GapFillFlag fills gaps.

## Limits

The specification volumes and order state-change matrices were not read.
