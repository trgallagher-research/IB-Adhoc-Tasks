# Collective Innovation — HTTP Mapping

Working folder for mapping Microsoft Forms responses to their destination
SharePoint list (`Knowledge Submissions`) and generating the Compose + 
`Send an HTTP request to SharePoint` implementation used by the flow.

## Status (2026-07-28)

| Area | State |
|------|-------|
| Forms Excel evidence | ✅ ingested — 47 cols (6 metadata + 41 questions), 6 dummy responses; inventory in `01-forms-excel/sanitized/` |
| Get response details evidence | ✅ response 6 ingested (sanitized, body-only) — 48 opaque keys; inventory in `02-get-response-details/sanitized/` |
| Forms-key mappings | 9 **Confirmed**, 2 Probable, 30 Unresolved (of 41 questions) — see `05-mapping-spec/` |
| SharePoint schema evidence | ❌ absent — **all SharePoint-side facts Unresolved**; see `03-sharepoint-schema/COLLECTION-INSTRUCTIONS.md` |
| Existing flow evidence | ❌ absent — see `04-existing-flow/COLLECTION-INSTRUCTIONS.md` |
| Executable payload | intentionally **empty** (0 mappings meet the Existing/Confirmed-both-sides bar); pipeline proven end-to-end on dummy fixtures |
| Blockers | consolidated in `EVIDENCE-REQUEST.md` (EV‑1…EV‑5) |
| Git history exposure | assessed in `GIT-EXPOSURE-NOTE.md`; working tree remediated, history decision pending |

**Regenerate everything after new evidence:** `./scripts/run_checks.sh`
(rebuilds inventories → mapping spec → reports → payload → validation report,
then runs the quality gate). Mapping upgrades are made only in
`scripts/build_mapping_spec.py`, with evidence strings — never by editing
generated files.

Key documents: `05-mapping-spec/mapping-spec.md` (+ `unresolved-mappings.md`,
`coverage-report.md`), `06-generated-output/approach-assessment.md`,
`implementation-instructions.md`, `permission-matrix.md`, `test-matrix.md`,
`cutover-rollback.md`, `validation-report.md`.

## Folder structure

| Folder | Contents |
|--------|----------|
| `01-forms-excel/` | Microsoft Forms responses exported to Excel |
| `02-get-response-details/` | Output of the flow's "Get response details" action |
| `03-sharepoint-schema/` | Target SharePoint list schema (columns / internal names) |
| `04-existing-flow/` | Export of the existing Power Automate flow |
| `05-mapping-spec/` | Field mapping specification (source → SharePoint) |
| `06-generated-output/` | Generated mapping artifacts / HTTP request bodies |

Folders `01`–`04` each contain two subfolders:

- **`raw/`** — unredacted, local-only inputs. **Never committed** (git-ignored).
- **`sanitized/`** — redacted inputs that are safe to commit.

`raw/` directories are intentionally absent from git; recreate them locally as
needed. Only `sanitized/` content is version-controlled.

## Data-handling rules

**`raw/` files must never be committed.** They are git-ignored so that
unredacted source data — real Forms exports, flow exports, response payloads —
never leaves the local machine.

**`sanitized/` files must not contain any of the following:**

- personal names
- email addresses
- access tokens
- cookies
- connection credentials
- tenant secrets
- real submission content

**The following *may* be retained in `sanitized/`, because the mapping cannot be
built without them:**

- opaque Microsoft Forms response keys (the question / response identifiers)
- SharePoint internal field names (e.g. `Title`, `field_5`, `OData__x0037_…`)

These are structural identifiers, not personal content.

## Mapping rules

- **Never map on field order alone.** Every generated mapping must be justified by
  a stable identifier (a Forms response key or a SharePoint internal name) or an
  explicit label match. Positional coincidence ("column 3 → column 3") is not a
  valid basis for a mapping.
- **Report unresolved mappings; do not guess.** Any source field that cannot be
  confidently matched to a destination field is listed as *unresolved* in the
  mapping spec for a human to resolve. A guessed mapping is worse than a flagged
  gap.
