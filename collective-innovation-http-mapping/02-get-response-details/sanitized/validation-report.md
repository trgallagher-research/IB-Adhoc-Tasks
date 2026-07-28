# Validation report — Get response details (response-6)

_Generated 2026-07-28._

## Source handling

- Input: one raw Power Automate **Get response details** result. The raw file is **not** committed; only sanitized artifacts are.
- Used **only the `body`**. Discarded `statusCode` and all `headers`; no routing, correlation, session, tenant, environment, or subscription identifiers are retained.
- `responder` value redacted to `[REDACTED_EMAIL]`; `submitDate` value redacted to `[DATE_VALUE]`; every answer value replaced by a category marker. All property **names** (including every `r…` key) are preserved exactly.

## Property inventory

- Total `body` properties: **50**
- Properties beginning with `r`: **49** (includes the system field `responder`)
- Opaque `r`-hash question keys (`r`+32 hex): **48**
- System fields: **2** (`responder`, `submitDate`)

Value-category breakdown (by marker applied):

| Category | Count |
| --- | --- |
| FreeText | 7 |
| Choice | 5 |
| Number | 4 |
| Date | 2 |
| MultiSelect | 1 |
| Empty | 30 |
| Email | 1 |

## Reference used for matching

- Forms Excel export (`01-forms-excel`): **47 columns** (6 system + **41 question columns**), **6 responses**.
- ⚠️ All 6 rows share a **single email**, and rows 3–6 carry **identical answer content** — so neither email nor row position is a reliable anchor. Matching was done by **which column uniquely contains each distinctive value**, never by field order.
- ⚠️ **48 response keys vs 41 question columns** — the counts do not line up, so positional (order-based) mapping is invalid by construction. The 30 blank keys correspond to unanswered questions.

## Results

- **Confirmed: 9**, **Probable: 2**, **Unresolved: 39** (of 50 properties).
- *Confirmed* = value is distinctive and maps to exactly one Excel column (no field-order assumption). *Probable* = a dominant/known candidate exists but was not uniquely proven. *Unresolved* = blank, non-distinctive (Yes/No, single-digit ratings), or not found.

### Confirmed (key → question label)

| FormsResponseKey | Category | CandidateQuestionLabel |
| --- | --- | --- |
| `responder` | Email | Email |
| `r5caae6a11afb406a8e77e0b242fb4cab` | FreeText | Opportunity Description |
| `rc12c559d019d4f9f9f8ed773c21c686f` | FreeText | Internal Stakeholders Consulted |
| `r577a0e5e42554b6f8d82f7c24b8f183b` | FreeText | Comments & explanation of agreement score (Reputational Impact) |
| `r650d9f2a4d1f43e8938032a9cd60c658` | FreeText | Comments & explanation of agreement score (Operational Impact) |
| `r5d267e063680468b8f77617ee0269b60` | FreeText | Internal Consultation Context & Outcomes |
| `rf8348c8485dd40b08c00e76f66a3d428` | FreeText | Anticipated timeline for implementation |
| `r8718cecca56b4ed692e9042452d04195` | Date | Anticipated launch date |
| `rf9f8fa67e4fb4dfead61d31cba86aa7a` | FreeText | Strategic Alignment Rationale |

### Probable (needs review)

| FormsResponseKey | Category | CandidateQuestionLabel |
| --- | --- | --- |
| `submitDate` | Date | Completion time |
| `r1da539bd1a494208849da87ee257c128` | MultiSelect | Strategic Goals |

## Requirement compliance

1. Every `r…` property preserved exactly — **yes** (names untouched; only values replaced).
2. `responder`/`submitDate` names preserved, values redacted — **yes**.
3. `responder` → `[REDACTED_EMAIL]` — **yes**.
4. Free-text → `[TEXT_VALUE]` / blanks → `[EMPTY]` — **yes**.
5. Dates → `[DATE_VALUE]` — **yes**.
6. Numeric ratings → `[NUMBER_VALUE]` — **yes**.
7. Yes/No → `[CHOICE_VALUE]` — **yes**.
8. Multi-select → `[MULTISELECT_VALUE]` — **yes**.
9. Blank properties retained, not deleted — **yes** (all 30 kept as `[EMPTY]`).
10. No label inferred from a blank — **yes** (all blanks are Unresolved).
11. No `r…` key altered/shortened/regenerated — **yes**.
12. Total `r…` properties reported — **yes** (see inventory).

CSV Confidence values used: Confirmed / Probable / Unresolved only. Confirmed requires a distinctive value matched to the Excel export without relying on field order; blanks are Unresolved.
