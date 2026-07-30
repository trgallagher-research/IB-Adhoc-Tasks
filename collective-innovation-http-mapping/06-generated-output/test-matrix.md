# Test matrix

All tests run in the **copied** flow against dummy submissions from your own
account. The production flow stays untouched. Tests marked ⚠ are negative
tests — expected to fail in a specific way.

| ID | Purpose | Input | Expected result |
|----|---------|-------|-----------------|
| T0 | DLP / action availability (permission P1) | read-only schema GET | 200 with field JSON; a DLP block fails the run before SharePoint responds |
| T1 | Minimal create | dummy submission answering only required questions | 201; item created; every unanswered Number/DateTime/Choice column empty (not 0, not 1900-01-01, not 'null') |
| T2 | Full create | dummy submission answering every question incl. conditionals | 201; every mapped column populated; values match the submission verbatim |
| T3 | Blank-to-typed handling | dummy submission with rating and date questions left blank (if form permits) | 201; Number/DateTime columns empty; no `''`-to-type error |
| T4 | JSON-sensitive characters | dummy answers containing `"` `'` `\` line breaks, Unicode (é, ü), emoji | 201; text stored intact; no payload parse error |
| T5 | Multi-choice serialization | Strategic Goals with 3 selections; Impacted Programmes with 2 | 201; stored as `'A; B; C'` joined text (per brief's multiline-text expectation) |
| T6 | Title fallback + truncation | (a) blank-description dummy if the form allows; (b) description > 255 chars | (a) Title = `Form response <id>`; (b) Title truncated at 255 with `...` |
| T7 | Duplicate prevention | Resubmit the successful T2 run from run history | run succeeds but takes the duplicate branch; **no second item** |
| T7b | Duplicate check is form-scoped | inspect the `Duplicate check` Uri | filter includes `and SourceForm eq '<form name>'`. Without it, a second form's response 7 would match this form's response 7 and its submission would be silently skipped — see `multi-form-architecture.md` |
| T8 | Concurrency | two dummy submissions ~simultaneously | two items, no duplicates, no collision (trigger concurrency = 1) |
| T9 | Timezone | note submission local time; compare stored submitted-on value | stored UTC instant equals the submission moment (submitDate is UTC; Excel export is tenant-local — do not "correct" twice) |
| T10 ⚠ | Wrong internal name detection | POST with one deliberately misspelled property | 400 "property does not exist" — confirms the error signature used in triage |
| T11 ⚠ | Choice mismatch detection | POST a Choice value not in the live choice set (dummy item, delete after) | 400 "value is not supported" — confirms choice validation is active on this list |
| T12 | Catch path | force TRY failure (e.g. temporarily misspell the list title) | CATCH runs; notification received with response ID + payload; no partial item |
| T13 | Post-fix replay | after T12, fix and Resubmit the failed run | item created exactly once (T7 logic protects the replay) |
| T14 | Conditional-branch payload | dummy with External Partner = No | partner columns empty, not `'N/A'`/`false` |
| T15 | AI-layer isolation | inspect T2's item | raw-answer columns contain Forms values only; AI fields contain AI output only; reviewer + projected-impact fields blank; ReviewStatus at default |

Record each result (run link, item ID, pass/fail) in a copy of this table in
`06-generated-output/test-results-<date>.md` before cutover. T1–T15 all passing
is a cutover precondition.
