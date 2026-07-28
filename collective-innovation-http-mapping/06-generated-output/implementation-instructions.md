# Implementation instructions — modified flow design

Manual-transfer guide for the copied Power Automate flow. Everything here uses
evidenced structural identifiers where they exist; placeholders in
`<<double angle brackets>>` require evidence that is still outstanding (see
`EVIDENCE-REQUEST.md`). **Do not deploy while any placeholder remains.**

## Flow shape (unchanged upstream, new tail)

```
When a new response is submitted            (existing trigger)
→ Get response details                      (existing)
→ labelled-submission construction          (existing — preserve verbatim)
→ AI Builder / Run a prompt                 (existing — preserve verbatim)
→ Select actions                            (existing — preserve verbatim)
→ [NEW] Compose: item payload
→ [NEW] Scope: TRY
    → [NEW] Send an HTTP request to SharePoint: duplicate check (GET)
    → [NEW] Condition: no existing item
        yes → [NEW] Send an HTTP request to SharePoint: create item (POST)
        no  → terminate (Succeeded) — duplicate delivery, skip
→ [NEW] Scope: CATCH  (Configure run after: TRY has failed / timed out)
    → notification + audit (below)
```

Set **trigger concurrency to 1** (trigger settings → Concurrency Control → On,
degree 1) so two near-simultaneous submissions cannot race the duplicate check.

## 1. Compose: item payload

Action name suggestion: `Compose_item_payload`. Input: the object in
`compose-item-payload.json` (regenerated whenever the spec gains executable
mappings). Authoring rules that make it safe:

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

Still gated on EV‑2: the trigger expression above is the documented pattern but
unverified against this flow, so the duplicate check and the `FormResponseID`
payload property stay out of executable output until the flow export confirms
it. If the list may exceed 5,000 items, index `FormResponseID` (permission P7).

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

Live schema: `Title` is **not required** on this list (and its linked-title
view column displays as "Opportunity"), but the payload populates it anyway for
usable views. The generated expression never sends null: Opportunity
Description truncated to 255 characters with an ellipsis, falling back to
`Form submission <submitDate>` when blank. (The fallback deliberately avoids
the unverified trigger response-ID path; switch it to the response ID after
EV‑2 confirms the expression.)

## 5. OriginalSubmission

Destination confirmed: `OriginalSubmission` (multiline text, plain). The
source expression is preserved, not rebuilt: once the flow export is in
`04-existing-flow/`, the existing labelled-submission output expression is
copied verbatim into that property with confidence `Existing`. Until then it
is deliberately absent from the payload.

## 6. Processing status / error handling

- Confirmed columns: `ProcessingStatus` (Choice: Received / Processing /
  Processed / Failed; column default **Processed**), `ProcessedDate`
  (DateTime), `ProcessingError` (multiline). The Phase 1 payload omits them so
  the column defaults apply; whether the existing flow sets them explicitly
  awaits the flow export.
- CATCH scope (runs after TRY fails or times out):
  1. `Compose_error_detail`: `@{result('TRY')}` — captures which action failed
     and the raw error body.
  2. Notify (email or Teams to the maintainer) including the Form response ID
     and the composed payload for replay.
  3. Do **not** attempt a second create from the catch path — failed runs are
     replayed from the run history (**Resubmit**) after the cause is fixed;
     the duplicate check makes resubmission idempotent.
- `ReviewStatus` stays at its column default — **`Not reviewed`, confirmed by
  the live schema**; reviewer and projected-impact fields are never in the
  payload.

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
