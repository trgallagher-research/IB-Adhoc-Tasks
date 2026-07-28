# Build route B — text template (use this when clipboard paste is unavailable)

The `paste-actions/` clipboard route is tenant- and designer-version dependent.
In this tenant the **My clipboard** tab does not accept a pasted action
(confirmed 2026‑07‑28), so this is the working route.

## Why a second encoding exists

`compose-item-payload.json` holds the payload as a JSON **object** whose values
are bare-`@` expressions. That form only survives the clipboard route: pasted
into a designer input field, bare `@` expressions are stored as inert text.

`compose-item-payload.template.txt` is the same 61 properties encoded as a JSON
**text template** using `@{...}` interpolation — the mechanism the existing flow
already relies on (the AI action's SubmissionText field carries dozens of
`@{...}` tokens), so it is proven to work in this tenant. Both files are
generated from the same spec by the same script and are semantically identical.

## Type control in the text form

The text template must emit *typed* JSON, so each value fragment is built to
produce the right literal:

| Case | Emitted | Result in JSON |
|------|---------|----------------|
| answered text | `"escaped value"` (quotes added by the expression) | JSON string |
| blank text | the bare word `null` | JSON null |
| answered rating | bare integer via `int()` | JSON number |
| blank rating | bare word `null` | JSON null |
| date / response ID | quotes are in the template itself | JSON string |

Note the quoting asymmetry: fields that can be null carry **no quotes in the
template** (the expression supplies them when there is a value), while fields
that can never be null (`SubmittedDate`, `FormResponseID`, `ContentTypeId`)
are quoted in the template directly. This is deliberate — do not "tidy" it.

## Escaping

Every free-text value passes through an explicit escape chain before being
quoted:

```
\  -> \\      then
"  -> \"      then
CR -> \r ,  LF -> \n ,  TAB -> \t     (via decodeUriComponent so no literal
                                       control characters sit in the expression)
```

Order is load-bearing: the backslash must be escaped first, or the escapes
added afterwards would themselves be re-escaped. Power Automate string literals
use single quotes and treat backslash as an ordinary character, so `'\'` is one
backslash and `'\\'` is two.

**This escaping is unverified in a live tenant.** Test **T4** (JSON-sensitive
characters) is the check that proves it; run it before cutover. If T4 fails
with a body-parse error, capture the Compose output and the exact error — the
fallback is to drop the free-text escape chain and instead post those columns
in a follow-up `MERGE` update where the connector handles escaping.

## Build steps

1. **Smoke test first** (2 minutes, proves the mechanism):
   add a Compose named `Compose item payload`, paste
   `compose-item-payload.SMOKETEST.txt` (3 properties) into its **Inputs**
   field, save, and run one dummy submission. In the run history the Compose
   output must be valid JSON with real values — a quoted Title string, and a
   bare number or `null` for the rating. If that works, the full file will.
2. Replace the Compose Inputs with the whole of
   `compose-item-payload.template.txt`, save.
3. Point the HTTP action's **Body** at it:
   `@{outputs('Compose_item_payload')}` — wrap in `json(...)` only if the
   action rejects a string body.
4. Verify with **Peek code** that the Compose `inputs` is a single text blob
   containing `@{` tokens, and that no `@@` appears anywhere.

## Which file to keep

Both. `compose-item-payload.json` remains the canonical machine-readable
artefact (and the one the validation report describes); the `.template.txt` is
the transfer format for this tenant. Regenerating either regenerates both.
