# Implementation instructions — modified flow design

Manual-transfer guide for the copied Power Automate flow. Everything here uses
evidenced structural identifiers where they exist; placeholders in
`<<double angle brackets>>` require evidence that is still outstanding (see
`EVIDENCE-REQUEST.md`). **Do not deploy while any placeholder remains.**

## Flow shape (unchanged upstream, new tail)

```
When a new response is submitted            (existing trigger)
→ Get response details                      (existing; action name VERIFIED: Get_response_details)
→ [NEW] Compose_labelled_submission         (the existing labelled text, moved out of the AI action
                                             verbatim — content: compose-labelled-submission.txt)
→ Run a prompt                              (existing — change ONLY its SubmissionText input to
                                             @{outputs('Compose_labelled_submission')})
→ Select actions ×8                         (existing — preserve verbatim)
→ [NEW] Compose: item payload               (compose-item-payload.json — fully replaces Create item:
                                             39 raw columns + audit fields + all 17 flow-layer
                                             properties the old Create item set)
→ [NEW] Scope: TRY
    → [NEW] Send an HTTP request to SharePoint: duplicate check (GET)
    → [NEW] Condition: no existing item
        yes → [NEW] Send an HTTP request to SharePoint: create item (POST)
        no  → terminate (Succeeded) — duplicate delivery, skip
→ [NEW] Scope: CATCH  (Configure run after: TRY has failed / timed out)
    → notification + audit (below)
→ [REMOVED] Create item                     (replaced by the HTTP POST)
```

Set **trigger concurrency to 1** (trigger settings → Concurrency Control → On,
degree 1) so two near-simultaneous submissions cannot race the duplicate check.

## 1. Compose: item payload

Action name: **`Compose item payload`** (referenced in expressions as
`Compose_item_payload`).

**Transfer format — read `BUILD-ROUTE-text-template.md` first.** This tenant's
designer does not accept clipboard-pasted actions, so the payload is
transferred as `compose-item-payload.template.txt` (a JSON text template using
`@{...}` interpolation) pasted into the Compose **Inputs** field. Prove the
mechanism with `compose-item-payload.SMOKETEST.txt` (3 properties) before
pasting all 61. The object form below describes the intended semantics and
remains the canonical artefact.

Authoring rules that make it safe:

- Build the input as a **JSON object in the designer**, with each property's
  value being a single expression token — in code view that is the
  `"@if(...)"` form (one `@`, no `{}`). A single-token expression keeps its
  native type, so `null` stays JSON null and `int(...)` stays a number.
- Never assemble JSON by string concatenation; platform serialization is what
  guarantees quotes, apostrophes, line breaks and Unicode are escaped.
- The expressions reference `outputs('Get_response_details')` — **rename to
  match the real action name** (spaces become underscores). Verify once in the
  live flow.

Blank handling contract (already encoded in the generated expressions):

| Source situation | Sent to SharePoint |
|------------------|--------------------|
| unanswered text/multiline question (`''`) | `null` |
| unanswered rating (`''`) | `null` (never `''`, never `0`) |
| unanswered date (`''`) | `null` (never `''`) |
| unanswered Yes/No (`''`) | `null` (never `false`, never `'N/A'`) — pass answers through verbatim; `ComplianceBoundaryAdaptation` also accepts "I don't know" |
| multi-choice answer `'["A","B"]'` | `'A; B'` (text serialization — `StrategicGoals`/`ImpactedProgrammes` confirmed as multiline text, not MultiChoice) |
| answered value | trimmed value, typed per live schema |

## 2. Duplicate check (GET)

- Action: **Send an HTTP request to SharePoint** (same connection as the
  existing Create item)
- Site Address: `<<site-url>>`
- Method: `GET`
- Uri (`FormResponseID` confirmed by the live schema as a **Text** column, so
  the filter value is **quoted**):

  ```
  _api/web/lists/getbytitle('Knowledge Submissions')/items?$select=Id&$top=1&$filter=FormResponseID eq '@{triggerOutputs()?['body/resourceData/responseId']}'
  ```

- Headers: `Accept: application/json;odata=nometadata`
- Condition: `@empty(body('Duplicate_check')?['value'])` → *yes* = safe to create.

The trigger expression is now **verified** (used identically in the existing
flow's Get response details, AI prompt, and Create item — EV‑2), so the
duplicate check and the `FormResponseID` payload property are fully evidenced.
If the list may exceed 5,000 items, index `FormResponseID` (permission P7).

## 3. Create item (POST)

- Action: **Send an HTTP request to SharePoint**, same connection
- Site Address: `<<site-url>>`
- Method: `POST`
- Uri: `_api/web/lists/getbytitle('Knowledge Submissions')/items`
- Headers:

  ```
  Accept:        application/json;odata=nometadata
  Content-Type:  application/json;odata=nometadata
  ```

- Body: `@{outputs('Compose_item_payload')}`

With `odata=nometadata` on both headers, no `__metadata`/entity-type wrapper is
required. Success returns **201** with the created item (capture
`body(...)?['Id']` if downstream steps want it).

## 4. Title

Live schema: `Title` is **not required** on this list (linked-title view
column displays as "Opportunity"). The existing flow maps Title to the raw
Opportunity Description — a latent runtime failure for descriptions over the
255-character Text limit. The generated expression is a **documented
deviation**: truncated at 255 with an ellipsis, falling back to
`Form response <id>` (verified trigger path) when blank; never null.

## 5. OriginalSubmission

The existing flow builds the labelled submission text inline in the AI action
and **never stores it** — the column sits empty. The replacement closes that
audit gap without changing the text: the identical template (preserved
verbatim in `compose-labelled-submission.txt`, extracted from the flow
capture) moves into `Compose_labelled_submission`, which feeds both the AI
prompt and the `OriginalSubmission` payload property.

## 6. Processing status / error handling

- The existing flow **explicitly sets** `ProcessingStatus` = `Processed`,
  `ProcessedDate` = `utcNow()`, `PromptVersion` and `SourceForm` constants —
  all preserved verbatim in the payload's flow-layer properties (including the
  `PromptVersion` trailing-newline quirk; trim it only as a reviewed change).
  `ProcessingError` is not set by the existing flow and is written only by the
  new catch path.
- CATCH scope (runs after TRY fails or times out):
  1. `Compose_error_detail`: `@{result('TRY')}` — captures which action failed
     and the raw error body.
  2. Notify (email or Teams to the maintainer) including the Form response ID
     and the composed payload for replay.
  3. Do **not** attempt a second create from the catch path — failed runs are
     replayed from the run history (**Resubmit**) after the cause is fixed;
     the duplicate check makes resubmission idempotent.
- `ReviewStatus` is set explicitly to `Not reviewed` — exactly as the existing
  flow does (and matching the column default); other reviewer and
  projected-impact fields are never in the payload.

## 7. Distinguishing permission errors from payload errors

| Symptom | Meaning | Action |
|---------|---------|--------|
| `403` / "Access denied" | connection lacks write on this list | permission matrix row P4; not a payload issue |
| `401` | connection expired/broken | re-authenticate the SharePoint connection |
| `404` on the Uri | wrong list title or site address | fix Uri; check exact list title |
| `400` "The property '<name>' does not exist on type…" | wrong internal name | schema evidence wrong/stale — re-export fields |
| `400` "Invalid data has been used to update the list item" / type message | value/type mismatch (e.g. string into Number) | payload bug; compare against validation report |
| `400` "Specified value is not supported for the … field" | Choice value not in live choice set | update choice normalization from live schema |
| Action blocked before run / DLP violation banner | tenant DLP forbids the HTTP action | approach-assessment fallback; needs admin conversation |

## 8. Phase 1 file scope

The Forms supporting-files answer is a reference to files stored in the form
owner's upload folder — posting it to a list field does **not** attach files.
Phase 1: the payload excludes the upload answer entirely. If a visible trace is
wanted, the only safe Phase 1 option is a text column explicitly labelled as a
file *reference*; actual attachment migration (copy file + `AttachmentFiles`
endpoint) is a separate later phase with its own permissions test.

## 9. Regeneration loop

After any new evidence lands in `01`–`04`:

```
./scripts/run_checks.sh
```

rebuilds inventories → spec → reports → payload → validation report, and fails
loudly if any rule is violated. Transfer the regenerated
`compose-item-payload.json` into the Compose action manually.
