# Coverage report

Generated 2026-07-28 by `scripts/build_reports.py` from `mapping-spec.json` and the response-key inventory.

## Totals reconciliation

| Population | Count | Breakdown |
|------------|-------|-----------|
| Excel columns | 47 | 6 Forms metadata + 41 questions |
| Question mappings | 41 | 9 Confirmed + 2 Probable + 30 Unresolved (Forms side) |
| Opaque `r…` keys | 48 | 11 assigned (Confirmed+Probable) + 7 in candidate pools + 30 blank/unattributable + 0 otherwise unaccounted |
| Executable mappings | 0 | SharePoint schema evidence absent |

Key-count arithmetic: 48 keys − 41 questions = **at least 7 surplus keys** even if every question maps 1:1; with 30 blank keys against 23 unanswered questions in response 6, the surplus is consistent but the specific surplus keys cannot be identified from current evidence.

## 1. Form fields without a SharePoint destination

- **Implementation Readiness Notice (Q22)** — determined to need NO destination: blank in all six reference responses including the fully completed one, so it is a display-only element. (Verify once against the live form.)
- **Add any supporting files (Q47)** — no ordinary-field destination; Phase 1 treats file references separately (see implementation instructions).
- **Excel metadata 'Start time' and 'Last modified time'** — no Get-response-details equivalent; no destination proposed.
- **Excel metadata 'Name'** — no Get-response-details equivalent (only `responder` email); destination undecided.
- All other question fields have an *intended* destination that is Unresolved pending schema evidence — they are not 'no destination' cases.

## 2. Intended raw SharePoint fields without Form sources

Cannot be enumerated until the live schema export arrives. Known-by-hint candidates from the brief (Title is flow-constructed; FormResponseId is flow-constructed) are covered in the implementation design. This section must be regenerated after schema ingest.

## 3. Unexplained Forms keys

- 30 keys are blank in response 6 and unattributable.
- Of the 18 non-blank keys: 11 assigned, 7 sit in candidate pools (five 'No' values, two '1' values).
- At least 7 keys are surplus to the 41 questions (possible section/notice elements, deleted or hidden questions). Their identity is unknowable from current evidence.

## 4. Existing AI and processing mappings

Innovation Type, Horizon, Categorization, Ownership, OriginalSubmission and the labelled-submission construction remain with the existing flow actions. **Pending `04-existing-flow/` export**; they are preserved, not rebuilt, and are out of scope for the raw-answer payload.

## 5. Intentionally blank reviewer fields

Human-review/governance fields (including ReviewStatus default 'Not reviewed' pending flow proof) are intentionally not populated by the create payload.

## 6. Intentionally blank projected-impact fields

Projected-impact measures (Word model, governance layer) are intentionally blank at item creation.

## 7. Excluded SharePoint system fields

Standard system/hidden/read-only fields (e.g. content type, version, created/modified stamps, author/editor) will be excluded from the payload as a rule. The exact exclusion list is generated from the live schema export (`Hidden eq true`, `ReadOnlyField eq true`) — not enumerable until then.
