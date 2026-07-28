# Unresolved mappings report

Generated 2026-07-28 by `scripts/build_reports.py`. Every row here is excluded from executable output. Resolution paths are in `EVIDENCE-REQUEST.md`.

## A. SharePoint side — RESOLVED (live schema export 2026-07-28)

Every SharePoint internal name, type, required flag and choice set is now Confirmed from `03-sharepoint-schema/sanitized/knowledge-submissions-schema.json`. Remaining unresolved items are Forms-side keys and flow-layer expressions only.

## B. Probable Forms keys (human resolution required; not executable)

| ID | Question | Candidate key | Why capped at Probable |
|----|----------|---------------|------------------------|
| Q34 | Operational Impact: This opportunity requires a substantial  | `rca68d3a0ad2b45c397fd0523414426b5` | 1–5 rating values are ruled non-distinctive; multiset-unique match only. |
| Q37 | Reputational Impact: This opportunity creates reputational r | `r1903e1b8394140d19377b15fc81edd65` | 1–5 rating values are ruled non-distinctive; multiset-unique match only. |

## C. Unresolved Forms keys with known candidate sets

Ambiguity within response 6 (values 'No' and '1' are non-distinctive):

| ID | Question | Candidate keys |
|----|----------|----------------|
| Q11 | External Partner Involved? | `r516051da52cf4166a478cd83a6e15291`, `r5f267e3e119041469c62a472d832324f`, `rf76887b82f1f4414a41f5e65ecef7cbd`, `r587705b554a5436aa6663834b1582469`, `rbc83faed4a274e0fb254a5c4c21edd73` |
| Q17 | Does this suggested idea directly impact a local market? | `r516051da52cf4166a478cd83a6e15291`, `r5f267e3e119041469c62a472d832324f`, `rf76887b82f1f4414a41f5e65ecef7cbd`, `r587705b554a5436aa6663834b1582469`, `rbc83faed4a274e0fb254a5c4c21edd73` |
| Q32 | Financial Impact: This opportunity requires additional budge | `r90c6dc19b575459fa68b7a65b23a9a06`, `re95a3bb4ed594260b8745180ba8d56a7` |
| Q35 | Operational Impact: This opportunity requires operations (pe | `r90c6dc19b575459fa68b7a65b23a9a06`, `re95a3bb4ed594260b8745180ba8d56a7` |
| Q41 | Is there Network/Expert Community (IBEN) Impact to be consid | `r516051da52cf4166a478cd83a6e15291`, `r5f267e3e119041469c62a472d832324f`, `rf76887b82f1f4414a41f5e65ecef7cbd`, `r587705b554a5436aa6663834b1582469`, `rbc83faed4a274e0fb254a5c4c21edd73` |
| Q43 | Is there a Professional Learning Impact to be considered reg | `r516051da52cf4166a478cd83a6e15291`, `r5f267e3e119041469c62a472d832324f`, `rf76887b82f1f4414a41f5e65ecef7cbd`, `r587705b554a5436aa6663834b1582469`, `rbc83faed4a274e0fb254a5c4c21edd73` |
| Q45 | Are there any additional factors to be considered regarding  | `r516051da52cf4166a478cd83a6e15291`, `r5f267e3e119041469c62a472d832324f`, `rf76887b82f1f4414a41f5e65ecef7cbd`, `r587705b554a5436aa6663834b1582469`, `rbc83faed4a274e0fb254a5c4c21edd73` |

## D. Unresolved Forms keys with no candidate evidence

Blank in response 6; blank properties cannot be attributed to questions. Most will resolve from a capture of reference response 2 (richly distinctive dummy content).

| ID | Question |
|----|----------|
| Q08 | Sponsor |
| Q12 | Organization Name |
| Q13 | Contact Person |
| Q14 | Role |
| Q18 | Local market(s) |
| Q19 | Is a compliance boundary adaptation required? |
| Q20 | If yes, is chief support secured? |
| Q21 | Specify chief support details |
| Q22 | Implementation Readiness Notice |
| Q23 | Strategic importance: This opportunity is strategically important to the market, |
| Q24 | Comments & explanation of agreement score (Strategic importance) |
| Q25 | Localized service offerings: This opportunity is directly connected to local way |
| Q26 | Comments & explanation of agreement score (Localized service offerings) |
| Q27 | Impact Description |
| Q28 | Data Evidence Supporting the Opportunity |
| Q29 | Expected Evidence for Impact |
| Q30 | Impacted Programme(s) |
| Q31 | Stakeholder Feedback Summary |
| Q33 | Comments & explanation of agreement score (Financial Impact) |
| Q42 | If Yes, please explain the Network/Expert Community (IBEN) Impact. |
| Q44 | If Yes, please explain the Professional Learning Impact. |
| Q46 | If Yes, please explain the additional factors. |
| Q47 | Add any supporting files |

## E. Flow-layer items awaiting the flow export

- `OriginalSubmission` source expression (labelled-submission construction) — must be preserved, not reconstructed.
- AI Builder / Select action mappings for Innovation Type, Horizon, Categorization, Ownership.
- The working default written to `ReviewStatus` (assumed 'Not reviewed'; unproven).
- The exact trigger expression for the Form response ID.
