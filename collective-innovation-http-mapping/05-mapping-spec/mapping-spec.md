# Mapping specification — Forms → SharePoint `Knowledge Submissions`

Generated 2026-07-28 by `scripts/build_reports.py` from `mapping-spec.json` (the machine-readable source of truth). Do not hand-edit; edit the spec builder and regenerate.

## Confidence states

- **Existing** — Preserved from a working flow mapping (requires 04-existing-flow evidence).
- **Confirmed** — Supported by authoritative structural, distinctive dummy-test, or unique label-match evidence.
- **Probable** — Strongly suggested but unproved; requires human resolution; NEVER executable.
- **Unresolved** — Missing, ambiguous, obsolete, or contradictory.

**Executability rule:** executable == true requires forms side AND SharePoint side each Existing/Confirmed, with every expression source evidenced. Enforced by scripts/validate_spec.py and scripts/generate_artifacts.py.

## Evidence base

- `forms_excel`: 01-forms-excel/sanitized/Innovation-Intake-Form-responses-reference.xlsx (6 dummy responses)
- `get_response_details`: 02-get-response-details/sanitized/get-response-details-response-6.body.json (dummy response 6)
- `sharepoint_schema`: 03-sharepoint-schema/sanitized/knowledge-submissions-schema.json (live export 2026-07-28)
- `existing_flow`: ABSENT — 04-existing-flow/ empty

The SharePoint side is **Confirmed for every mapping** from the live schema export of 2026-07-28 (unique label correspondence, types, required flags and choice sets). Executability now turns on the Forms side and on expression-source verification.

## Forms metadata mappings

| ID | Source expression | Forms conf. | SharePoint | Normalization |
|----|-------------------|-------------|------------|---------------|
| M-TITLE | `Opportunity Description key (Q07) with a submitDate-based fallback` | Confirmed | `Title` (Text, Confirmed) | Opportunity Description truncated to 255 chars with ellipsis; if blank, 'Form submission <submitDate>'. Never null, never ''. |
| M-RESPONDER | `body('Get_response_details')?['responder']` | Confirmed | `Respondent` (Text, Confirmed) | Plain string into the Text column. (Not a Person field — no claims resolution needed.) |
| M-SUBMITDATE | `body('Get_response_details')?['submitDate']` | Confirmed | `SubmittedDate` (DateTime, Confirmed) | concat(formatDateTime(value, 'yyyy-MM-ddTHH:mm:ss'), 'Z') — source is UTC. Never ''. |
| M-RESPONSEID | `triggerOutputs()?['body/resourceData/responseId']` | Probable | `FormResponseID` (Text, Confirmed) | string(response ID) into the Text column. Duplicate-check filter: FormResponseID eq '<id>'. |

## Question mappings (Excel columns 7–47)

| ID | Question label | Answer shape | Forms response key | Forms conf. | SharePoint | Executable |
|----|----------------|--------------|--------------------|-------------|------------|------------|
| Q07 | Opportunity Description | free text | `r5caae6a11afb406a8e77e0b242fb4cab` | Confirmed | `OpportunityDescription` (Note, Confirmed) | yes |
| Q08 | Sponsor | free text | — | Unresolved | `Sponsor` (Text, Confirmed) | no |
| Q09 | Anticipated launch date | date | `r8718cecca56b4ed692e9042452d04195` | Confirmed | `AnticipatedLaunchDate` (DateTime (DateOnly), Confirmed) | yes |
| Q10 | Anticipated timeline for implementation | free text | `rf8348c8485dd40b08c00e76f66a3d428` | Confirmed | `ImplementationTimeline` (Note, Confirmed) | yes |
| Q11 | External Partner Involved? | Yes/No | candidates: 5 | Unresolved | `ExternalPartnerInvolved` (Choice, Confirmed) | no |
| Q12 | Organization Name | free text | — | Unresolved | `PartnerOrganisation` (Text, Confirmed) | no |
| Q13 | Contact Person | free text | — | Unresolved | `PartnerContactPerson` (Text, Confirmed) | no |
| Q14 | Role | free text | — | Unresolved | `PartnerContactRole` (Text, Confirmed) | no |
| Q15 | Strategic Goals | multi-choice | `r1da539bd1a494208849da87ee257c128` | Confirmed | `StrategicGoals` (Note, Confirmed) | yes |
| Q16 | Strategic Alignment Rationale | free text | `rf9f8fa67e4fb4dfead61d31cba86aa7a` | Confirmed | `StrategicAlignmentRationale` (Note, Confirmed) | yes |
| Q17 | Does this suggested idea directly impact a local market? | Yes/No | candidates: 5 | Unresolved | `LocalMarketImpact` (Choice, Confirmed) | no |
| Q18 | Local market(s) | free text | — | Unresolved | `LocalMarketDetails` (Note, Confirmed) | no |
| Q19 | Is a compliance boundary adaptation required? | Yes/No | — | Unresolved | `ComplianceBoundaryAdaptation` (Choice, Confirmed) | no |
| Q20 | If yes, is chief support secured? | Yes/No | — | Unresolved | `ChiefSupportSecured` (Choice, Confirmed) | no |
| Q21 | Specify chief support details | free text | — | Unresolved | `ChiefSupportDetails` (Note, Confirmed) | no |
| Q22 | Implementation Readiness Notice | display-only notice (no input observed) | — | Unresolved | Unresolved — no schema evidence | no |
| Q23 | Strategic importance: This opportunity is strategically important to t | rating 1-5 | — | Unresolved | `StrategicImportanceScore` (Number, Confirmed) | no |
| Q24 | Comments & explanation of agreement score (Strategic importance) | free text | — | Unresolved | `StrategicImportanceExplanation` (Note, Confirmed) | no |
| Q25 | Localized service offerings: This opportunity is directly connected to | rating 1-5 | — | Unresolved | `LocalizedServiceOfferingScore` (Number, Confirmed) | no |
| Q26 | Comments & explanation of agreement score (Localized service offerings | free text | — | Unresolved | `LocalizedServiceOfferingExplanat` (Note, Confirmed) | no |
| Q27 | Impact Description | free text | — | Unresolved | `ImpactDescription` (Note, Confirmed) | no |
| Q28 | Data Evidence Supporting the Opportunity | free text | — | Unresolved | `DataEvidence` (Note, Confirmed) | no |
| Q29 | Expected Evidence for Impact | free text | — | Unresolved | `ExpectedEvidence` (Note, Confirmed) | no |
| Q30 | Impacted Programme(s) | multi-choice | — | Unresolved | `ImpactedProgrammes` (Note, Confirmed) | no |
| Q31 | Stakeholder Feedback Summary | free text | — | Unresolved | `StakeholderFeedbackSummary` (Note, Confirmed) | no |
| Q32 | Financial Impact: This opportunity requires additional budget to be pi | rating 1-5 | candidates: 2 | Unresolved | `FinancialImpactScore` (Number, Confirmed) | no |
| Q33 | Comments & explanation of agreement score (Financial Impact) | free text | — | Unresolved | `FinancialImpactExplanation` (Note, Confirmed) | no |
| Q34 | Operational Impact: This opportunity requires a substantial volume of  | rating 1-5 | `rca68d3a0ad2b45c397fd0523414426b5` | Probable | `OperationalSupportScore` (Number, Confirmed) | no |
| Q35 | Operational Impact: This opportunity requires operations (people, proc | rating 1-5 | candidates: 2 | Unresolved | `OperationalChangesScore` (Number, Confirmed) | no |
| Q36 | Comments & explanation of agreement score (Operational Impact) | free text | `r650d9f2a4d1f43e8938032a9cd60c658` | Confirmed | `OperationalImpactExplanation` (Note, Confirmed) | yes |
| Q37 | Reputational Impact: This opportunity creates reputational risk for th | rating 1-5 | `r1903e1b8394140d19377b15fc81edd65` | Probable | `ReputationalImpactScore` (Number, Confirmed) | no |
| Q38 | Comments & explanation of agreement score (Reputational Impact) | free text | `r577a0e5e42554b6f8d82f7c24b8f183b` | Confirmed | `ReputationalImpactExplanation` (Note, Confirmed) | yes |
| Q39 | Internal Stakeholders Consulted | free text | `rc12c559d019d4f9f9f8ed773c21c686f` | Confirmed | `InternalStakeholdersConsulted` (Note, Confirmed) | yes |
| Q40 | Internal Consultation Context & Outcomes | free text | `r5d267e063680468b8f77617ee0269b60` | Confirmed | `InternalConsultationOutcomes` (Note, Confirmed) | yes |
| Q41 | Is there Network/Expert Community (IBEN) Impact to be considered regar | Yes/No | candidates: 5 | Unresolved | `IBENImpact` (Choice, Confirmed) | no |
| Q42 | If Yes, please explain the Network/Expert Community (IBEN) Impact. | free text | — | Unresolved | `IBENImpactDescription` (Note, Confirmed) | no |
| Q43 | Is there a Professional Learning Impact to be considered regarding thi | Yes/No | candidates: 5 | Unresolved | `ProfessionalLearningImpact` (Choice, Confirmed) | no |
| Q44 | If Yes, please explain the Professional Learning Impact. | free text | — | Unresolved | `ProfessionalLearningImpactDescri` (Note, Confirmed) | no |
| Q45 | Are there any additional factors to be considered regarding this oppor | Yes/No | candidates: 5 | Unresolved | `AdditionalFactors` (Choice, Confirmed) | no |
| Q46 | If Yes, please explain the additional factors. | free text | — | Unresolved | `AdditionalFactorsDescription` (Note, Confirmed) | no |
| Q47 | Add any supporting files | file upload | — | Unresolved | Unresolved — no schema evidence | no |

## Evidence detail (Confirmed and Probable rows)

### M-TITLE — Required-by-convention Title, built by the flow.

- Confidence: **Confirmed**
- Evidence: Built solely from Confirmed sources: the Q07 key and the structural submitDate property. (Live schema shows Title is not actually Required on this list; it is populated anyway for usable views. Fallback deliberately avoids the trigger response-ID path, which is unverified until the flow export lands.)
- Normalization: Opportunity Description truncated to 255 chars with ellipsis; if blank, 'Form submission <submitDate>'. Never null, never ''.
- Note: Linked-title view column displays as 'Opportunity'.

### M-RESPONDER — Submitter email (Forms metadata, not an r-key).

- Confidence: **Confirmed**
- Evidence: Structural property of the Get-response-details body; observed populated in the response-6 capture and corresponding to the Excel 'Email' metadata column.
- Normalization: Plain string into the Text column. (Not a Person field — no claims resolution needed.)
- Note: Excel 'Name' column has no Get-response-details equivalent; no destination exists for it in the live schema either.

### M-SUBMITDATE — Submission timestamp (Forms metadata).

- Confidence: **Confirmed**
- Evidence: Structural property of the body. Observed 'M/d/yyyy h:mm:ss AM/PM' in UTC: the response-6 capture shows 3:23:34 PM against the Excel completion time 17:23:34 (tenant-local, UTC+2 at capture).
- Normalization: concat(formatDateTime(value, 'yyyy-MM-ddTHH:mm:ss'), 'Z') — source is UTC. Never ''.

### M-RESPONSEID — Form response ID — duplicate-prevention key and audit reference.

- Confidence: **Probable**
- Evidence: Documented output path of the 'When a new response is submitted' trigger; the standard pattern, but NOT yet verified against this flow's export — so this mapping stays out of executable output despite its destination being Confirmed. Verify via 04-existing-flow evidence (trigger.json / get-response-details.json).
- Normalization: string(response ID) into the Text column. Duplicate-check filter: FormResponseID eq '<id>'.

### Q07 — Opportunity Description

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Pilot a searchable online resource hub for schools.' matches exactly one column and exactly one key within the response.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q09 — Anticipated launch date

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: only ISO-date value in the body ('2026-12-01') matches the only date answer in the row (Excel renders it as 2026-12-01 00:00:00).
- Normalization: DateTime (DateOnly) destination: send the key's 'yyyy-MM-dd' string as-is. Blank -> JSON null. NEVER send ''.

### Q10 — Anticipated timeline for implementation

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Build in October, test in November, and pilot in December 2026.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q15 — Strategic Goals

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: only JSON-array-serialized value in the body ('["Driver A1"]') matches the multi-choice serialization of the row's Strategic Goals value ('Driver A1;'). The only other multi-choice question (Impacted Programme(s)) is blank in this response.
- Normalization: Value arrives as a JSON-array *string* (e.g. '["A","B"]'). Destination is CONFIRMED multiline text (Note): join(json(value), '; '). Blank -> JSON null.
- Note: Destination CONFIRMED as multiline text (Note), not MultiChoice — '; '-joined text serialization applies.

### Q16 — Strategic Alignment Rationale

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: deliberate marker value — plain string 'Driver A1' exactly matches the rationale column, and is structurally distinct from the JSON-array form carried by the Strategic Goals key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q34 — Operational Impact: This opportunity requires a substantial volume of support from the IB to ensure it does not compromise our standards and quality.

- Confidence: **Probable**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: value '2' is unique within the response's four-rating multiset {1,1,2,3} and the row's answered ratings form the same multiset, with '2' on this column. Capped at Probable because the brief rules 1-5 values non-distinctive. Resolve with a distinct-permutation test submission.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q36 — Comments & explanation of agreement score (Operational Impact)

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Limited support is expected and no operational changes are planned.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q37 — Reputational Impact: This opportunity creates reputational risk for the organization.

- Confidence: **Probable**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: value '3' is unique within the response's four-rating multiset; same reasoning and same Probable cap as the Operational-support rating. Resolve with a distinct-permutation test submission.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q38 — Comments & explanation of agreement score (Reputational Impact)

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'The reputational risk is currently uncertain.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q39 — Internal Stakeholders Consulted

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Professional Learning team.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q40 — Internal Consultation Context & Outcomes

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'The team supported testing a small pilot.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

## Backend fields — not Form questions (internal names evidenced by live schema)

| Fields | Layer | Behaviour at item creation |
|--------|-------|----------------------------|
| `AISummary`, `Topics`, `KeyFindings`, `Examples`, `OpenQuestions`, `DifferentPerspectives`, `ClaimsToVerify`, `RelatedKnowledge`, `FullAIOutput` | AI-generated analysis | Preserve the existing flow's AI/Select mappings once the flow export is in 04-existing-flow/; never source from raw Forms answers. |
| `HumanReviewRequired`, `HumanReviewReason`, `ReviewStatus` | Human review and governance | Not in the raw-answer payload. ReviewStatus default 'Not reviewed' is CONFIRMED by the live schema (column default) — omitting it from the payload applies it. HumanReviewRequired defaults to No (0); whether the flow's AI branch overrides it awaits the flow export. |
| `ProcessingStatus`, `ProcessedDate`, `ProcessingError`, `PromptVersion`, `SourceForm` | Processing and audit metadata | ProcessingStatus choices Received/Processing/Processed/Failed with column default 'Processed' (confirmed); SourceForm defaults to the form name; PromptVersion defaults '1.0'. Whether the flow sets these explicitly awaits the flow export — until then the payload omits them and defaults apply. |
| `OriginalSubmission` | Processing and audit metadata | Destination CONFIRMED (Note). Source expression is the existing labelled-submission construction — preserved verbatim once the flow export is available; absent from the payload until then. |
| `FormResponseID`, `SubmittedDate`, `Respondent` | Processing and audit metadata | All three CONFIRMED to exist. SubmittedDate/Respondent are executable now; FormResponseID awaits trigger-expression verification (see M-RESPONSEID). |
