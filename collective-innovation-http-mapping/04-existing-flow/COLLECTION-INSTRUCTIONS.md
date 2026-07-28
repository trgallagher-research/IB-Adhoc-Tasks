# Existing Power Automate flow — collection instructions

Goal: capture the working flow's **action definitions and expressions** so that
existing mappings (labelled-submission construction, AI Builder prompt inputs,
Select actions, Create item field assignments, trigger response-ID path) can be
preserved with confidence state `Existing` instead of being reconstructed.

Place the raw export in `04-existing-flow/raw/` (git-ignored), then a redacted
copy in `04-existing-flow/sanitized/`.

## Method A — solution/package export (complete)

1. Power Automate portal → **My flows** → the innovation intake flow → **…** →
   **Export** → **Package (.zip)**.
2. Save the zip to `04-existing-flow/raw/`.
3. Unzip; the file that matters is `definition.json` (inside
   `Microsoft.Flow/flows/<guid>/`). It contains every action, parameter and
   expression.

If Export is greyed out (some tenants restrict it), use Method B.

## Method B — per-action Peek code (no export rights needed)

In the flow editor, for each action below: **…** menu → **Peek code**, copy the
JSON shown, and save one file per action in `04-existing-flow/raw/`:

| File | Action |
|------|--------|
| `trigger.json` | When a new response is submitted |
| `get-response-details.json` | Get response details |
| `labelled-submission.json` | the existing labelled-submission construction action(s) |
| `ai-builder.json` | AI Builder – Run a prompt |
| `select-*.json` | each existing Select action |
| `create-item.json` | SharePoint – Create item |

`create-item.json` is the highest-value single file: its `parameters` block
holds the working SharePoint internal names (as `item/<InternalName>` keys) and
the working expressions — this alone can upgrade several mappings to `Existing`.

## Redaction checklist for `sanitized/`

- Replace tenant/site URLs with `<site-url>`; keep list/library names.
- Remove `connectionReferences` values (connection IDs, tenant IDs); keep the
  connector *types*.
- Remove any real submission text embedded in test values or comments.
- KEEP: action names, all expressions (`body('…')?['r…']`, `items()`, etc.),
  Forms `r…` keys, SharePoint internal names, the AI Builder prompt text (redact
  any personal names inside it).

## After ingest

Run the spec rebuild so `Existing` mappings are read from the flow evidence, and
so `OriginalSubmission`, ReviewStatus default, and the trigger's response-ID
expression stop being Unresolved/Probable.
