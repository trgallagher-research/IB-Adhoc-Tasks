# Validation report — executable payload properties

Generated 2026-07-28 by `scripts/generate_artifacts.py`. Lists the source and normalization of every property in `compose-item-payload.json`, the exclusions, and the checks applied.

## Executable properties: 61

| Property (internal name) | SP type | Source | Confidence | Kind |
|--------------------------|---------|--------|------------|------|
| `Title` | Text | `r5caae6a11afb406a8e77e0b242fb4cab` | Existing | title_from_description |
| `Respondent` | Text | Submitter email (Forms metadata). | Existing | responder |
| `SubmittedDate` | DateTime | Submission timestamp (Forms metadata). | Existing | submitdate |
| `FormResponseID` | Text | Form response ID — duplicate-prevention key and audit reference. | Existing | responseid_string |
| `OriginalSubmission` | Note | Full labelled raw submission (audit layer). | Existing | original_submission |
| `OpportunityDescription` | Note | `r5caae6a11afb406a8e77e0b242fb4cab` | Existing | multiline |
| `Sponsor` | Text | `r8140da6e45c84dbcab391c05346d9b16` | Existing | multiline |
| `AnticipatedLaunchDate` | DateTime (DateOnly) | `r8718cecca56b4ed692e9042452d04195` | Existing | date |
| `ImplementationTimeline` | Note | `rf8348c8485dd40b08c00e76f66a3d428` | Existing | multiline |
| `ExternalPartnerInvolved` | Choice | `r587705b554a5436aa6663834b1582469` | Existing | yesno_choice |
| `PartnerOrganisation` | Text | `rf7cbe61f26ab41cfa28f0b2a009e9d7c` | Existing | multiline |
| `PartnerContactPerson` | Text | `r072e0a054db54072b75c27d3d8e90140` | Existing | multiline |
| `PartnerContactRole` | Text | `r685fa8b221f64f9188951dfb6fb629ec` | Existing | multiline |
| `StrategicGoals` | Note | `r1da539bd1a494208849da87ee257c128` | Existing | multichoice_as_text |
| `StrategicAlignmentRationale` | Note | `rf9f8fa67e4fb4dfead61d31cba86aa7a` | Existing | multiline |
| `LocalMarketImpact` | Choice | `r516051da52cf4166a478cd83a6e15291` | Existing | yesno_choice |
| `LocalMarketDetails` | Note | `rf81976cae03249ef86d0d299bf126aac` | Existing | multiline |
| `ComplianceBoundaryAdaptation` | Choice | `r9ec31f96e7b34fb791c734433bb022a3` | Existing | yesno_choice |
| `ChiefSupportSecured` | Choice | `rf0bccf6e481343d1823057965c3271ea` | Existing | yesno_choice |
| `ChiefSupportDetails` | Note | `r0b456ff26ee24c11a9503908ffea1b53` | Existing | multiline |
| `StrategicImportanceScore` | Number | `rfb959d52f2494d1b92e07856edeee015` | Existing | rating |
| `StrategicImportanceExplanation` | Note | `re8d27932c227466996dbc77f67f71faa` | Existing | multiline |
| `LocalizedServiceOfferingScore` | Number | `r809645c3237a4bb4969b8082026cb3cc` | Existing | rating |
| `LocalizedServiceOfferingExplanat` | Note | `r3e390836da294861a927ce63c8d0f2c6` | Existing | multiline |
| `ImpactDescription` | Note | `rf703806487ab4148994d2fd2edb79941` | Existing | multiline |
| `DataEvidence` | Note | `r75f4515f78d946ac8a4274c151307c3e` | Existing | multiline |
| `ExpectedEvidence` | Note | `rbb5f5979ba74480fba871dbaaeb381e9` | Existing | multiline |
| `ImpactedProgrammes` | Note | `rd668321450304780986d33d7e6f474b9` | Existing | multichoice_as_text |
| `StakeholderFeedbackSummary` | Note | `rba40cea72cef44df9c70637d7473d033` | Existing | multiline |
| `FinancialImpactScore` | Number | `r90c6dc19b575459fa68b7a65b23a9a06` | Existing | rating |
| `FinancialImpactExplanation` | Note | `ra89a8e77654b43a6af62ff1247df9f8f` | Existing | multiline |
| `OperationalSupportScore` | Number | `rca68d3a0ad2b45c397fd0523414426b5` | Existing | rating |
| `OperationalChangesScore` | Number | `re95a3bb4ed594260b8745180ba8d56a7` | Existing | rating |
| `OperationalImpactExplanation` | Note | `r650d9f2a4d1f43e8938032a9cd60c658` | Existing | multiline |
| `ReputationalImpactScore` | Number | `r1903e1b8394140d19377b15fc81edd65` | Existing | rating |
| `ReputationalImpactExplanation` | Note | `r577a0e5e42554b6f8d82f7c24b8f183b` | Existing | multiline |
| `InternalStakeholdersConsulted` | Note | `rc12c559d019d4f9f9f8ed773c21c686f` | Existing | multiline |
| `InternalConsultationOutcomes` | Note | `r5d267e063680468b8f77617ee0269b60` | Existing | multiline |
| `IBENImpact` | Choice | `r5f267e3e119041469c62a472d832324f` | Existing | yesno_choice |
| `IBENImpactDescription` | Note | `r011318f6666745c891df6ed52af394b0` | Existing | multiline |
| `ProfessionalLearningImpact` | Choice | `rf76887b82f1f4414a41f5e65ecef7cbd` | Existing | yesno_choice |
| `ProfessionalLearningImpactDescri` | Note | `r074e7a91d52747519a8fe0e9af68e7dd` | Existing | multiline |
| `AdditionalFactors` | Choice | `rbc83faed4a274e0fb254a5c4c21edd73` | Existing | yesno_choice |
| `AdditionalFactorsDescription` | Note | `r90a4a472716942dfa4b9d5de21931774` | Existing | multiline |
| `SourceForm` | (flow layer) | constant `"Innovation Intake Form (Knowledge-Bank)"` | Existing | verbatim |
| `AISummary` | (flow layer) | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredO` | Existing | verbatim |
| `Topics` | (flow layer) | `join(body('Select_Topics'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `KeyFindings` | (flow layer) | `join(body('Select_Key_Findings'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `Examples` | (flow layer) | `join(body('Select_Examples'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `OpenQuestions` | (flow layer) | `join(body('Select_Open_Questions'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `DifferentPerspectives` | (flow layer) | `join(body('Select_Different_Perspectives'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `ClaimsToVerify` | (flow layer) | `join(body('Select_Claims_To_Verify'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `RelatedKnowledge` | (flow layer) | `join(body('Select_Related_Knowledge'), decodeUriComponent('%0A'))` | Existing | verbatim |
| `HumanReviewRequired` | (flow layer) | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredO` | Existing | verbatim |
| `HumanReviewReason` | (flow layer) | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredO` | Existing | verbatim |
| `ReviewStatus` | (flow layer) | constant `"Not reviewed"` | Existing | verbatim |
| `FullAIOutput` | (flow layer) | `outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text']` | Existing | verbatim |
| `ProcessingStatus` | (flow layer) | constant `"Processed"` | Existing | verbatim |
| `ProcessedDate` | (flow layer) | `utcNow()` | Existing | verbatim |
| `PromptVersion` | (flow layer) | constant `"Knowledge Submission Analyser v1\n"` | Existing | verbatim |
| `ContentTypeId` | (flow layer) | constant `"0x01002470676DA4BBF5468468EDBF918DE47C0082A052FA62248A4A84337267D7DD930B"` | Existing | verbatim |

## Excluded from per-column payload

| ID | Mapping | Forms conf. | SP conf. | Note |
|----|---------|-------------|----------|------|
| Q22 | Implementation Readiness Notice | Existing | Confirmed | no destination (by determination) |
| Q47 | Add any supporting files | Existing | Confirmed | no destination (by determination) |

Both excluded questions' raw answers still reach SharePoint inside `OriginalSubmission` (preserved labelled text), as in the existing flow's AI prompt.

## Dummy-body simulation

Raw/metadata properties (including the rendered `OriginalSubmission` template) are simulated against the sanitized response-6 body and a synthetic edge-case body (quotes, apostrophes, backslash, line breaks, Unicode, emoji; every other answer blank). Asserted: JSON round-trip escaping; blank -> `null` (never `''`, `0`, `false`, `'N/A'`, `'null'`); int for Number; ISO shape for DateTime; non-empty strings for Text/Note/Choice; `Title` never null (truncation at 255; response-ID fallback). Flow-layer (AI/constant) properties are preserved verbatim from the working flow and are exercised by the live test matrix instead. Results: `simulation-results.json`.

## Deliberate deviations from the existing Create item (documented)

- `Title`: truncated at 255 with ellipsis + blank fallback (existing raw mapping fails for >255-char descriptions).
- `SubmittedDate`: ISO 8601 UTC instead of the raw US-format string (same instant; REST is stricter than the connector).
- `OriginalSubmission`: newly populated with the preserved labelled text (existing flow left it empty).
- Everything else flow-layer: verbatim, including the `PromptVersion` trailing newline.

## Still requiring manual testing in Power Automate

- End-to-end create via the copied flow: test matrix T0–T15 (incl. DLP probe T0, duplicate check T7/T13, choice/boolean/date acceptance).
- AI-layer values arriving through the HTTP payload identically to the connector path (compare one item created by each).
