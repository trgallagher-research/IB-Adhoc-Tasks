# Test results — 2026-07-28

Recorded against `test-matrix.md`. Environment: sandbox harness
(`TEST-HARNESS-sandbox-flow.md`, Build B — live Forms connector), replaying
Form response ID 7. Dummy data only.

## Payload composition — PASSED

`compose-item-payload.SANDBOX.json` (50 properties: 39 raw + 5 metadata + 6
constant flow-layer) evaluated in a Compose action and inspected in run output.

| Check | Result | Evidence from the run |
|-------|--------|-----------------------|
| Object mode / expressions evaluate | PASS | every property resolved; no literal `@` text |
| Blank answer → real JSON `null` | PASS | `PartnerOrganisation`, `LocalMarketDetails`, `ImpactDescription`, `StrategicImportanceScore` … all bare `null` |
| No empty strings emitted | PASS | no `""` anywhere in the output |
| Number columns receive integers | PASS | `FinancialImpactScore: 1`, `OperationalSupportScore: 1`, `OperationalChangesScore: 1`, `ReputationalImpactScore: 3` |
| Blank Number → `null`, not `0` | PASS | `StrategicImportanceScore: null`, `LocalizedServiceOfferingScore: null` |
| Text/Note columns plain strings | PASS | no double-quoting, no escaping artefacts |
| Choice pass-through verbatim | PASS | `ExternalPartnerInvolved: "No"`, `ProfessionalLearningImpact: "Yes"` |
| Blank Choice → `null` | PASS | `ComplianceBoundaryAdaptation: null`, `ChiefSupportSecured: null` |
| Multi-choice → joined text | PASS | `StrategicGoals: "Driver A1"` (from `["Driver A1"]`) |
| Date shape | PASS | `AnticipatedLaunchDate: "2026-12-01"` |
| submitDate → ISO 8601 UTC | PASS | `SubmittedDate: "2026-07-28T11:15:51Z"` from `7/28/2026 11:15:51 AM` |
| `Title` never null, ≤255 | PASS | populated from Opportunity Description (161 chars, no truncation needed) |
| Flow-layer constants preserved | PASS | `SourceForm`, `ReviewStatus: "Not reviewed"`, `ProcessingStatus: "Processed"`, `PromptVersion` (trailing newline intact), `ContentTypeId` |
| `ProcessedDate` | PASS | `utcNow()` resolved |
| Labelled submission renders | PASS | full text with real answers substituted; feeds `OriginalSubmission` |

## Consequential finding — transfer format

Pasting a JSON **object** into a Compose Inputs field is parsed as an object
and each value evaluated, so single-`@` expressions return native types. The
earlier text-template encoding (`.template.txt`), built on the assumption that
the field stores inert text, produced double-quoted strings and the *string*
`"null"`. **`compose-item-payload.PASTE.json` is the transfer format**;
`.template.txt` is retained as a fallback only.

## T4 (JSON-sensitive characters) — superseded

Object mode means the platform performs string escaping itself, so the
hand-built escape chain is no longer in the executable path. T4 is retained in
the matrix as a confirmation during live testing rather than as a risk item.

## Expected sandbox-only artefact (not a defect)

`OriginalSubmission` shows an empty "Form response ID" line: the harness uses a
manual trigger, so `triggerOutputs()?['body/resourceData/responseId']` has no
value. It populates in the real flow, where `FormResponseID: "7"` in this same
run already confirms the equivalent expression resolves.

---

# Live test — copied flow, submission A (response ID 8)

First end-to-end run of the copied flow with the HTTP actions. Verified from a
CSV export of `Knowledge Submissions` (item `FormResponseID = 8`, compared
against items 4–7 created by the original flow).

## PASSED

| Check | Evidence |
|-------|----------|
| **T0 — DLP / HTTP action permitted** | `Send an HTTP request to SharePoint` ran; item created. The generic HTTP action is **not** DLP-blocked in this tenant. |
| **P4 — connection can create items via REST** | item 8 exists |
| Title truncation at 255 + ellipsis | `Opportunity` ends `…the pilot wou...` while `OpportunityDescription` holds the full 430-character text — the deviation from the original flow works, and would have failed as a raw mapping |
| Multi-choice → joined text | `StrategicGoals` = `Driver A1; Driver B1; Driver C2` |
| Double quotes survive | `Pilot a searchable "resource hub"` stored intact |
| Backslash survives | `C:\temp\notes` stored intact |
| Non-ASCII survives | `México`, em-dashes stored intact |
| Blank Number → empty, not 0 | all six rating columns empty on item 8 |
| Blank text/Choice → empty | `ChiefSupportDetails`, `PartnerContactRole`, impact fields all empty; no `N/A`, no `false` |
| Conditional branch populated | partner columns filled when `ExternalPartnerInvolved = Yes` |
| **OriginalSubmission populated** | filled on item 8; **empty on items 4–7** — the audit gap this project closed |
| Flow-layer preserved | `ReviewStatus = Not reviewed`, `ProcessingStatus = Processed`, `SourceForm`, `PromptVersion` identical to items 4–7 |
| AI layer unaffected | AISummary/Topics/KeyFindings/etc. populated as before |

## FINDING 1 — Choice value not in the live choice set (action required)

`ComplianceBoundaryAdaptation` stored:

> `I don't know (see compliance boundaries appendix)`

The live column's choices are exactly `Yes` / `No` / `I don't know`. The Form's
option text carries a parenthetical the SharePoint choice does not.

**SharePoint accepted it anyway** — REST does not enforce choice membership the
way the list UI does. So this fails silently and pollutes filtering, grouping
and any view built on that column.

Not a payload defect: the mapping passed through exactly what the Form gave it,
which is the specified behaviour. It is a **source/destination vocabulary
mismatch**. Options, in order of preference:

1. Edit the SharePoint choice to match the Form option text verbatim (safest —
   no mapping logic, no data loss).
2. Edit the Form option to `I don't know` to match SharePoint.
3. Add a normalization step mapping Form option text → SharePoint choice.
   Rejected unless 1 and 2 are both impossible: it introduces a hand-maintained
   lookup that will drift.

The same class of mismatch may exist on other Choice questions whose Form text
has not yet been compared with the column's choices — `ExternalPartnerInvolved`,
`LocalMarketImpact`, `ChiefSupportSecured`, `IBENImpact`,
`ProfessionalLearningImpact`, `AdditionalFactors` all matched on this
submission, but only the values actually submitted were exercised.

## FINDING 2 — Implementation Readiness Notice is an input after all

The labelled submission for response 8 shows:

> `16. Implementation Readiness Notice:` → `none`

Every one of the six reference responses had this blank, which was the basis
for the determination "display-only element, no SharePoint destination
required". That determination is **now falsified**: the question accepts input.

Consequence: its answer currently reaches SharePoint **only** inside
`OriginalSubmission`, with no dedicated column. Decision needed:

1. Accept — the value is preserved in the labelled text, and the question is
   arguably procedural rather than reportable; or
2. Add a `ReadinessNotice` multiline column and map key
   `r8d49a8bdd5e94aee82f332fcab962a51` (already evidenced from the flow).

Until decided, no data is lost, but the field is not queryable.

## NOT YET EXERCISED (re-test needed)

| Gap | Why | How to close |
|-----|-----|--------------|
| Line breaks in text | Submission A typed the literal words "then a line break" instead of pressing Enter | resubmit with real Enter keypresses in a long-text answer |
| Number columns **with values** | all ratings were left blank on submission A | submission with ratings filled (proven in sandbox, not yet live) |
| Multi-line + rating together | as above | one combined submission covers both |

## OBSERVED, NOT A DEFECT

`SubmittedDate` displays one hour later than the Form's submitDate (`2:00 PM`
vs `1:00:55 PM`). SharePoint stores UTC and renders in local/site timezone
(UTC+1 at this date). Items 4–7, created by the original flow, show the same
offset — behaviour is unchanged from the original flow, and the stored instant
is correct.

## Still to run

T5–T13, T15 — duplicate check (T7), resubmit idempotency (T13), concurrency
(T8), catch path (T12), and the re-tests listed above.
