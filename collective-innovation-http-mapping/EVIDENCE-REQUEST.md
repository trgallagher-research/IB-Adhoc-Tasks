# Consolidated evidence request

Everything repository-local that could be built from current evidence has been
built. The items below are the only remaining blockers; each lists exactly what
to capture, where to put it, and what it unblocks. Work them in order — EV‑1
and EV‑2 unblock the most.

Reminder for all captures: place unredacted originals in the relevant
`raw/` folder (git-ignored), then a redacted copy in `sanitized/` following the
folder's instructions file. Dummy submissions only; never real submission text.

## EV‑1 — Live SharePoint schema export (highest value)

- **How:** `03-sharepoint-schema/COLLECTION-INSTRUCTIONS.md` (browser GET or a
  one-off HTTP action in a copied flow — the latter also proves permission P1/P2).
- **Unblocks:** the SharePoint side of *every* mapping (internal names, types,
  required flags, choice sets, defaults); the excluded-system-fields list; the
  raw-fields-without-Form-source coverage section; whether a Form-response-ID
  column and processing/audit columns exist; whether `StrategicGoals` /
  `ImpactedProgrammes` are multiline text (text serialization) or MultiChoice.
- **Then:** internal-name assignments are added to `scripts/build_mapping_spec.py`
  with the schema as evidence, and `./scripts/run_checks.sh` regenerates a
  non-empty executable payload.

## EV‑2 — Existing flow export or per-action Peek code

- **How:** `04-existing-flow/COLLECTION-INSTRUCTIONS.md`. If export is blocked,
  `create-item.json` (Peek code of the current Create item) alone is the single
  most valuable file.
- **Unblocks:** `Existing`-state preservation of all working mappings; the
  `OriginalSubmission` source expression; the real `ReviewStatus` default; the
  AI-layer field routing; the live `Get response details` action name; the
  trigger's exact response-ID expression (currently `Probable`).

## EV‑3 — `Get response details` body for reference response 2

- **How:** open the flow run that processed response 2 (submitted 2026‑07‑24
  11:25) → `Get response details` → Outputs → copy the body. Redact `responder`
  and headers as in the response‑6 sanitized file; save as
  `02-get-response-details/sanitized/get-response-details-response-2.body.json`.
- **Unblocks:** most of the 21 text-question keys currently Unresolved with no
  candidates (Sponsor, partner fields, local market, chief support, comments,
  impact/evidence fields, IBEN/PL/additional explanations, Impacted
  Programme(s) via its distinctive `MYP;DP` array) — response 2's answers are
  distinctive dummy sentences.

## EV‑4 — Three designed disambiguation submissions (A, B, C)

Resolves what response 2 cannot: Yes/No keys and 1–5 rating keys, which are
never distinctive individually. Submit three dummy responses to the live form,
then capture each `Get response details` body as in EV‑3.

**Text fields:** in submission A, answer every text question with a unique
marker sentence containing the question's column number, e.g.
`Marker A col 12 — dummy text.` (any distinctive per-question text works).
This confirms every text key in one capture, independent of EV‑3.

**Ratings** (needs the local-market branch open in A and B so all six rating
questions appear — answer the market question Yes):

| Rating question (Excel col) | A | B |
|---|---|---|
| Strategic importance (23) | 1 | 1 |
| Localized service offerings (25) | 2 | 1 |
| Financial Impact (32) | 3 | 2 |
| Operational Impact: support volume (34) | 4 | 3 |
| Operational Impact: operations changes (35) | 5 | 4 |
| Reputational Impact (37) | 1 | 5 |

Every question's (A,B) value pair is unique, so the six keys resolve exactly.

**Yes/No questions** (7 incl. conditionals; the (A,B,C) triple per question is
unique):

| Yes/No question (Excel col) | A | B | C |
|---|---|---|---|
| External Partner Involved? (11) | Yes | No | Yes |
| Local market impact? (17) | Yes | Yes | Yes |
| Compliance boundary adaptation? (19) | Yes | Yes | No |
| Chief support secured? (20) | Yes | No | *(hidden)* |
| IBEN impact? (41) | Yes | No | No |
| Professional Learning impact? (43) | No | Yes | Yes |
| Additional factors? (45) | No | No | Yes |

- **Unblocks:** the five-way 'No' candidate set, the two-way '1' rating pair,
  the two `Probable` ratings → `Confirmed`, and the conditional-question keys.
- Delete the dummy SharePoint items the production flow creates for A/B/C (or
  note their IDs) so the list stays clean.

## EV‑5 — Small confirmations (no capture needed, one look each)

1. In the Forms editor: confirm **Implementation Readiness Notice** is a
   text/section element with no input (current determination: no SharePoint
   destination; blank in all six reference responses).
2. Confirm the exact list title is `Knowledge Submissions` (used in every Uri).
3. Confirm whether a **Form response ID column** exists on the list (comes free
   with EV‑1); if not, decide who adds it (permission matrix P6).
4. Site URL for the action configs (kept as `<<site-url>>` in committed files).

## What happens when evidence lands

```
./scripts/run_checks.sh
```

regenerates inventories → spec → reports → payload → validation report and runs
the quality gate. Mapping upgrades happen only in `scripts/build_mapping_spec.py`
(with evidence strings), never by hand-editing generated files.
