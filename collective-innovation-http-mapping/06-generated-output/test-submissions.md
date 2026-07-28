# Mock form submissions for testing

Copy-paste answers for dummy submissions against the copied flow. All content
is invented; names, organisations and people are fictional. Question labels
below are the live form's, in form order.

Three submissions, each aimed at specific rows of `test-matrix.md`:

| # | Purpose | Covers |
|---|---------|--------|
| **A** | Everything answered, deliberately awkward characters, over-long description | T2, T4, T5, T6b |
| **B** | Bare minimum, everything optional blank | T1, T3, T6a |
| **C** | All conditional branches closed | T14 |

Submit **A first** — it exercises the most. Note each submission's response ID
(visible in the flow run, and as `FormResponseID` on the created item) so you
can find and delete the items afterwards.

---

## Submission A — full, with awkward characters

Answer **Yes** to the local-market question so the two extra rating questions
appear.

| Question | Answer |
|---|---|
| Opportunity Description | `Pilot a searchable "resource hub" for schools that consolidates guidance, professional learning materials, worked examples and implementation resources into one place, so that colleagues don't spend time hunting across separate platforms; the pilot would cover discovery, tagging, permissions, multilingual labels, feedback capture, usage analytics, content ownership, review cycles and a lightweight governance model for retiring outdated material.` |
| Sponsor | `Alex Rivera — Director, Test Department` |
| Anticipated launch date | `01/12/2026` (pick 1 December 2026 in the date picker) |
| Anticipated timeline for implementation | `Build in October 2026.` then a **line break**, then `Test in November — "internal only".` then a line break, then `Pilot in December 2026.` |
| External Partner Involved? | `Yes` |
| Organization Name | `Learning Futures Lab (test)` |
| Contact Person | `Jordan Bailey` |
| Role | `Programme Director` |
| Strategic Goals | tick **three** options |
| Strategic Alignment Rationale | `Supports discovery of existing material; reduces duplication; improves consistency of what schools see. Path example: C:\temp\notes — testing a backslash.` |
| Does this suggested idea directly impact a local market? | `Yes` |
| Local market(s) | `Netherlands, Spain, México — multilingual schools` |
| Is a compliance boundary adaptation required? | `I don't know` |
| If yes, is chief support secured? | `No` |
| Specify chief support details | `Not yet raised; would need a decision before any pilot begins.` |
| Strategic importance (rating) | `5` |
| Comments (Strategic importance) | `Could support acquisition conversations by making the offer easier to see.` |
| Localized service offerings (rating) | `2` |
| Comments (Localized service offerings) | `Content would initially be centrally produced, so local relevance is limited at first.` |
| Impact Description | `Roughly 12 schools in the pilot. Expected: faster discovery, fewer repeat queries, clearer ownership.` |
| Data Evidence Supporting the Opportunity | `Informal feedback only at this stage — no systematic data yet.` |
| Expected Evidence for Impact | `Task-completion rate, time-to-find, satisfaction score, repeat-query volume.` |
| Impacted Programme(s) | tick **two** options |
| Stakeholder Feedback Summary | `Early conversations suggest interest, with caveats about who maintains content.` |
| Financial Impact (rating) | `4` |
| Comments (Financial Impact) | `Some budget needed for design and translation review; no licence cost expected.` |
| Operational Impact — support (rating) | `3` |
| Operational Impact — changes (rating) | `1` |
| Comments (Operational Impact) | `Temporary support from several teams during the pilot; no permanent process change proposed.` |
| Reputational Impact (rating) | `2` |
| Comments (Reputational Impact) | `Low, provided outdated material can be withdrawn quickly.` |
| Internal Stakeholders Consulted | `Professional Learning; Technology; Data Protection` |
| Internal Consultation Context & Outcomes | `Supportive of a limited pilot subject to clear ownership and a review cycle.` |
| IBEN Impact? | `Yes` |
| Explain IBEN Impact | `A small number of experienced educators could review relevance during the pilot.` |
| Professional Learning Impact? | `Yes` |
| Explain Professional Learning Impact | `Directly affects how schools discover professional learning; PL team would define inclusion criteria.` |
| Additional factors? | `Yes` |
| Explain additional factors | `Accessibility, multilingual quality, retention/retirement of content, and access permissions.` |
| Supporting files | leave empty |

**What A proves:** the description is over 255 characters, so `Title` must come
back truncated with `...` while `OpportunityDescription` keeps the full text.
The quotes, apostrophe, backslash, em-dashes, accented character and line
breaks all have to survive into SharePoint intact. `ComplianceBoundaryAdaptation`
must store `I don't know` — the third choice, not Yes/No. Both multi-selects
must arrive as `; `-joined text.

---

## Submission B — minimum, everything else blank

Answer **only** what the form forces you to. Leave every optional question
untouched — especially all ratings and the launch date.

| Question | Answer |
|---|---|
| Opportunity Description | `Minimal test B` |
| any question the form marks required | shortest valid answer, e.g. `Test` |
| everything else | **leave blank** |

**What B proves:** the null handling that the whole payload design turns on.
On the created item, every skipped Number column must be **empty — not `0`**,
the date column empty — **not 1900-01-01**, and blank Choice columns empty —
not `N/A`. Also `Title` should read `Minimal test B`.

---

## Submission C — conditionals closed

| Question | Answer |
|---|---|
| Opportunity Description | `Conditional branch test C` |
| Sponsor | `Test Sponsor` |
| External Partner Involved? | `No` |
| Does this suggested idea directly impact a local market? | `No` |
| Is a compliance boundary adaptation required? | `No` |
| IBEN Impact? | `No` |
| Professional Learning Impact? | `No` |
| Additional factors? | `No` |
| everything else | leave blank / shortest valid answer |

**What C proves:** when a branch is closed, its follow-up columns
(`PartnerOrganisation`, `LocalMarketDetails`, `ChiefSupportDetails`,
`IBENImpactDescription`, and so on) must be **empty**, never `N/A` or `false`.
The parent Yes/No columns must still read `No`.

---

## After testing

1. Note each response ID.
2. Delete the created items from `Knowledge Submissions` (filter or sort by
   `FormResponseID` to find them).
3. Record outcomes in `test-results-2026-07-28.md`.

The Forms responses themselves can stay — they are dummy data, and keeping them
means any of these can be replayed later through the sandbox harness by ID
without re-typing.
