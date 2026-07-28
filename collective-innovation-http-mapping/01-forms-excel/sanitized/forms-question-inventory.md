# Forms question inventory (normalized)

Generated 2026-07-28 by `scripts/build_inventories.py` from the dummy-safe Excel reference export. 47 columns = 6 Forms metadata + 41 question/output columns, across 6 dummy reference responses.

| # | Kind | Question label | Filled (of 6) | Notes |
|---|------|----------------|---------------|-------|
| 1 | metadata | ID | 6 |  |
| 2 | metadata | Start time | 6 |  |
| 3 | metadata | Completion time | 6 |  |
| 4 | metadata | Email | 6 |  |
| 5 | metadata | Name | 6 |  |
| 6 | metadata | Last modified time | 0 |  |
| 7 | question | Opportunity Description | 6 |  |
| 8 | question | Sponsor | 2 |  |
| 9 | question | Anticipated launch date | 6 | date question; Excel shows datetime at midnight |
| 10 | question | Anticipated timeline for implementation | 6 |  |
| 11 | question | External Partner Involved? | 6 |  |
| 12 | question | Organization Name | 1 | conditional on 'External Partner Involved?' = Yes (filled only in response 2) |
| 13 | question | Contact Person | 1 | conditional on 'External Partner Involved?' = Yes (filled only in response 2) |
| 14 | question | Role | 1 | conditional on 'External Partner Involved?' = Yes (filled only in response 2) |
| 15 | question | Strategic Goals | 6 | multi-choice; Excel serializes as 'Choice1;Choice2;' with trailing semicolon |
| 16 | question | Strategic Alignment Rationale | 6 |  |
| 17 | question | Does this suggested idea directly impact a local market? | 6 |  |
| 18 | question | Local market(s) | 2 | conditional on 'Does this suggested idea directly impact a local market?' = Yes |
| 19 | question | Is a compliance boundary adaptation required? | 2 |  |
| 20 | question | If yes, is chief support secured? | 2 | conditional on 'Is a compliance boundary adaptation required?' = Yes |
| 21 | question | Specify chief support details | 2 | conditional on 'Is a compliance boundary adaptation required?' = Yes |
| 22 | question | Implementation Readiness Notice | 0 | BLANK in all 6 reference responses including fully-completed response 2 — almost certainly a display-only notice element with no input |
| 23 | question | Strategic importance: This opportunity is strategically important to the market, including | 2 | filled only in responses 1-2 (both local market = Yes); appears conditional on the local-market branch — unproven, verify against live form; Likert-style rating; observed integer strings within 1-5 |
| 24 | question | Comments & explanation of agreement score (Strategic importance) | 2 | filled only in responses 1-2; see column 23 note |
| 25 | question | Localized service offerings: This opportunity is directly connected to local ways of worki | 2 | filled only in responses 1-2; see column 23 note; Likert-style rating; observed integer strings within 1-5 |
| 26 | question | Comments & explanation of agreement score (Localized service offerings) | 2 | filled only in responses 1-2; see column 23 note |
| 27 | question | Impact Description | 2 |  |
| 28 | question | Data Evidence Supporting the Opportunity | 2 |  |
| 29 | question | Expected Evidence for Impact | 2 |  |
| 30 | question | Impacted Programme(s) | 2 | multi-choice; Excel serializes as 'Choice1;Choice2;' with trailing semicolon |
| 31 | question | Stakeholder Feedback Summary | 2 |  |
| 32 | question | Financial Impact: This opportunity requires additional budget to be piloted or taken to ma | 6 | Likert-style rating; observed integer strings within 1-5 |
| 33 | question | Comments & explanation of agreement score (Financial Impact) | 2 |  |
| 34 | question | Operational Impact: This opportunity requires a substantial volume of support from the IB  | 6 | Likert-style rating; observed integer strings within 1-5 |
| 35 | question | Operational Impact: This opportunity requires operations (people, process, or system) chan | 6 | Likert-style rating; observed integer strings within 1-5 |
| 36 | question | Comments & explanation of agreement score (Operational Impact) | 6 |  |
| 37 | question | Reputational Impact: This opportunity creates reputational risk for the organization. | 6 | Likert-style rating; observed integer strings within 1-5 |
| 38 | question | Comments & explanation of agreement score (Reputational Impact) | 6 |  |
| 39 | question | Internal Stakeholders Consulted | 6 |  |
| 40 | question | Internal Consultation Context & Outcomes | 6 |  |
| 41 | question | Is there Network/Expert Community (IBEN) Impact to be considered regarding this opportunit | 6 |  |
| 42 | question | If Yes, please explain the Network/Expert Community (IBEN) Impact. | 1 | conditional on IBEN impact = Yes |
| 43 | question | Is there a Professional Learning Impact to be considered regarding this opportunity? | 6 |  |
| 44 | question | If Yes, please explain the Professional Learning Impact. | 1 | conditional on Professional Learning impact = Yes |
| 45 | question | Are there any additional factors to be considered regarding this opportunity? | 6 |  |
| 46 | question | If Yes, please explain the additional factors. | 1 | conditional on additional factors = Yes |
| 47 | question | Add any supporting files | 0 | file-upload question; blank in all reference responses |
