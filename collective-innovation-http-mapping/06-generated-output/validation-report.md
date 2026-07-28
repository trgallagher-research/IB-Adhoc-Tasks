# Validation report — executable payload properties

Generated 2026-07-28 by `scripts/generate_artifacts.py`. Lists the source and normalization of every property in `compose-item-payload.json`, the exclusions, and the checks applied.

## Executable properties: 12

| Property (internal name) | SP type | Source | Forms conf. | SP conf. | Normalization kind |
|--------------------------|---------|--------|-------------|----------|--------------------|
| `Title` | Text | Required-by-convention Title, built by the flow. | Confirmed | Confirmed | title_from_description |
| `Respondent` | Text | Submitter email (Forms metadata, not an r-key). | Confirmed | Confirmed | responder |
| `SubmittedDate` | DateTime | Submission timestamp (Forms metadata). | Confirmed | Confirmed | submitdate |
| `OpportunityDescription` | Note | `r5caae6a11afb406a8e77e0b242fb4cab` | Confirmed | Confirmed | multiline |
| `AnticipatedLaunchDate` | DateTime (DateOnly) | `r8718cecca56b4ed692e9042452d04195` | Confirmed | Confirmed | date |
| `ImplementationTimeline` | Note | `rf8348c8485dd40b08c00e76f66a3d428` | Confirmed | Confirmed | multiline |
| `StrategicGoals` | Note | `r1da539bd1a494208849da87ee257c128` | Confirmed | Confirmed | multichoice_as_text |
| `StrategicAlignmentRationale` | Note | `rf9f8fa67e4fb4dfead61d31cba86aa7a` | Confirmed | Confirmed | multiline |
| `OperationalImpactExplanation` | Note | `r650d9f2a4d1f43e8938032a9cd60c658` | Confirmed | Confirmed | multiline |
| `ReputationalImpactExplanation` | Note | `r577a0e5e42554b6f8d82f7c24b8f183b` | Confirmed | Confirmed | multiline |
| `InternalStakeholdersConsulted` | Note | `rc12c559d019d4f9f9f8ed773c21c686f` | Confirmed | Confirmed | multiline |
| `InternalConsultationOutcomes` | Note | `r5d267e063680468b8f77617ee0269b60` | Confirmed | Confirmed | multiline |

## Excluded from executable output (by rule)

| ID | Mapping | Forms conf. | SP conf. | Note |
|----|---------|-------------|----------|------|
| M-RESPONSEID | Form response ID — duplicate-prevention key and audit refere | Probable | Confirmed |  |
| Q08 | Sponsor | Unresolved | Confirmed |  |
| Q11 | External Partner Involved? | Unresolved | Confirmed |  |
| Q12 | Organization Name | Unresolved | Confirmed |  |
| Q13 | Contact Person | Unresolved | Confirmed |  |
| Q14 | Role | Unresolved | Confirmed |  |
| Q17 | Does this suggested idea directly impact a local market? | Unresolved | Confirmed |  |
| Q18 | Local market(s) | Unresolved | Confirmed |  |
| Q19 | Is a compliance boundary adaptation required? | Unresolved | Confirmed |  |
| Q20 | If yes, is chief support secured? | Unresolved | Confirmed |  |
| Q21 | Specify chief support details | Unresolved | Confirmed |  |
| Q22 | Implementation Readiness Notice | Unresolved | Confirmed | no destination |
| Q23 | Strategic importance: This opportunity is strategically impo | Unresolved | Confirmed |  |
| Q24 | Comments & explanation of agreement score (Strategic importa | Unresolved | Confirmed |  |
| Q25 | Localized service offerings: This opportunity is directly co | Unresolved | Confirmed |  |
| Q26 | Comments & explanation of agreement score (Localized service | Unresolved | Confirmed |  |
| Q27 | Impact Description | Unresolved | Confirmed |  |
| Q28 | Data Evidence Supporting the Opportunity | Unresolved | Confirmed |  |
| Q29 | Expected Evidence for Impact | Unresolved | Confirmed |  |
| Q30 | Impacted Programme(s) | Unresolved | Confirmed |  |
| Q31 | Stakeholder Feedback Summary | Unresolved | Confirmed |  |
| Q32 | Financial Impact: This opportunity requires additional budge | Unresolved | Confirmed |  |
| Q33 | Comments & explanation of agreement score (Financial Impact) | Unresolved | Confirmed |  |
| Q34 | Operational Impact: This opportunity requires a substantial  | Probable | Confirmed |  |
| Q35 | Operational Impact: This opportunity requires operations (pe | Unresolved | Confirmed |  |
| Q37 | Reputational Impact: This opportunity creates reputational r | Probable | Confirmed |  |
| Q41 | Is there Network/Expert Community (IBEN) Impact to be consid | Unresolved | Confirmed |  |
| Q42 | If Yes, please explain the Network/Expert Community (IBEN) I | Unresolved | Confirmed |  |
| Q43 | Is there a Professional Learning Impact to be considered reg | Unresolved | Confirmed |  |
| Q44 | If Yes, please explain the Professional Learning Impact. | Unresolved | Confirmed |  |
| Q45 | Are there any additional factors to be considered regarding  | Unresolved | Confirmed |  |
| Q46 | If Yes, please explain the additional factors. | Unresolved | Confirmed |  |
| Q47 | Add any supporting files | Unresolved | Confirmed | no destination |

## Dummy-body simulation (production payload)

The payload semantics are mirrored in Python and run against the sanitized response-6 body and a synthetic edge-case body (quotes, apostrophes, backslash, line breaks, Unicode, emoji; every other answer blank). Asserted:

- valid JSON round-trip — all JSON-sensitive characters survive;
- blank answers become JSON `null` — never `''`, `0`, `false`, `'N/A'` or the string `'null'`;
- Number columns receive integers; DateTime columns ISO-shaped strings; Text/Note/Choice columns non-empty strings;
- `Title` is never null or empty (truncation at 255 with ellipsis; submitDate-based fallback).

Results: `06-generated-output/simulation-results.json`.

## Still requiring live verification in Power Automate

- the actual `Get response details` action name referenced by `outputs('Get_response_details')`;
- the trigger path `triggerOutputs()?['body/resourceData/responseId']` (blocks FormResponseID and the duplicate check — flow-export evidence EV-2);
- date-only acceptance by `AnticipatedLaunchDate` (schema says Format=DateOnly; T1/T3 confirm);
- end-to-end create via the copied flow (test matrix T0–T15).
