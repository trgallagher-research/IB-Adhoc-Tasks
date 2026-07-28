# Mock form submissions for testing

Generated 2026-07-28 by `scripts/build_test_submissions.py`. Answers are hand-authored; question labels and destination columns come from `mapping-spec.json`, so the verification table cannot drift from the mapping.

All content is invented; names and organisations are fictional.

## ⚠ The governance gate — read before Section 4

The form branches on **Q13 (compliance boundary adaptation)** and **Q14 (chief support secured)**. Answering Q13 `Yes`/`I don't know` **and** Q14 `No` shows the Implementation Readiness Notice (Q16) and then **ends the form** — Q15 and the whole of Sections 5, 6 and 7 never appear, ratings included.

Evidence: response 8 took that path, and Q15 arrived blank despite being marked *Required*. Submission **FULL** below therefore answers Q13 `Yes` / Q14 `Yes` to keep the form open. Submission **GATE** deliberately takes the gated path.

---

# Submission FULL — every question answered

One submission covering all 41 questions. Every free-text answer starts with a `Q<n>` marker matching its form question number, so if a key were mis-mapped it shows up immediately in the created item — no diffing required.

| Form Q | Question | Answer to enter | Note |
|--------|----------|-----------------|------|
| 1 | Opportunity Description | `Q1 — Pilot a searchable "resource hub" for schools that consolidates guidance, professional learning materials, worked examples and implementation resources into one place, so colleagues don't spend time hunting across separate platforms; scope covers discovery, tagging, permissions, multilingual labels, feedback capture, usage analytics, content ownership and review cycles.` | **over 255 chars on purpose** — Title must truncate with `...`, description must not |
| 2 | Sponsor | `Q2 Sponsor — Alex Rivera, Director (Test Dept)` |  |
| 3 | Anticipated launch date | `1/12/2026` | pick 1 December 2026 in the date picker |
| 4 | Anticipated timeline for implementation | *see fenced block below* | **press Enter between lines** — see the fenced block below |
| 5 | External Partner Involved? | `Yes` | opens Q6–Q8 |
| 6 | Organization Name | `Q6 Org — Learning Futures Lab (test)` |  |
| 7 | Contact Person | `Q7 Contact — Jordan Bailey` |  |
| 8 | Role | `Q8 Role — Programme Director` | was blank last run; must not be this time |
| 9 | Strategic Goals | `Driver A2, Driver B3, Driver C1` | tick exactly these **three** — deliberately not A1 |
| 10 | Strategic Alignment Rationale | `Q10 Rationale — supports discovery; reduces duplication. Path test: C:\temp\notes — ünïcödé é.` | carries a backslash and accents |
| 11 | Does this suggested idea directly impact a local market? | `Yes` | opens Q12 |
| 12 | Local market(s) | `Q12 Markets — Netherlands, Spain, México` |  |
| 13 | Is a compliance boundary adaptation required? | `Yes` | ⚠ **Yes**, then Q14 **Yes** — otherwise the form ends early |
| 14 | If yes, is chief support secured? | `Yes` | ⚠ **must be Yes** to keep the form open |
| 15 | Specify chief support details | `Q15 Chief support — confirmed for a limited discovery and pilot phase.` |  |
| 16 | Implementation Readiness Notice | *leave blank* | should not appear on this path; if it does, leave blank |
| 17 | Strategic importance: This opportunity is strategically im | `5` | rating |
| 18 | Comments & explanation of agreement score (Strategic impor | `Q18 Comments — strategic importance rationale.` |  |
| 19 | Localized service offerings: This opportunity is directly  | `1` | rating |
| 20 | Comments & explanation of agreement score (Localized servi | `Q20 Comments — localized service offerings rationale.` |  |
| 21 | Impact Description | *see fenced block below* | **press Enter between lines** |
| 22 | Data Evidence Supporting the Opportunity | `Q22 Data evidence — informal feedback only so far.` |  |
| 23 | Expected Evidence for Impact | `Q23 Expected evidence — task completion, time-to-find, satisfaction.` |  |
| 24 | Impacted Programme(s) | `PYP, DP, Non-programme specific` | tick exactly these **three** |
| 25 | Stakeholder Feedback Summary | `Q25 Stakeholder feedback — early interest, caveats on ownership.` |  |
| 26 | Financial Impact: This opportunity requires additional bud | `4` | rating |
| 27 | Comments & explanation of agreement score (Financial Impac | `Q27 Comments — financial impact rationale.` |  |
| 28 | Operational Impact: This opportunity requires a substantia | `2` | rating |
| 29 | Operational Impact: This opportunity requires operations ( | `3` | rating |
| 30 | Comments & explanation of agreement score (Operational Imp | `Q30 Comments — operational impact rationale.` |  |
| 31 | Reputational Impact: This opportunity creates reputational | `5` | rating — repeats Q17's value, see note below |
| 32 | Comments & explanation of agreement score (Reputational Im | `Q32 Comments — reputational impact rationale.` |  |
| 33 | Internal Stakeholders Consulted | `Q33 Stakeholders — Professional Learning; Technology; Data Protection.` |  |
| 34 | Internal Consultation Context & Outcomes | `Q34 Consultation — supportive of a limited pilot subject to ownership.` |  |
| 35 | Is there Network/Expert Community (IBEN) Impact to be cons | `Yes` | opens Q36 |
| 36 | If Yes, please explain the Network/Expert Community (IBEN) | `Q36 IBEN — experienced educators could review relevance during the pilot.` |  |
| 37 | Is there a Professional Learning Impact to be considered r | `Yes` | opens Q38 |
| 38 | If Yes, please explain the Professional Learning Impact. | `Q38 PL — affects how schools discover professional learning.` |  |
| 39 | Are there any additional factors to be considered regardin | `Yes` | opens Q40 |
| 40 | If Yes, please explain the additional factors. | `Q40 Additional — accessibility, multilingual quality, retention of content.` |  |
| 41 | Add any supporting files | *attach a file* | **upload any small test file** — Phase 1 does not map it, but the flow must not break |

### Multi-line answers — type these with real Enter keypresses

**Q4 — Anticipated timeline for implementation**

```
Q4 line one — build in October 2026.
Q4 line two — test in November, "internal only".
Q4 line three — pilot in December 2026.
```

**Q21 — Impact Description**

```
Q21 first paragraph: about 12 schools in the pilot.
Q21 second paragraph: expected faster discovery & fewer repeat queries.
Q21 third paragraph: 100% of pilot schools surveyed.
```

Do not type the words "line break" — the point is to test real newline characters reaching a multiline SharePoint column.

### Note on the ratings

Six rating questions, five possible values, so one value must repeat: **Q17 and Q31 are both `5`**. They map to very different columns (`StrategicImportanceScore` and `ReputationalImpactScore`) and their adjacent comment fields carry distinct `Q<n>` markers, so a swap would still be visible. Every other rating is unique.

## Verification table — check each row on the created item

| Form Q | SharePoint column | Expect |
|--------|-------------------|--------|
| 1 | `OpportunityDescription` | full text (Title separately truncated to 255 + `...`) |
| 2 | `Sponsor` | `Q2 Sponsor — Alex Rivera, Director (Test Dep…` |
| 3 | `AnticipatedLaunchDate` | `2026-12-01` |
| 4 | `ImplementationTimeline` | line breaks preserved |
| 5 | `ExternalPartnerInvolved` | `Yes` |
| 6 | `PartnerOrganisation` | `Q6 Org — Learning Futures Lab (test)` |
| 7 | `PartnerContactPerson` | `Q7 Contact — Jordan Bailey` |
| 8 | `PartnerContactRole` | `Q8 Role — Programme Director` |
| 9 | `StrategicGoals` | `Driver A2; Driver B3; Driver C1` |
| 10 | `StrategicAlignmentRationale` | `Q10 Rationale — supports discovery; reduces …` |
| 11 | `LocalMarketImpact` | `Yes` |
| 12 | `LocalMarketDetails` | `Q12 Markets — Netherlands, Spain, México` |
| 13 | `ComplianceBoundaryAdaptation` | `Yes` |
| 14 | `ChiefSupportSecured` | `Yes` |
| 15 | `ChiefSupportDetails` | `Q15 Chief support — confirmed for a limited …` |
| 16 | `— (no destination by design)` | empty |
| 17 | `StrategicImportanceScore` | bare number `5` |
| 18 | `StrategicImportanceExplanation` | `Q18 Comments — strategic importance rational…` |
| 19 | `LocalizedServiceOfferingScore` | bare number `1` |
| 20 | `LocalizedServiceOfferingExplanat` | `Q20 Comments — localized service offerings r…` |
| 21 | `ImpactDescription` | line breaks preserved |
| 22 | `DataEvidence` | `Q22 Data evidence — informal feedback only s…` |
| 23 | `ExpectedEvidence` | `Q23 Expected evidence — task completion, tim…` |
| 24 | `ImpactedProgrammes` | `PYP; DP; Non-programme specific` |
| 25 | `StakeholderFeedbackSummary` | `Q25 Stakeholder feedback — early interest, c…` |
| 26 | `FinancialImpactScore` | bare number `4` |
| 27 | `FinancialImpactExplanation` | `Q27 Comments — financial impact rationale.` |
| 28 | `OperationalSupportScore` | bare number `2` |
| 29 | `OperationalChangesScore` | bare number `3` |
| 30 | `OperationalImpactExplanation` | `Q30 Comments — operational impact rationale.` |
| 31 | `ReputationalImpactScore` | bare number `5` |
| 32 | `ReputationalImpactExplanation` | `Q32 Comments — reputational impact rationale…` |
| 33 | `InternalStakeholdersConsulted` | `Q33 Stakeholders — Professional Learning; Te…` |
| 34 | `InternalConsultationOutcomes` | `Q34 Consultation — supportive of a limited p…` |
| 35 | `IBENImpact` | `Yes` |
| 36 | `IBENImpactDescription` | `Q36 IBEN — experienced educators could revie…` |
| 37 | `ProfessionalLearningImpact` | `Yes` |
| 38 | `ProfessionalLearningImpactDescri` | `Q38 PL — affects how schools discover profes…` |
| 39 | `AdditionalFactors` | `Yes` |
| 40 | `AdditionalFactorsDescription` | `Q40 Additional — accessibility, multilingual…` |
| 41 | `— (no destination by design)` | no column — file not mapped in Phase 1; **flow must still succeed** |

Plus the flow-layer columns, which must look identical to items created by the original flow: `SourceForm`, `ReviewStatus` = *Not reviewed*, `ProcessingStatus` = *Processed*, `PromptVersion`, `ProcessedDate`, and all AI columns populated. `OriginalSubmission` must be **populated** (the original flow left it empty).

---

# Submission GATE — governance early-exit (already passed as response 8)

Keep as a named test: it is a legitimate production path and proves the payload copes when most of the form never appears.

| Form Q | Answer |
|--------|--------|
| 1 Opportunity Description | `GATE test` |
| 3 Anticipated launch date | any |
| 4 Timeline | `GATE test` |
| 5 External Partner Involved? | `No` |
| 9 Strategic Goals | tick one |
| 10 Rationale | `GATE test` |
| 11 Local market? | `Yes` |
| 12 Local market(s) | `GATE market` |
| 13 Compliance adaptation? | `I don't know (see compliance boundaries appendix)` |
| 14 Chief support secured? | `No` |
| 16 Readiness Notice | leave blank |

The form should end straight after Q16.

**What it proves:** all six ratings and every Section 5–7 column arrive empty rather than `0`, `false` or `N/A`, even though many are marked *Required*. Re-run only if the payload changes.

---

## After testing

1. Note each response ID.
2. Delete the created items from `Knowledge Submissions` (sort by `FormResponseID`).
3. Record outcomes in `test-results-2026-07-28.md`.

Keep the Forms responses — they are dummy data, and the sandbox harness can replay any of them by ID without re-typing.
