# Mapping specification — Forms → SharePoint `Knowledge Submissions`

Generated 2026-07-28 by `scripts/build_reports.py` from `mapping-spec.json` (the machine-readable source of truth). Do not hand-edit; edit the spec builder and regenerate.

## Confidence states

- **Existing** — Preserved from a working flow mapping (requires 04-existing-flow evidence).
- **Confirmed** — Supported by authoritative structural or distinctive dummy-test evidence.
- **Probable** — Strongly suggested but unproved; requires human resolution; NEVER executable.
- **Unresolved** — Missing, ambiguous, obsolete, or contradictory.

**Executability rule:** executable == true requires forms side AND SharePoint side each Existing or Confirmed. Enforced by scripts/validate_spec.py and scripts/generate_artifacts.py.

## Evidence base

- `forms_excel`: 01-forms-excel/sanitized/Innovation-Intake-Form-responses-reference.xlsx (6 dummy responses)
- `get_response_details`: 02-get-response-details/sanitized/get-response-details-response-6.body.json (dummy response 6)
- `sharepoint_schema`: ABSENT — 03-sharepoint-schema/ empty
- `existing_flow`: ABSENT — 04-existing-flow/ empty

**The SharePoint side of every row below is Unresolved** because `03-sharepoint-schema/` holds no live schema export yet. No mapping is executable until that evidence arrives.

## Forms metadata mappings

| ID | Source expression | Forms conf. | SharePoint | Normalization |
|----|-------------------|-------------|------------|---------------|
| M-RESPONDER | `body('Get_response_details')?['responder']` | Confirmed | Unresolved — no schema evidence | Plain string. Only usable for a Person field via a lookup/claims resolution step — do not post a bare email string to a Person column withou |
| M-SUBMITDATE | `body('Get_response_details')?['submitDate']` | Confirmed | Unresolved — no schema evidence | formatDateTime(..., 'yyyy-MM-ddTHH:mm:ssZ') — treat the source as UTC. Never send ''. |
| M-RESPONSEID | `triggerOutputs()?['body/resourceData/responseId']` | Probable | Unresolved — no schema evidence | Integer. Store as Number or single-line text; used for idempotency lookup before create. |

## Question mappings (Excel columns 7–47)

| ID | Question label | Answer shape | Forms response key | Forms conf. | SharePoint | Executable |
|----|----------------|--------------|--------------------|-------------|------------|------------|
| Q07 | Opportunity Description | free text | `r5caae6a11afb406a8e77e0b242fb4cab` | Confirmed | Unresolved — no schema evidence | no |
| Q08 | Sponsor | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q09 | Anticipated launch date | date | `r8718cecca56b4ed692e9042452d04195` | Confirmed | Unresolved — no schema evidence | no |
| Q10 | Anticipated timeline for implementation | free text | `rf8348c8485dd40b08c00e76f66a3d428` | Confirmed | Unresolved — no schema evidence | no |
| Q11 | External Partner Involved? | Yes/No | candidates: 5 | Unresolved | Unresolved — no schema evidence | no |
| Q12 | Organization Name | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q13 | Contact Person | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q14 | Role | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q15 | Strategic Goals | multi-choice | `r1da539bd1a494208849da87ee257c128` | Confirmed | Unresolved — no schema evidence | no |
| Q16 | Strategic Alignment Rationale | free text | `rf9f8fa67e4fb4dfead61d31cba86aa7a` | Confirmed | Unresolved — no schema evidence | no |
| Q17 | Does this suggested idea directly impact a local market? | Yes/No | candidates: 5 | Unresolved | Unresolved — no schema evidence | no |
| Q18 | Local market(s) | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q19 | Is a compliance boundary adaptation required? | Yes/No | — | Unresolved | Unresolved — no schema evidence | no |
| Q20 | If yes, is chief support secured? | Yes/No | — | Unresolved | Unresolved — no schema evidence | no |
| Q21 | Specify chief support details | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q22 | Implementation Readiness Notice | display-only notice (no input observed) | — | Unresolved | Unresolved — no schema evidence | no |
| Q23 | Strategic importance: This opportunity is strategically important to t | rating 1-5 | — | Unresolved | Unresolved — no schema evidence | no |
| Q24 | Comments & explanation of agreement score (Strategic importance) | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q25 | Localized service offerings: This opportunity is directly connected to | rating 1-5 | — | Unresolved | Unresolved — no schema evidence | no |
| Q26 | Comments & explanation of agreement score (Localized service offerings | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q27 | Impact Description | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q28 | Data Evidence Supporting the Opportunity | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q29 | Expected Evidence for Impact | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q30 | Impacted Programme(s) | multi-choice | — | Unresolved | Unresolved — no schema evidence | no |
| Q31 | Stakeholder Feedback Summary | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q32 | Financial Impact: This opportunity requires additional budget to be pi | rating 1-5 | candidates: 2 | Unresolved | Unresolved — no schema evidence | no |
| Q33 | Comments & explanation of agreement score (Financial Impact) | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q34 | Operational Impact: This opportunity requires a substantial volume of  | rating 1-5 | `rca68d3a0ad2b45c397fd0523414426b5` | Probable | Unresolved — no schema evidence | no |
| Q35 | Operational Impact: This opportunity requires operations (people, proc | rating 1-5 | candidates: 2 | Unresolved | Unresolved — no schema evidence | no |
| Q36 | Comments & explanation of agreement score (Operational Impact) | free text | `r650d9f2a4d1f43e8938032a9cd60c658` | Confirmed | Unresolved — no schema evidence | no |
| Q37 | Reputational Impact: This opportunity creates reputational risk for th | rating 1-5 | `r1903e1b8394140d19377b15fc81edd65` | Probable | Unresolved — no schema evidence | no |
| Q38 | Comments & explanation of agreement score (Reputational Impact) | free text | `r577a0e5e42554b6f8d82f7c24b8f183b` | Confirmed | Unresolved — no schema evidence | no |
| Q39 | Internal Stakeholders Consulted | free text | `rc12c559d019d4f9f9f8ed773c21c686f` | Confirmed | Unresolved — no schema evidence | no |
| Q40 | Internal Consultation Context & Outcomes | free text | `r5d267e063680468b8f77617ee0269b60` | Confirmed | Unresolved — no schema evidence | no |
| Q41 | Is there Network/Expert Community (IBEN) Impact to be considered regar | Yes/No | candidates: 5 | Unresolved | Unresolved — no schema evidence | no |
| Q42 | If Yes, please explain the Network/Expert Community (IBEN) Impact. | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q43 | Is there a Professional Learning Impact to be considered regarding thi | Yes/No | candidates: 5 | Unresolved | Unresolved — no schema evidence | no |
| Q44 | If Yes, please explain the Professional Learning Impact. | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q45 | Are there any additional factors to be considered regarding this oppor | Yes/No | candidates: 5 | Unresolved | Unresolved — no schema evidence | no |
| Q46 | If Yes, please explain the additional factors. | free text | — | Unresolved | Unresolved — no schema evidence | no |
| Q47 | Add any supporting files | file upload | — | Unresolved | Unresolved — no schema evidence | no |

## Evidence detail (Confirmed and Probable rows)

### M-RESPONDER — Submitter email (Forms metadata, not an r-key).

- Confidence: **Confirmed**
- Evidence: Structural property of the Get-response-details body; observed populated in the response-6 capture and corresponding to the Excel 'Email' metadata column.
- Normalization: Plain string. Only usable for a Person field via a lookup/claims resolution step — do not post a bare email string to a Person column without testing.
- Note: Excel 'Name' column has no Get-response-details equivalent; derive from Office 365 Users connector if needed, or leave to SharePoint Created By.

### M-SUBMITDATE — Submission timestamp (Forms metadata).

- Confidence: **Confirmed**
- Evidence: Structural property of the body. Observed 'M/d/yyyy h:mm:ss AM/PM' in UTC: the response-6 capture shows 3:23:34 PM against the Excel completion time 17:23:34 (tenant-local, UTC+2 at capture).
- Normalization: formatDateTime(..., 'yyyy-MM-ddTHH:mm:ssZ') — treat the source as UTC. Never send ''.

### M-RESPONSEID — Form response ID — duplicate-prevention key and audit reference.

- Confidence: **Probable**
- Evidence: Documented output path of the 'When a new response is submitted' trigger; the expression is the standard pattern but has not been verified against this flow's export. The Excel ID column (1..6) shows the sequential IDs exist. Verify the exact path in the live flow's Get-response-details 'Response Id' parameter.
- Normalization: Integer. Store as Number or single-line text; used for idempotency lookup before create.
- Note: Excel metadata 'Start time' and 'Last modified time' have no Get-response-details equivalent; no destination proposed.

### Q07 — Opportunity Description

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Pilot a searchable online resource hub for schools.' matches exactly one column and exactly one key within the response.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q09 — Anticipated launch date

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: only ISO-date value in the body ('2026-12-01') matches the only date answer in the row (Excel renders it as 2026-12-01 00:00:00).
- Normalization: If SharePoint type is DateTime: send ISO 8601 (the key already carries 'yyyy-MM-dd'; add 'T00:00:00Z' only if the live field rejects date-only). Blank -> JSON null. NEVER send ''.

### Q10 — Anticipated timeline for implementation

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Build in October, test in November, and pilot in December 2026.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q15 — Strategic Goals

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: only JSON-array-serialized value in the body ('["Driver A1"]') matches the multi-choice serialization of the row's Strategic Goals value ('Driver A1;'). The only other multi-choice question (Impacted Programme(s)) is blank in this response.
- Normalization: Value arrives as a JSON-array *string* (e.g. '["A","B"]'). If the destination is multiline text (as the brief indicates for StrategicGoals/ImpactedProgrammes): join(json(value), '; '). If the live schema instead shows MultiChoice: {'results': json(value)}. Blank -> omit/JSON null.
- Note: Brief indicates the likely destination is a multiline-text column (StrategicGoals named in the task brief — hint only, not schema evidence); serialize as joined text, not SharePoint multi-choice syntax.

### Q16 — Strategic Alignment Rationale

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: deliberate marker value — plain string 'Driver A1' exactly matches the rationale column, and is structurally distinct from the JSON-array form carried by the Strategic Goals key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q34 — Operational Impact: This opportunity requires a substantial volume of support from the IB to ensure it does not compromise our standards and quality.

- Confidence: **Probable**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: value '2' is unique within the response's four-rating multiset {1,1,2,3} and the row's answered ratings form the same multiset, with '2' on this column. Capped at Probable because the brief rules 1-5 values non-distinctive. Resolve with a distinct-permutation test submission.
- Normalization: If SharePoint type is Number: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q36 — Comments & explanation of agreement score (Operational Impact)

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Limited support is expected and no operational changes are planned.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q37 — Reputational Impact: This opportunity creates reputational risk for the organization.

- Confidence: **Probable**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: value '3' is unique within the response's four-rating multiset; same reasoning and same Probable cap as the Operational-support rating. Resolve with a distinct-permutation test submission.
- Normalization: If SharePoint type is Number: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.

### Q38 — Comments & explanation of agreement score (Reputational Impact)

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'The reputational risk is currently uncertain.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q39 — Internal Stakeholders Consulted

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'Professional Learning team.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

### Q40 — Internal Consultation Context & Outcomes

- Confidence: **Confirmed**
- Evidence: response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6: distinctive dummy value 'The team supported testing a small pilot.' matches exactly one column and one key.
- Normalization: Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.

## Backend fields (Word field model) — not Form questions

| Field (name hint) | Layer | Behaviour at item creation |
|-------------------|-------|----------------------------|
| Innovation Type | AI-generated analysis | Preserve the existing flow's AI/Select mapping once the flow export is in 04-existing-flow/; never source from raw Forms answers. |
| Horizon | AI-generated analysis | Same as Innovation Type. |
| Categorization | AI-generated analysis | Same as Innovation Type. |
| Ownership | AI-generated analysis / governance | Same as Innovation Type; confirm layer from flow export. |
| Projected-impact measures | Human review / governance | Intentionally blank at item creation. |
| Governance and review fields (incl. ReviewStatus) | Human review / governance | Intentionally blank except agreed defaults; ReviewStatus stays 'Not reviewed' unless the flow export proves a different working default. |
| Processing/audit fields (processing status, error detail) | Processing and audit metadata | Set by the flow itself per the error-handling design; internal names require schema evidence. |
| OriginalSubmission | Processing and audit metadata | Preserve the existing labelled-submission construction output verbatim once the flow export is available; do not reconstruct it. |
| FormResponseId (or equivalent) | Processing and audit metadata | Duplicate-prevention key. Whether a column exists is unknown — see evidence request; if absent, one must be added to the list before cutover. |

Field names above are hints from the task brief / Word model, **not** evidenced SharePoint internal names.
