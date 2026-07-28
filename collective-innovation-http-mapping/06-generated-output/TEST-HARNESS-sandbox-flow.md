# Test harness — sandbox flow (test without burning form submissions)

A standalone, manually-triggered flow that replays **any existing Forms
response** through the payload logic. Build it once; run it as often as you
like. It touches nothing in production: no trigger, no SharePoint write, no
effect on the real or copied flow.

Use it to prove the payload before wiring the copied flow, and to re-test after
any payload change. A failed form submission (e.g. submitted while no flow was
enabled) is not wasted — its response still exists in Forms and can be replayed
here by ID.

## What it covers

50 of the 61 payload properties: **all 39 raw question columns**, all 5
metadata/audit properties, and the 6 constant/`utcNow()` flow-layer ones. The
11 properties sourced from `Run_a_prompt` / `Select_*` are omitted because
those actions do not exist here — they are preserved verbatim from the working
flow, so live test **T2** is their check.

This means the harness exercises the entire risk surface this project created:
key resolution, blank→null typing, choice pass-through, multi-choice
serialization, date shape, Title truncation, and the character escaping.

## Two ways to build it

**Route 1 — connector-free (recommended).** A Compose stands in for `Get
response details`, so the harness needs no Forms connection at all. This
sidesteps the Form Id dropdown entirely, which matters because the dropdown
lists only personally-owned forms and rejects a pasted ID for a group-owned
one. It also lets the escaping test (T4) run immediately, with no form
submission. See **Build A** below.

**Route 2 — live Forms call.** Uses the real connector against a real
response. Only worth doing once Route 1 is green, and only if you want to
confirm the live body matches the fixture. See **Build B**.

## Build A — connector-free (~5 minutes)

1. Power Automate → **Create** → **Instant cloud flow** →
   `ZZ Sandbox — payload test` → trigger **Manually trigger a flow** → Create.
2. **+ New step** → **Compose** → rename to exactly **`Compose response id`**.
   Inputs: `7` (any number; it only feeds the Title fallback and FormResponseID).
3. **+ New step** → **Compose** → rename to exactly **`Get response details`**.
   *(Yes — a Compose with the connector's name. Expressions reference actions by
   name, so this transparently substitutes for it.)*
   Inputs: click **fx** (Expression) and paste the whole of
   `compose-fake-response.RESPONSE6.txt` — a single `json('…')` expression.
4. **+ New step** → **Compose** → rename to **`Compose labelled submission`** →
   Inputs: paste `compose-labelled-submission.txt`.
5. **+ New step** → **Compose** → rename to **`Compose item payload`** →
   Inputs: paste `compose-item-payload.SANDBOX.txt`.
6. **Save** → **Test** → *Manually* → **Run flow**.

Why this is faithful: the Forms connector flattens its output to keys like
`body/r<hash>`, and `?['body/x']` is a *literal* key lookup — so an object
built by `json()` with those same flat keys is indistinguishable to every
downstream expression. The fixture is the sanitized response 6, dummy data
already in this repo.

**Then run the escaping test (T4) immediately:** change the `Get response
details` Compose input to `compose-fake-response.EDGECASE.txt` and run again.
That body carries `"` `'` `\`, a newline, a tab, a CR, accented characters and
an emoji, plus a two-value multi-choice and a rating. If the payload output
still parses as JSON, the escaping chain is proven.

## Build B — live Forms call (~10 minutes)

1. Power Automate → **Create** → **Instant cloud flow** → name it
   `ZZ Sandbox — payload test` → trigger **Manually trigger a flow** → Create.
2. **+ New step** → **Compose** → rename to exactly **`Compose response id`**.
   Inputs: the response number you want to replay, e.g. `7`.
   *(This is the only thing you edit between test runs.)*
3. **+ New step** → Microsoft Forms → **Get response details**.
   - *Form Id*: pick the innovation intake form from the dropdown. **If it is
     not listed** — expected, because the dropdown shows only forms you
     personally own and this one is group-owned — choose **Enter custom value**
     and paste the form ID. Get it from the original flow: `Get response
     details` → **⋯ → Peek code** → the `form_id` value (88 characters, ends
     `PWcu`). It is deliberately redacted in `04-existing-flow/sanitized/`, so
     the live flow is the source of truth for it; do not commit it.
   - *Response Id*: click into the field, choose the **Expression** tab (*fx*)
     in the popup — **not** the Dynamic content tab — and enter
     `outputs('Compose_response_id')`.
   - **Gotcha:** clicking into either field opens the dynamic-content panel,
     and a stray click there drops a token (typically `Body`) into the field.
     A Form Id containing text *plus* a token is rejected with a misleading
     "'Form Id' is required". Delete any such pill with its **×** so Form Id
     holds plain text only. Confirm via the action's **Code view** tab:
     `form_id` must be a plain string, `response_id` must be
     `@outputs('Compose_response_id')`.
   - Confirm the action is named exactly **`Get response details`** (rename if
     the designer appended a number — the expressions depend on it).
4. **+ New step** → **Compose** → rename to exactly
   **`Compose labelled submission`** → Inputs: paste the whole of
   `compose-labelled-submission.txt`.
5. **+ New step** → **Compose** → rename to exactly **`Compose item payload`**
   → Inputs: paste the whole of `compose-item-payload.SANDBOX.txt`.
6. **Save**.

## Run and read the results

**Test** → *Manually* → **Test** → **Run flow**. It finishes in seconds.

Open the run and check each Compose output in turn:

| Check | What you want to see | What failure looks like |
|-------|---------------------|-------------------------|
| `Compose labelled submission` | The full labelled text with **real answers** substituted | Literal `@{outputs(...)}` text — the paste did not evaluate |
| `Compose item payload` renders | A JSON object with your answers | Literal `@{` tokens, or the whole thing as one quoted string |
| Blank answers | `null` with no quotes | `""`, `0`, or the word `"null"` in quotes |
| Answered ratings | a bare number, e.g. `3` | `"3"` in quotes |
| `StrategicGoals` | `"Driver A1; Driver B2"` — semicolon-joined text | `["Driver A1"]` left as a JSON array string |
| `AnticipatedLaunchDate` | `"2026-12-01"` | `""` or a mangled date |
| Yes/No columns | `"Yes"` / `"No"` verbatim | `true`/`false`, or `"N/A"` |
| `Title` | quoted text, ≤255 chars | untruncated long text, or `null` |

**The decisive check:** copy the `Compose item payload` output into any JSON
validator (or just re-paste it into a scratch Compose). If it parses, the body
is well-formed and the escaping held.

## Escaping test (T4) — see Build A; also runnable against a live response

Submit one dummy form response whose free-text answers contain
`He said "let's try" — line one`, a line break, a backslash `\`, and an accented
character. Note its response ID, put that ID in `Compose response id`, re-run.
The payload output must still be valid JSON, with the quotes appearing as `\"`
and the line break as `\n`. If it breaks, capture the output and the error —
the fallback is documented in `BUILD-ROUTE-text-template.md`.

## Re-testing later

Change the number in `Compose response id`, run again. To re-test after a
payload regeneration, re-paste `compose-item-payload.SANDBOX.txt`.

## When you are done

Leave the sandbox flow in place (it is inert — a manual trigger that writes
nothing), or delete it. It is prefixed `ZZ` so it sorts to the bottom of My
flows. It is **not** part of the production design and must never be given a
Forms trigger or a SharePoint write action.
