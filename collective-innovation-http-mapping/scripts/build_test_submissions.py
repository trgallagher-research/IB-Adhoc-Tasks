#!/usr/bin/env python3
"""Generate 06-generated-output/test-submissions.md.

The answers are hand-authored here; the question labels, Excel columns and
destination SharePoint internal names are pulled from mapping-spec.json so the
verification table cannot drift from the mapping.

Design rule for the full-coverage submission: every free-text answer carries a
`Q<n>` marker matching its form question number, so a mis-mapped key is visible
at a glance in the created item rather than requiring a diff.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "05-mapping-spec/mapping-spec.json").read_text())
GENERATED = "2026-07-28"

BY_COL = {e["excel_column"]: e for e in SPEC["question_mappings"]}

# form question number -> excel column (form order is Excel order for questions)
FORM_Q_TO_COL = {n: n + 6 for n in range(1, 42)}

MULTILINE_Q4 = """Q4 line one — build in October 2026.
Q4 line two — test in November, "internal only".
Q4 line three — pilot in December 2026."""

MULTILINE_Q21 = """Q21 first paragraph: about 12 schools in the pilot.
Q21 second paragraph: expected faster discovery & fewer repeat queries.
Q21 third paragraph: 100% of pilot schools surveyed."""

# excel column -> (answer, note shown in the instructions table)
ANSWERS = {
    7: ("Q1 — Pilot a searchable \"resource hub\" for schools that consolidates guidance, professional "
        "learning materials, worked examples and implementation resources into one place, so colleagues "
        "don't spend time hunting across separate platforms; scope covers discovery, tagging, permissions, "
        "multilingual labels, feedback capture, usage analytics, content ownership and review cycles.",
        "**over 255 chars on purpose** — Title must truncate with `...`, description must not"),
    8: ("Q2 Sponsor — Alex Rivera, Director (Test Dept)", ""),
    9: ("1/12/2026", "pick 1 December 2026 in the date picker"),
    10: (MULTILINE_Q4, "**press Enter between lines** — see the fenced block below"),
    11: ("Yes", "opens Q6–Q8"),
    12: ("Q6 Org — Learning Futures Lab (test)", ""),
    13: ("Q7 Contact — Jordan Bailey", ""),
    14: ("Q8 Role — Programme Director", "was blank last run; must not be this time"),
    15: ("Driver A2, Driver B3, Driver C1", "tick exactly these **three** — deliberately not A1"),
    16: ("Q10 Rationale — supports discovery; reduces duplication. Path test: C:\\temp\\notes — ünïcödé é.",
         "carries a backslash and accents"),
    17: ("Yes", "opens Q12"),
    18: ("Q12 Markets — Netherlands, Spain, México", ""),
    19: ("Yes", "⚠ **Yes**, then Q14 **Yes** — otherwise the form ends early"),
    20: ("Yes", "⚠ **must be Yes** to keep the form open"),
    21: ("Q15 Chief support — confirmed for a limited discovery and pilot phase.", ""),
    22: (None, "should not appear on this path; if it does, leave blank"),
    23: ("5", "rating"),
    24: ("Q18 Comments — strategic importance rationale.", ""),
    25: ("1", "rating"),
    26: ("Q20 Comments — localized service offerings rationale.", ""),
    27: (MULTILINE_Q21, "**press Enter between lines**"),
    28: ("Q22 Data evidence — informal feedback only so far.", ""),
    29: ("Q23 Expected evidence — task completion, time-to-find, satisfaction.", ""),
    30: ("PYP, DP, Non-programme specific", "tick exactly these **three**"),
    31: ("Q25 Stakeholder feedback — early interest, caveats on ownership.", ""),
    32: ("4", "rating"),
    33: ("Q27 Comments — financial impact rationale.", ""),
    34: ("2", "rating"),
    35: ("3", "rating"),
    36: ("Q30 Comments — operational impact rationale.", ""),
    37: ("5", "rating — repeats Q17's value, see note below"),
    38: ("Q32 Comments — reputational impact rationale.", ""),
    39: ("Q33 Stakeholders — Professional Learning; Technology; Data Protection.", ""),
    40: ("Q34 Consultation — supportive of a limited pilot subject to ownership.", ""),
    41: ("Yes", "opens Q36"),
    42: ("Q36 IBEN — experienced educators could review relevance during the pilot.", ""),
    43: ("Yes", "opens Q38"),
    44: ("Q38 PL — affects how schools discover professional learning.", ""),
    45: ("Yes", "opens Q40"),
    46: ("Q40 Additional — accessibility, multilingual quality, retention of content.", ""),
    47: ("UPLOAD", "**upload any small test file** — Phase 1 does not map it, but the flow must not break"),
}


def sp_name(col):
    sp = BY_COL[col]["sharepoint"]
    return sp["internal_name"] or "— (no destination by design)"


def main():
    md = [
        "# Mock form submissions for testing",
        "",
        f"Generated {GENERATED} by `scripts/build_test_submissions.py`. Answers are "
        "hand-authored; question labels and destination columns come from "
        "`mapping-spec.json`, so the verification table cannot drift from the mapping.",
        "",
        "All content is invented; names and organisations are fictional.",
        "",
        "## ⚠ The governance gate — read before Section 4",
        "",
        "The form branches on **Q13 (compliance boundary adaptation)** and **Q14 (chief "
        "support secured)**. Answering Q13 `Yes`/`I don't know` **and** Q14 `No` shows "
        "the Implementation Readiness Notice (Q16) and then **ends the form** — Q15 and "
        "the whole of Sections 5, 6 and 7 never appear, ratings included.",
        "",
        "Evidence: response 8 took that path, and Q15 arrived blank despite being marked "
        "*Required*. Submission **FULL** below therefore answers Q13 `Yes` / Q14 `Yes` "
        "to keep the form open. Submission **GATE** deliberately takes the gated path.",
        "",
        "---",
        "",
        "# Submission FULL — every question answered",
        "",
        "One submission covering all 41 questions. Every free-text answer starts with a "
        "`Q<n>` marker matching its form question number, so if a key were mis-mapped it "
        "shows up immediately in the created item — no diffing required.",
        "",
        "| Form Q | Question | Answer to enter | Note |",
        "|--------|----------|-----------------|------|",
    ]
    for qn in range(1, 42):
        col = FORM_Q_TO_COL[qn]
        answer, note = ANSWERS[col]
        label = BY_COL[col]["form_question_label"]
        if answer is None:
            shown = "*leave blank*"
        elif answer == "UPLOAD":
            shown = "*attach a file*"
        elif "\n" in answer:
            shown = "*see fenced block below*"
        else:
            shown = f"`{answer}`"
        md.append(f"| {qn} | {label[:58]} | {shown} | {note} |")

    md += [
        "",
        "### Multi-line answers — type these with real Enter keypresses",
        "",
        "**Q4 — Anticipated timeline for implementation**",
        "",
        "```",
        MULTILINE_Q4,
        "```",
        "",
        "**Q21 — Impact Description**",
        "",
        "```",
        MULTILINE_Q21,
        "```",
        "",
        "Do not type the words \"line break\" — the point is to test real newline "
        "characters reaching a multiline SharePoint column.",
        "",
        "### Note on the ratings",
        "",
        "Six rating questions, five possible values, so one value must repeat: **Q17 and "
        "Q31 are both `5`**. They map to very different columns "
        "(`StrategicImportanceScore` and `ReputationalImpactScore`) and their adjacent "
        "comment fields carry distinct `Q<n>` markers, so a swap would still be visible. "
        "Every other rating is unique.",
        "",
        "## Verification table — check each row on the created item",
        "",
        "| Form Q | SharePoint column | Expect |",
        "|--------|-------------------|--------|",
    ]
    for qn in range(1, 42):
        col = FORM_Q_TO_COL[qn]
        answer, _ = ANSWERS[col]
        shape = BY_COL[col]["forms_answer_shape"]
        if answer is None:
            expect = "empty"
        elif answer == "UPLOAD":
            expect = "no column — file not mapped in Phase 1; **flow must still succeed**"
        elif shape == "rating 1-5":
            expect = f"bare number `{answer}`"
        elif shape == "multi-choice":
            expect = "`" + "; ".join(a.strip() for a in answer.split(",")) + "`"
        elif shape == "date":
            expect = "`2026-12-01`"
        elif "\n" in answer:
            expect = "line breaks preserved"
        elif qn == 1:
            expect = "full text (Title separately truncated to 255 + `...`)"
        else:
            expect = f"`{answer[:44]}…`" if len(answer) > 44 else f"`{answer}`"
        md.append(f"| {qn} | `{sp_name(col)}` | {expect} |")

    md += [
        "",
        "Plus the flow-layer columns, which must look identical to items created by the "
        "original flow: `SourceForm`, `ReviewStatus` = *Not reviewed*, `ProcessingStatus` "
        "= *Processed*, `PromptVersion`, `ProcessedDate`, and all AI columns populated. "
        "`OriginalSubmission` must be **populated** (the original flow left it empty).",
        "",
        "---",
        "",
        "# Submission GATE — governance early-exit (already passed as response 8)",
        "",
        "Keep as a named test: it is a legitimate production path and proves the payload "
        "copes when most of the form never appears.",
        "",
        "| Form Q | Answer |",
        "|--------|--------|",
        "| 1 Opportunity Description | `GATE test` |",
        "| 3 Anticipated launch date | any |",
        "| 4 Timeline | `GATE test` |",
        "| 5 External Partner Involved? | `No` |",
        "| 9 Strategic Goals | tick one |",
        "| 10 Rationale | `GATE test` |",
        "| 11 Local market? | `Yes` |",
        "| 12 Local market(s) | `GATE market` |",
        "| 13 Compliance adaptation? | `I don't know (see compliance boundaries appendix)` |",
        "| 14 Chief support secured? | `No` |",
        "| 16 Readiness Notice | leave blank |",
        "",
        "The form should end straight after Q16.",
        "",
        "**What it proves:** all six ratings and every Section 5–7 column arrive empty "
        "rather than `0`, `false` or `N/A`, even though many are marked *Required*. "
        "Re-run only if the payload changes.",
        "",
        "---",
        "",
        "## After testing",
        "",
        "1. Note each response ID.",
        "2. Delete the created items from `Knowledge Submissions` (sort by "
        "`FormResponseID`).",
        "3. Record outcomes in `test-results-2026-07-28.md`.",
        "",
        "Keep the Forms responses — they are dummy data, and the sandbox harness can "
        "replay any of them by ID without re-typing.",
        "",
    ]
    (ROOT / "06-generated-output/test-submissions.md").write_text("\n".join(md))
    print(f"test-submissions.md written: {len(ANSWERS)} questions covered")


if __name__ == "__main__":
    main()
