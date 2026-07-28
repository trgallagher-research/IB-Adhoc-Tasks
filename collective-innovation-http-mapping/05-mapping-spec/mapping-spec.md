# Mapping specification — Forms → SharePoint `Knowledge Submissions`

Generated 2026-07-28 by `scripts/build_reports.py` from `mapping-spec.json` (the machine-readable source of truth). Do not hand-edit; edit the spec builder and regenerate.

## Confidence states

- **Existing** — Preserved from a working flow mapping (04-existing-flow evidence).
- **Confirmed** — Supported by authoritative structural, distinctive dummy-test, or unique label-match evidence.
- **Probable** — Strongly suggested but unproved; requires human resolution; NEVER executable.
- **Unresolved** — Missing, ambiguous, obsolete, or contradictory.

**Executability rule:** executable == true requires forms side AND SharePoint side each Existing/Confirmed, with every expression source evidenced. Enforced by scripts/validate_spec.py and scripts/generate_artifacts.py.

## Evidence base

- `forms_excel`: 01-forms-excel/sanitized/Innovation-Intake-Form-responses-reference.xlsx (6 dummy responses)
- `get_response_details`: 02-get-response-details/sanitized/get-response-details-response-6.body.json (dummy response 6)
- `sharepoint_schema`: 03-sharepoint-schema/sanitized/knowledge-submissions-schema.json (live export 2026-07-28)
- `existing_flow`: 04-existing-flow/sanitized/ (Peek-code captures 2026-07-28: trigger, Get response details, Run a prompt incl. labelled-submission construction, 3 of 8 Select actions, Create item)

**Cross-validation:** The flow's label->key pairings agree with ALL prior dummy-test evidence: 9 Confirmed matches, both Probables resolved as predicted, the five-way 'No' set and two-way '1' pair resolve bijectively. 41 flow keys + 7 permanently-blank surplus keys = 48 observed keys exactly.

## Forms metadata mappings

| ID | Source | Conf. | SharePoint | Executable |
|----|--------|-------|------------|------------|
| M-TITLE | Opportunity Description key (Q07), truncated, with response-ID fallback | Existing | `Title` (Text, Confirmed) | yes |
| M-RESPONDER | body('Get_response_details')?['responder'] | Existing | `Respondent` (Text, Confirmed) | yes |
| M-SUBMITDATE | body('Get_response_details')?['submitDate'] | Existing | `SubmittedDate` (DateTime, Confirmed) | yes |
| M-RESPONSEID | triggerOutputs()?['body/resourceData/responseId'] | Existing | `FormResponseID` (Text, Confirmed) | yes |
| M-ORIGINALSUBMISSION | outputs('Compose_labelled_submission') — the existing labelled-submission text,  | Existing | `OriginalSubmission` (Note, Confirmed) | yes |

## Question mappings (Excel columns 7–47) — all keys `Existing` from the flow's labelled construction

| ID | Question label | Answer shape | Forms response key | Conf. | SharePoint | Executable |
|----|----------------|--------------|--------------------|-------|------------|------------|
| Q07 | Opportunity Description | free text | `r5caae6a11afb406a8e77e0b242fb4cab` | Existing | `OpportunityDescription` (Note, Confirmed) | yes |
| Q08 | Sponsor | free text | `r8140da6e45c84dbcab391c05346d9b16` | Existing | `Sponsor` (Text, Confirmed) | yes |
| Q09 | Anticipated launch date | date | `r8718cecca56b4ed692e9042452d04195` | Existing | `AnticipatedLaunchDate` (DateTime (DateOnly), Confirmed) | yes |
| Q10 | Anticipated timeline for implementation | free text | `rf8348c8485dd40b08c00e76f66a3d428` | Existing | `ImplementationTimeline` (Note, Confirmed) | yes |
| Q11 | External Partner Involved? | Yes/No | `r587705b554a5436aa6663834b1582469` | Existing | `ExternalPartnerInvolved` (Choice, Confirmed) | yes |
| Q12 | Organization Name | free text | `rf7cbe61f26ab41cfa28f0b2a009e9d7c` | Existing | `PartnerOrganisation` (Text, Confirmed) | yes |
| Q13 | Contact Person | free text | `r072e0a054db54072b75c27d3d8e90140` | Existing | `PartnerContactPerson` (Text, Confirmed) | yes |
| Q14 | Role | free text | `r685fa8b221f64f9188951dfb6fb629ec` | Existing | `PartnerContactRole` (Text, Confirmed) | yes |
| Q15 | Strategic Goals | multi-choice | `r1da539bd1a494208849da87ee257c128` | Existing | `StrategicGoals` (Note, Confirmed) | yes |
| Q16 | Strategic Alignment Rationale | free text | `rf9f8fa67e4fb4dfead61d31cba86aa7a` | Existing | `StrategicAlignmentRationale` (Note, Confirmed) | yes |
| Q17 | Does this suggested idea directly impact a local market? | Yes/No | `r516051da52cf4166a478cd83a6e15291` | Existing | `LocalMarketImpact` (Choice, Confirmed) | yes |
| Q18 | Local market(s) | free text | `rf81976cae03249ef86d0d299bf126aac` | Existing | `LocalMarketDetails` (Note, Confirmed) | yes |
| Q19 | Is a compliance boundary adaptation required? | Yes/No | `r9ec31f96e7b34fb791c734433bb022a3` | Existing | `ComplianceBoundaryAdaptation` (Choice, Confirmed) | yes |
| Q20 | If yes, is chief support secured? | Yes/No | `rf0bccf6e481343d1823057965c3271ea` | Existing | `ChiefSupportSecured` (Choice, Confirmed) | yes |
| Q21 | Specify chief support details | free text | `r0b456ff26ee24c11a9503908ffea1b53` | Existing | `ChiefSupportDetails` (Note, Confirmed) | yes |
| Q22 | Implementation Readiness Notice | display-only notice (no input observed) | `r8d49a8bdd5e94aee82f332fcab962a51` | Existing | — (no destination, Confirmed) | no |
| Q23 | Strategic importance: This opportunity is strategically important to t | rating 1-5 | `rfb959d52f2494d1b92e07856edeee015` | Existing | `StrategicImportanceScore` (Number, Confirmed) | yes |
| Q24 | Comments & explanation of agreement score (Strategic importance) | free text | `re8d27932c227466996dbc77f67f71faa` | Existing | `StrategicImportanceExplanation` (Note, Confirmed) | yes |
| Q25 | Localized service offerings: This opportunity is directly connected to | rating 1-5 | `r809645c3237a4bb4969b8082026cb3cc` | Existing | `LocalizedServiceOfferingScore` (Number, Confirmed) | yes |
| Q26 | Comments & explanation of agreement score (Localized service offerings | free text | `r3e390836da294861a927ce63c8d0f2c6` | Existing | `LocalizedServiceOfferingExplanat` (Note, Confirmed) | yes |
| Q27 | Impact Description | free text | `rf703806487ab4148994d2fd2edb79941` | Existing | `ImpactDescription` (Note, Confirmed) | yes |
| Q28 | Data Evidence Supporting the Opportunity | free text | `r75f4515f78d946ac8a4274c151307c3e` | Existing | `DataEvidence` (Note, Confirmed) | yes |
| Q29 | Expected Evidence for Impact | free text | `rbb5f5979ba74480fba871dbaaeb381e9` | Existing | `ExpectedEvidence` (Note, Confirmed) | yes |
| Q30 | Impacted Programme(s) | multi-choice | `rd668321450304780986d33d7e6f474b9` | Existing | `ImpactedProgrammes` (Note, Confirmed) | yes |
| Q31 | Stakeholder Feedback Summary | free text | `rba40cea72cef44df9c70637d7473d033` | Existing | `StakeholderFeedbackSummary` (Note, Confirmed) | yes |
| Q32 | Financial Impact: This opportunity requires additional budget to be pi | rating 1-5 | `r90c6dc19b575459fa68b7a65b23a9a06` | Existing | `FinancialImpactScore` (Number, Confirmed) | yes |
| Q33 | Comments & explanation of agreement score (Financial Impact) | free text | `ra89a8e77654b43a6af62ff1247df9f8f` | Existing | `FinancialImpactExplanation` (Note, Confirmed) | yes |
| Q34 | Operational Impact: This opportunity requires a substantial volume of  | rating 1-5 | `rca68d3a0ad2b45c397fd0523414426b5` | Existing | `OperationalSupportScore` (Number, Confirmed) | yes |
| Q35 | Operational Impact: This opportunity requires operations (people, proc | rating 1-5 | `re95a3bb4ed594260b8745180ba8d56a7` | Existing | `OperationalChangesScore` (Number, Confirmed) | yes |
| Q36 | Comments & explanation of agreement score (Operational Impact) | free text | `r650d9f2a4d1f43e8938032a9cd60c658` | Existing | `OperationalImpactExplanation` (Note, Confirmed) | yes |
| Q37 | Reputational Impact: This opportunity creates reputational risk for th | rating 1-5 | `r1903e1b8394140d19377b15fc81edd65` | Existing | `ReputationalImpactScore` (Number, Confirmed) | yes |
| Q38 | Comments & explanation of agreement score (Reputational Impact) | free text | `r577a0e5e42554b6f8d82f7c24b8f183b` | Existing | `ReputationalImpactExplanation` (Note, Confirmed) | yes |
| Q39 | Internal Stakeholders Consulted | free text | `rc12c559d019d4f9f9f8ed773c21c686f` | Existing | `InternalStakeholdersConsulted` (Note, Confirmed) | yes |
| Q40 | Internal Consultation Context & Outcomes | free text | `r5d267e063680468b8f77617ee0269b60` | Existing | `InternalConsultationOutcomes` (Note, Confirmed) | yes |
| Q41 | Is there Network/Expert Community (IBEN) Impact to be considered regar | Yes/No | `r5f267e3e119041469c62a472d832324f` | Existing | `IBENImpact` (Choice, Confirmed) | yes |
| Q42 | If Yes, please explain the Network/Expert Community (IBEN) Impact. | free text | `r011318f6666745c891df6ed52af394b0` | Existing | `IBENImpactDescription` (Note, Confirmed) | yes |
| Q43 | Is there a Professional Learning Impact to be considered regarding thi | Yes/No | `rf76887b82f1f4414a41f5e65ecef7cbd` | Existing | `ProfessionalLearningImpact` (Choice, Confirmed) | yes |
| Q44 | If Yes, please explain the Professional Learning Impact. | free text | `r074e7a91d52747519a8fe0e9af68e7dd` | Existing | `ProfessionalLearningImpactDescri` (Note, Confirmed) | yes |
| Q45 | Are there any additional factors to be considered regarding this oppor | Yes/No | `rbc83faed4a274e0fb254a5c4c21edd73` | Existing | `AdditionalFactors` (Choice, Confirmed) | yes |
| Q46 | If Yes, please explain the additional factors. | free text | `r90a4a472716942dfa4b9d5de21931774` | Existing | `AdditionalFactorsDescription` (Note, Confirmed) | yes |
| Q47 | Add any supporting files | file upload | `r7ba397b729054a109e0b046c38744e73` | Existing | — (no destination, Confirmed) | no |

## Flow-layer mappings — preserved verbatim from the existing Create item

| Property | Source |
|----------|--------|
| `SourceForm` | constant `"Innovation Intake Form (Knowledge-Bank)"` |
| `AISummary` | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/summ` |
| `Topics` | `join(body('Select_Topics'), decodeUriComponent('%0A'))` |
| `KeyFindings` | `join(body('Select_Key_Findings'), decodeUriComponent('%0A'))` |
| `Examples` | `join(body('Select_Examples'), decodeUriComponent('%0A'))` |
| `OpenQuestions` | `join(body('Select_Open_Questions'), decodeUriComponent('%0A'))` |
| `DifferentPerspectives` | `join(body('Select_Different_Perspectives'), decodeUriComponent('%0A'))` |
| `ClaimsToVerify` | `join(body('Select_Claims_To_Verify'), decodeUriComponent('%0A'))` |
| `RelatedKnowledge` | `join(body('Select_Related_Knowledge'), decodeUriComponent('%0A'))` |
| `HumanReviewRequired` | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/huma` |
| `HumanReviewReason` | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/huma` |
| `ReviewStatus` | constant `"Not reviewed"` |
| `FullAIOutput` | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text']` |
| `ProcessingStatus` | constant `"Processed"` |
| `ProcessedDate` | `utcNow()` |
| `PromptVersion` | constant `"Knowledge Submission Analyser v1\n"` |
| `ContentTypeId` | constant `"0x01002470676DA4BBF5468468EDBF918DE47C0082A052FA62248A4A84337267D7DD930B"` |

## Evidence detail

### M-TITLE — Title (linked-title displays as 'Opportunity').

- Confidence: **Existing**
- Evidence: Existing flow maps Title = raw Q07 key (create-item.json). DELIBERATE DEVIATION in the replacement: truncate to 255 chars with ellipsis (the existing raw mapping fails at runtime for descriptions over the Text-255 limit) and fall back to 'Form response <id>' when blank. VERIFIED in the flow captures: used as Get response details' response_id parameter, in the labelled-submission text, and in Create item's FormResponseID parameter (04-existing-flow/sanitized/).
- Normalization: Truncate at 255 with '...'; blank -> 'Form response <id>'. Never null, never ''.

### M-RESPONDER — Submitter email (Forms metadata).

- Confidence: **Existing**
- Evidence: Existing flow maps Respondent = responder verbatim (create-item.json); also a structural body property corroborated by the response-6 capture.
- Normalization: Plain string into the Text column (verbatim, as in the existing flow).

### M-SUBMITDATE — Submission timestamp (Forms metadata).

- Confidence: **Existing**
- Evidence: Existing flow posts the raw 'M/d/yyyy h:mm:ss AM/PM' UTC string to SubmittedDate (create-item.json). DELIBERATE DEVIATION in the replacement: normalize to ISO 8601 UTC (same instant, explicit format) because the REST endpoint is stricter than the connector about date parsing.
- Normalization: concat(formatDateTime(value, 'yyyy-MM-ddTHH:mm:ss'), 'Z') — source is UTC. Never ''.

### M-RESPONSEID — Form response ID — duplicate-prevention key and audit reference.

- Confidence: **Existing**
- Evidence: VERIFIED in the flow captures: used as Get response details' response_id parameter, in the labelled-submission text, and in Create item's FormResponseID parameter (04-existing-flow/sanitized/).
- Normalization: string(response ID) into the Text column. Duplicate-check filter: FormResponseID eq '<id>'.

### M-ORIGINALSUBMISSION — Full labelled raw submission (audit layer).

- Confidence: **Existing**
- Evidence: The labelled-submission construction is captured verbatim in 04-existing-flow/sanitized/run-a-prompt.json (SubmissionText). The existing flow builds it inline in the AI action and does NOT store it; the replacement moves it into a Compose_labelled_submission action referenced by BOTH the AI prompt and this property, closing the audit gap without changing the text.
- Normalization: Verbatim template output (generated to 06-generated-output/compose-labelled-submission.txt).

### Q07 — Opportunity Description

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Opportunity Description'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q08 — Sponsor

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Sponsor').
- Normalization: Trim; blank answer -> JSON null. Pass the value as a JSON object member (never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.

### Q09 — Anticipated launch date

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Anticipated launch date'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: DateTime (DateOnly) destination: send the key's 'yyyy-MM-dd' string as-is. Blank -> JSON null. NEVER send ''.

### Q10 — Anticipated timeline for implementation

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Anticipated timeline for implementation'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q11 — External Partner Involved?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('External Partner Involved?'). Consistent with the prior five-way 'No' candidate set from response-6 dummy-test correlation (bijective resolution).
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q12 — Organization Name

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Organization Name').
- Normalization: Trim; blank answer -> JSON null. Pass the value as a JSON object member (never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.

### Q13 — Contact Person

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Contact Person').
- Normalization: Trim; blank answer -> JSON null. Pass the value as a JSON object member (never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.

### Q14 — Role

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Role').
- Normalization: Trim; blank answer -> JSON null. Pass the value as a JSON object member (never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.

### Q15 — Strategic Goals

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Strategic Goals'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Value arrives as a JSON-array *string* (e.g. '["A","B"]'). Destination is CONFIRMED multiline text (Note): join(json(value), '; '). Blank -> JSON null.
- Note: Destination CONFIRMED as multiline text (Note), not MultiChoice — '; '-joined text serialization applies.

### Q16 — Strategic Alignment Rationale

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Strategic Alignment Rationale'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q17 — Does this suggested idea directly impact a local market?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Does this suggested idea directly impact a local market?'). Consistent with the prior five-way 'No' candidate set from response-6 dummy-test correlation (bijective resolution).
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q18 — Local market(s)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Local market(s)').
- Normalization: Trim; blank answer -> JSON null. Pass the value as a JSON object member (never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.

### Q19 — Is a compliance boundary adaptation required?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Is a compliance boundary adaptation required?').
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.
- Note: Live choice set includes a third option "I don't know" — pass-through, never coerce to Yes/No.

### Q20 — If yes, is chief support secured?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('If yes, is chief support secured?').
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q21 — Specify chief support details

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Specify chief support details').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q22 — Implementation Readiness Notice

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Implementation Readiness Notice').
- Normalization: No destination (confirmed); nothing sent per-column.

### Q23 — Strategic importance: This opportunity is strategically important to the market, including through its potential to support significant programme acquisition and/or reduce significant retention risks.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Strategic importance: This opportunity is strategically impo').
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q24 — Comments & explanation of agreement score (Strategic importance)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Comments & explanation of agreement score (Strategic importa').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q25 — Localized service offerings: This opportunity is directly connected to local ways of working (for example, language, district set PD schedule etc.) and would support the IB in being seen as a genu...

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Localized service offerings: This opportunity is directly co').
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q26 — Comments & explanation of agreement score (Localized service offerings)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Comments & explanation of agreement score (Localized service').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q27 — Impact Description

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Impact Description').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q28 — Data Evidence Supporting the Opportunity

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Data Evidence Supporting the Opportunity').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q29 — Expected Evidence for Impact

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Expected Evidence for Impact').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q30 — Impacted Programme(s)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Impacted Programme(s)').
- Normalization: Value arrives as a JSON-array *string* (e.g. '["A","B"]'). Destination is CONFIRMED multiline text (Note): join(json(value), '; '). Blank -> JSON null.
- Note: Destination CONFIRMED as multiline text (Note), not MultiChoice — '; '-joined text serialization applies.

### Q31 — Stakeholder Feedback Summary

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Stakeholder Feedback Summary').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q32 — Financial Impact: This opportunity requires additional budget to be piloted or taken to market.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Financial Impact: This opportunity requires additional budge'). Consistent with the prior two-way '1' candidate pair from response-6 dummy-test correlation.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q33 — Comments & explanation of agreement score (Financial Impact)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Comments & explanation of agreement score (Financial Impact)').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q34 — Operational Impact: This opportunity requires a substantial volume of support from the IB to ensure it does not compromise our standards and quality.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Operational Impact: This opportunity requires a substantial '). Resolves the prior Probable from response-6 dummy-test correlation (multiset-unique rating) — consistent.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q35 — Operational Impact: This opportunity requires operations (people, process, or system) changes.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Operational Impact: This opportunity requires operations (pe'). Consistent with the prior two-way '1' candidate pair from response-6 dummy-test correlation.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q36 — Comments & explanation of agreement score (Operational Impact)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Comments & explanation of agreement score (Operational Impac'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q37 — Reputational Impact: This opportunity creates reputational risk for the organization.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Reputational Impact: This opportunity creates reputational r'). Resolves the prior Probable from response-6 dummy-test correlation (multiset-unique rating) — consistent.
- Normalization: Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q38 — Comments & explanation of agreement score (Reputational Impact)

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Comments & explanation of agreement score (Reputational Impa'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q39 — Internal Stakeholders Consulted

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Internal Stakeholders Consulted'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q40 — Internal Consultation Context & Outcomes

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Internal Consultation Context & Outcomes'). Independently CORROBORATED by response-6 dummy-test correlation (distinctive dummy value).
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q41 — Is there Network/Expert Community (IBEN) Impact to be considered regarding this opportunity?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Is there Network/Expert Community (IBEN) Impact to be consid'). Consistent with the prior five-way 'No' candidate set from response-6 dummy-test correlation (bijective resolution).
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q42 — If Yes, please explain the Network/Expert Community (IBEN) Impact.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('If Yes, please explain the Network/Expert Community (IBEN) I').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q43 — Is there a Professional Learning Impact to be considered regarding this opportunity?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Is there a Professional Learning Impact to be considered reg').
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q44 — If Yes, please explain the Professional Learning Impact.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('If Yes, please explain the Professional Learning Impact.').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q45 — Are there any additional factors to be considered regarding this opportunity?

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Are there any additional factors to be considered regarding ').
- Normalization: Choice destination (choices verified in live schema): pass the answer string through verbatim ('Yes'/'No', and for ComplianceBoundaryAdaptation also "I don't know"). Blank -> JSON null; never invent 'N/A' or false.

### Q46 — If Yes, please explain the additional factors.

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('If Yes, please explain the additional factors.').
- Normalization: Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.

### Q47 — Add any supporting files

- Confidence: **Existing**
- Evidence: Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the labelled-submission construction explicitly pairs this question label with this key ('Add any supporting files').
- Normalization: No per-column destination (confirmed). Phase 1: excluded from the payload; raw string remains inside OriginalSubmission.

## Backend fields — not Form questions (internal names evidenced by live schema)

| Fields | Layer | Behaviour at item creation |
|--------|-------|----------------------------|
| `AISummary`, `Topics`, `KeyFindings`, `Examples`, `OpenQuestions`, `DifferentPerspectives`, `ClaimsToVerify`, `RelatedKnowledge`, `FullAIOutput` | AI-generated analysis | Preserved verbatim from the existing Create item (see flow_layer_mappings); sourced from Run_a_prompt / Select actions, never from raw Forms answers. |
| `HumanReviewRequired`, `HumanReviewReason`, `ReviewStatus` | Human review and governance | HumanReview* come from the AI output (existing mapping, preserved). ReviewStatus is explicitly set to 'Not reviewed' by the existing flow, matching the column default — preserved. |
| `ProcessingStatus`, `ProcessedDate`, `ProcessingError`, `PromptVersion`, `SourceForm` | Processing and audit metadata | ProcessingStatus 'Processed', ProcessedDate utcNow(), PromptVersion and SourceForm constants — all explicitly set by the existing flow, preserved. ProcessingError is NOT set by the existing flow; the new error-handling design writes it only on the catch path. |
| `OriginalSubmission` | Processing and audit metadata | NOT populated by the existing flow (gap). The replacement stores the preserved labelled-submission text here — see M-ORIGINALSUBMISSION. |
| `FormResponseID`, `SubmittedDate`, `Respondent` | Processing and audit metadata | All three preserved from the existing Create item; all executable. |
