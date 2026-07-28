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

## Still to run

T0 (DLP probe), T1, T3, T5–T15 — all require the copied flow with the HTTP
actions; see `test-matrix.md`.
