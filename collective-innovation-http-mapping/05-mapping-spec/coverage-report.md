# Coverage report

Generated 2026-07-28 by `scripts/build_reports.py` from `mapping-spec.json` and the response-key inventory.

## Totals reconciliation

| Population | Count | Breakdown |
|------------|-------|-----------|
| Excel columns | 47 | 6 Forms metadata + 41 questions |
| Question mappings | 41 | 41 Existing (Forms side) |
| Opaque `r…` keys | 48 | 41 assigned by the flow's labelled construction + 7 permanently-blank surplus keys |
| Executable payload properties | 61 | 39 question + 5 metadata/audit + 17 preserved flow-layer |

Key-count arithmetic closes exactly: 41 + 7 = 48.

## 1. Form fields without a per-column SharePoint destination

- **Implementation Readiness Notice (Q22)** — display-only element (key identified from the flow; blank in every observed response; no schema field). No destination required.
- **Add any supporting files (Q47)** — no supporting-files column; Phase 1 excludes file references from per-column storage. Raw answer string still lands inside `OriginalSubmission`.
- **Excel metadata 'Start time', 'Last modified time', 'Name'** — no Get-response-details equivalent and no schema destination; not mapped (as in the existing flow).

## 2. SharePoint fields without Form sources (from the live schema)

All evidenced and handled: flow-constructed audit fields (`Title`, `FormResponseID`, `SubmittedDate`, `Respondent`, `SourceForm`, `OriginalSubmission`, `ProcessedDate`, `ProcessingStatus`, `PromptVersion`), AI-layer fields, and governance fields — see the flow-layer and backend tables in the mapping spec. `ProcessingError` is written only by the new catch path.

## 3. Unexplained Forms keys

7 surplus keys, blank in every observed response and referenced nowhere in the flow (listed in the unresolved-mappings report). No action required.

## 4. Existing AI and processing mappings

Captured verbatim from Create item and preserved in the payload's flow-layer properties: AISummary, Topics, KeyFindings, Examples, OpenQuestions, DifferentPerspectives, ClaimsToVerify, RelatedKnowledge, HumanReviewRequired/Reason, FullAIOutput, ReviewStatus, ProcessingStatus, ProcessedDate, PromptVersion, SourceForm, ContentTypeId.

## 5. Intentionally blank reviewer fields

ReviewStatus is explicitly 'Not reviewed' (as in the existing flow, matching the column default); other governance fields are untouched by the payload.

## 6. Intentionally blank projected-impact fields

No projected-impact columns exist in the live schema's visible field set; nothing is sent.

## 7. Excluded SharePoint system fields (from the live schema)

- `LinkTitle (Computed, displays as 'Opportunity')`
- `_ColorTag (read-only)`
- `ComplianceAssetId (read-only)`
- `ID (Counter)`
- `ContentType (Computed)`
- `Modified`
- `Created`
- `Author (Created By)`
- `Editor (Modified By)`
- `_UIVersionString (Version)`
- `Attachments`
- `Edit (Computed)`
- `LinkTitleNoMenu (Computed)`
- `DocIcon (Computed)`
- `ItemChildCount`
- `FolderChildCount`
- `_ComplianceFlags`
- `_ComplianceTag`
- `_ComplianceTagWrittenTime`
- `_ComplianceTagUserId`
- `_IsRecord (Computed)`
- `AppAuthor`
- `AppEditor`
