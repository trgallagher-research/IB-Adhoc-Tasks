#!/usr/bin/env python3
"""Build 05-mapping-spec/mapping-spec.json from the source inventories plus the
evidence judgments encoded below.

The inventories are mechanical extracts; this file is where mapping *judgment*
lives, so every non-Unresolved assignment carries its evidence string. Rules
enforced here and in scripts/validate_spec.py:

  - Confirmed requires distinctive-value or structural evidence, never position.
  - Yes/No/blank/1-5 values are not distinctive evidence (rule from the brief),
    so multiset-unique rating matches are capped at Probable.
  - SharePoint-side facts are all Unresolved until 03-sharepoint-schema/ holds a
    live schema export. Names quoted from the task brief are hints, not evidence.
  - executable == True requires BOTH sides Existing/Confirmed. Nothing else may
    reach generated executable output.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = "2026-07-28"

FORMS_INV = json.loads((ROOT / "01-forms-excel/sanitized/forms-question-inventory.json").read_text())
KEYS_INV = json.loads((ROOT / "02-get-response-details/sanitized/response-keys-inventory.json").read_text())

LABELS = {c["excel_column"]: c["label"] for c in FORMS_INV["columns"]}
KNOWN_KEYS = {k["response_key"] for k in KEYS_INV["keys"]}

R6 = "response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6"

# Candidate sets for ambiguous non-distinctive values in response 6
NO_KEYS = ["r516051da52cf4166a478cd83a6e15291", "r5f267e3e119041469c62a472d832324f",
           "rf76887b82f1f4414a41f5e65ecef7cbd", "r587705b554a5436aa6663834b1582469",
           "rbc83faed4a274e0fb254a5c4c21edd73"]
NO_COLS = [11, 17, 41, 43, 45]
ONE_KEYS = ["r90c6dc19b575459fa68b7a65b23a9a06", "re95a3bb4ed594260b8745180ba8d56a7"]
ONE_COLS = [32, 35]

# column -> (key, confidence, evidence)
KEY_ASSIGNMENTS = {
    7: ("r5caae6a11afb406a8e77e0b242fb4cab", "Confirmed",
        f"{R6}: distinctive dummy value 'Pilot a searchable online resource hub for schools.' "
        "matches exactly one column and exactly one key within the response."),
    9: ("r8718cecca56b4ed692e9042452d04195", "Confirmed",
        f"{R6}: only ISO-date value in the body ('2026-12-01') matches the only date answer in the row "
        "(Excel renders it as 2026-12-01 00:00:00)."),
    10: ("rf8348c8485dd40b08c00e76f66a3d428", "Confirmed",
         f"{R6}: distinctive dummy value 'Build in October, test in November, and pilot in December 2026.' "
         "matches exactly one column and one key."),
    15: ("r1da539bd1a494208849da87ee257c128", "Confirmed",
         f"{R6}: only JSON-array-serialized value in the body ('[\"Driver A1\"]') matches the multi-choice "
         "serialization of the row's Strategic Goals value ('Driver A1;'). The only other multi-choice "
         "question (Impacted Programme(s)) is blank in this response."),
    16: ("rf9f8fa67e4fb4dfead61d31cba86aa7a", "Confirmed",
         f"{R6}: deliberate marker value — plain string 'Driver A1' exactly matches the rationale column, "
         "and is structurally distinct from the JSON-array form carried by the Strategic Goals key."),
    34: ("rca68d3a0ad2b45c397fd0523414426b5", "Probable",
         f"{R6}: value '2' is unique within the response's four-rating multiset {{1,1,2,3}} and the row's "
         "answered ratings form the same multiset, with '2' on this column. Capped at Probable because "
         "the brief rules 1-5 values non-distinctive. Resolve with a distinct-permutation test submission."),
    36: ("r650d9f2a4d1f43e8938032a9cd60c658", "Confirmed",
         f"{R6}: distinctive dummy value 'Limited support is expected and no operational changes are "
         "planned.' matches exactly one column and one key."),
    37: ("r1903e1b8394140d19377b15fc81edd65", "Probable",
         f"{R6}: value '3' is unique within the response's four-rating multiset; same reasoning and same "
         "Probable cap as the Operational-support rating. Resolve with a distinct-permutation test submission."),
    38: ("r577a0e5e42554b6f8d82f7c24b8f183b", "Confirmed",
         f"{R6}: distinctive dummy value 'The reputational risk is currently uncertain.' matches exactly "
         "one column and one key."),
    39: ("rc12c559d019d4f9f9f8ed773c21c686f", "Confirmed",
         f"{R6}: distinctive dummy value 'Professional Learning team.' matches exactly one column and one key."),
    40: ("r5d267e063680468b8f77617ee0269b60", "Confirmed",
         f"{R6}: distinctive dummy value 'The team supported testing a small pilot.' matches exactly one "
         "column and one key."),
}

SP_UNRESOLVED = {
    "display_name": None, "internal_name": None, "type": None,
    "required": None, "allowed_choices": None,
    "confidence": "Unresolved",
    "evidence": ("No SharePoint schema evidence in the repository (03-sharepoint-schema/ is empty). "
                 "Internal names, types, required flags and choice sets must come from a live schema "
                 "export — see 03-sharepoint-schema/COLLECTION-INSTRUCTIONS.md."),
}

# Normalization rules are written against the *expected* SharePoint type named in
# the brief where one was named; each rule is conditional on schema confirmation.
NORMALIZATION = {
    "text": "Trim; blank answer -> omit/JSON null. Pass the value as a JSON object member "
            "(never string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.",
    "multiline": "Pass through unmodified (preserve line breaks); blank -> omit/JSON null. Object-member escaping as for text.",
    "date": "If SharePoint type is DateTime: send ISO 8601 (the key already carries 'yyyy-MM-dd'; "
            "add 'T00:00:00Z' only if the live field rejects date-only). Blank -> JSON null. NEVER send ''.",
    "rating": "If SharePoint type is Number: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.",
    "yesno": "If SharePoint type is Choice: pass 'Yes'/'No' verbatim after verifying live choice set. "
             "If Boolean: equals(value,'Yes'). Blank -> JSON null; never invent 'N/A' or false.",
    "multichoice_as_text": "Value arrives as a JSON-array *string* (e.g. '[\"A\",\"B\"]'). If the destination is "
                           "multiline text (as the brief indicates for StrategicGoals/ImpactedProgrammes): "
                           "join(json(value), '; '). If the live schema instead shows MultiChoice: "
                           "{'results': json(value)}. Blank -> omit/JSON null.",
    "file_upload": "Do NOT post to an ordinary list field expecting attachments to appear. Phase 1 scope: "
                   "either omit entirely, or store the raw answer string (uploaded-file names/URLs as provided "
                   "by Forms) in a text column explicitly labelled as a reference, not an attachment.",
    "none": "No destination proposed; nothing sent.",
}

TYPE_HINTS = {  # forms-side answer shape only; SharePoint type remains unresolved
    7: ("multiline", "free text"), 8: ("text", "free text"),
    9: ("date", "date"), 10: ("multiline", "free text"),
    11: ("yesno", "Yes/No"), 12: ("text", "free text"), 13: ("text", "free text"),
    14: ("text", "free text"), 15: ("multichoice_as_text", "multi-choice"),
    16: ("multiline", "free text"), 17: ("yesno", "Yes/No"), 18: ("text", "free text"),
    19: ("yesno", "Yes/No"), 20: ("yesno", "Yes/No"), 21: ("multiline", "free text"),
    22: ("none", "display-only notice (no input observed)"),
    23: ("rating", "rating 1-5"), 24: ("multiline", "free text"),
    25: ("rating", "rating 1-5"), 26: ("multiline", "free text"),
    27: ("multiline", "free text"), 28: ("multiline", "free text"),
    29: ("multiline", "free text"), 30: ("multichoice_as_text", "multi-choice"),
    31: ("multiline", "free text"), 32: ("rating", "rating 1-5"),
    33: ("multiline", "free text"), 34: ("rating", "rating 1-5"),
    35: ("rating", "rating 1-5"), 36: ("multiline", "free text"),
    37: ("rating", "rating 1-5"), 38: ("multiline", "free text"),
    39: ("multiline", "free text"), 40: ("multiline", "free text"),
    41: ("yesno", "Yes/No"), 42: ("multiline", "free text"),
    43: ("yesno", "Yes/No"), 44: ("multiline", "free text"),
    45: ("yesno", "Yes/No"), 46: ("multiline", "free text"),
    47: ("file_upload", "file upload"),
}


def question_entries():
    entries = []
    for col in range(7, 48):
        label = LABELS[col]
        norm_key, answer_shape = TYPE_HINTS[col]
        e = {
            "map_id": f"Q{col:02d}",
            "form_question_label": label,
            "excel_column": col,
            "forms_answer_shape": answer_shape,
            "forms_response_key": None,
            "forms_key_confidence": "Unresolved",
            "forms_key_evidence": None,
            "forms_key_candidates": None,
            "sharepoint": dict(SP_UNRESOLVED),
            "normalization": NORMALIZATION[norm_key],
            "executable": False,
            "notes": [],
        }
        if col in KEY_ASSIGNMENTS:
            key, conf, ev = KEY_ASSIGNMENTS[col]
            assert key in KNOWN_KEYS, f"key {key} not in observed body: {col}"
            e.update(forms_response_key=key, forms_key_confidence=conf, forms_key_evidence=ev)
        elif col in NO_COLS:
            e["forms_key_candidates"] = list(NO_KEYS)
            e["forms_key_evidence"] = (
                f"{R6}: this question was answered 'No', and the body holds exactly five 'No' values — "
                "the candidate keys listed. 'No' is not distinctive, so no individual assignment is possible. "
                "Resolve with a test submission answering Yes/No in a distinct known pattern.")
        elif col in ONE_COLS:
            e["forms_key_candidates"] = list(ONE_KEYS)
            e["forms_key_evidence"] = (
                f"{R6}: the two candidate keys both carry '1', matching this column and one other rating "
                "column. Resolve with a distinct-permutation ratings test submission.")
        else:
            e["forms_key_evidence"] = (
                "Blank in response 6, and blank Forms properties cannot be attributed to questions "
                "(30 blank keys vs 23 blank questions). Resolve by capturing the Get-response-details body "
                "for reference response 2, whose distinctive dummy answers cover most of these fields.")
        if col == 22:
            e["notes"].append(
                "Implementation Readiness Notice: blank in ALL six reference responses including the fully "
                "completed response 2, so it carries no respondent data. Determination: NO SharePoint "
                "destination required. Confirm against the live form that it is a text/section element "
                "without an input control; if the flow export shows it referenced anywhere, revisit.")
        if col == 47:
            e["notes"].append(
                "Phase 1 file scope: Forms uploads land in the form owner's OneDrive/SharePoint upload "
                "folder; the answer is a reference string, not transferable attachment content via a list "
                "field. Defined separately in the implementation instructions.")
        if col in (15, 30):
            e["notes"].append(
                "Brief indicates the likely destination is a multiline-text column "
                f"({'StrategicGoals' if col == 15 else 'ImpactedProgrammes'} named in the task brief — "
                "hint only, not schema evidence); serialize as joined text, not SharePoint multi-choice syntax.")
        entries.append(e)
    return entries


METADATA_MAPPINGS = [
    {
        "map_id": "M-RESPONDER",
        "source": "body('Get_response_details')?['responder']",
        "description": "Submitter email (Forms metadata, not an r-key).",
        "forms_key_confidence": "Confirmed",
        "forms_key_evidence": "Structural property of the Get-response-details body; observed populated in the "
                              "response-6 capture and corresponding to the Excel 'Email' metadata column.",
        "sharepoint": dict(SP_UNRESOLVED),
        "normalization": "Plain string. Only usable for a Person field via a lookup/claims resolution step — "
                         "do not post a bare email string to a Person column without testing.",
        "executable": False,
        "notes": ["Excel 'Name' column has no Get-response-details equivalent; derive from Office 365 Users "
                  "connector if needed, or leave to SharePoint Created By."],
    },
    {
        "map_id": "M-SUBMITDATE",
        "source": "body('Get_response_details')?['submitDate']",
        "description": "Submission timestamp (Forms metadata).",
        "forms_key_confidence": "Confirmed",
        "forms_key_evidence": "Structural property of the body. Observed 'M/d/yyyy h:mm:ss AM/PM' in UTC: the "
                              "response-6 capture shows 3:23:34 PM against the Excel completion time 17:23:34 "
                              "(tenant-local, UTC+2 at capture).",
        "sharepoint": dict(SP_UNRESOLVED),
        "normalization": "formatDateTime(..., 'yyyy-MM-ddTHH:mm:ssZ') — treat the source as UTC. Never send ''.",
        "executable": False,
        "notes": [],
    },
    {
        "map_id": "M-RESPONSEID",
        "source": "triggerOutputs()?['body/resourceData/responseId']",
        "description": "Form response ID — duplicate-prevention key and audit reference.",
        "forms_key_confidence": "Probable",
        "forms_key_evidence": "Documented output path of the 'When a new response is submitted' trigger; the "
                              "expression is the standard pattern but has not been verified against this flow's "
                              "export. The Excel ID column (1..6) shows the sequential IDs exist. Verify the exact "
                              "path in the live flow's Get-response-details 'Response Id' parameter.",
        "sharepoint": dict(SP_UNRESOLVED),
        "normalization": "Integer. Store as Number or single-line text; used for idempotency lookup before create.",
        "executable": False,
        "notes": ["Excel metadata 'Start time' and 'Last modified time' have no Get-response-details equivalent; "
                  "no destination proposed."],
    },
]

# Backend fields named in the brief's Word field model: NOT Form questions.
BACKEND_FIELDS = [
    {"name_hint": n, "layer": layer, "initial_create_behaviour": beh}
    for n, layer, beh in [
        ("Innovation Type", "AI-generated analysis", "Preserve the existing flow's AI/Select mapping once the flow export is in 04-existing-flow/; never source from raw Forms answers."),
        ("Horizon", "AI-generated analysis", "Same as Innovation Type."),
        ("Categorization", "AI-generated analysis", "Same as Innovation Type."),
        ("Ownership", "AI-generated analysis / governance", "Same as Innovation Type; confirm layer from flow export."),
        ("Projected-impact measures", "Human review / governance", "Intentionally blank at item creation."),
        ("Governance and review fields (incl. ReviewStatus)", "Human review / governance",
         "Intentionally blank except agreed defaults; ReviewStatus stays 'Not reviewed' unless the flow export proves a different working default."),
        ("Processing/audit fields (processing status, error detail)", "Processing and audit metadata",
         "Set by the flow itself per the error-handling design; internal names require schema evidence."),
        ("OriginalSubmission", "Processing and audit metadata",
         "Preserve the existing labelled-submission construction output verbatim once the flow export is available; do not reconstruct it."),
        ("FormResponseId (or equivalent)", "Processing and audit metadata",
         "Duplicate-prevention key. Whether a column exists is unknown — see evidence request; if absent, one must be added to the list before cutover."),
    ]
]


def main():
    spec = {
        "_meta": {
            "title": "Forms -> SharePoint 'Knowledge Submissions' mapping specification",
            "generated_by": "scripts/build_mapping_spec.py",
            "generated": GENERATED,
            "confidence_states": {
                "Existing": "Preserved from a working flow mapping (requires 04-existing-flow evidence).",
                "Confirmed": "Supported by authoritative structural or distinctive dummy-test evidence.",
                "Probable": "Strongly suggested but unproved; requires human resolution; NEVER executable.",
                "Unresolved": "Missing, ambiguous, obsolete, or contradictory.",
            },
            "executability_rule": "executable == true requires forms side AND SharePoint side each Existing or Confirmed. Enforced by scripts/validate_spec.py and scripts/generate_artifacts.py.",
            "evidence_sources": {
                "forms_excel": "01-forms-excel/sanitized/Innovation-Intake-Form-responses-reference.xlsx (6 dummy responses)",
                "get_response_details": "02-get-response-details/sanitized/get-response-details-response-6.body.json (dummy response 6)",
                "sharepoint_schema": "ABSENT — 03-sharepoint-schema/ empty",
                "existing_flow": "ABSENT — 04-existing-flow/ empty",
            },
            "layer_model": [
                "1 raw Forms answers (from Get response details only)",
                "2 AI-generated analysis (never overwrites raw fields)",
                "3 human review and governance (blank/defaults at creation)",
                "4 processing and audit metadata (set by the flow)",
            ],
        },
        "forms_metadata_mappings": METADATA_MAPPINGS,
        "question_mappings": question_entries(),
        "backend_fields_not_form_questions": BACKEND_FIELDS,
    }
    out = ROOT / "05-mapping-spec/mapping-spec.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    q = spec["question_mappings"]
    by_conf = {}
    for e in q:
        by_conf[e["forms_key_confidence"]] = by_conf.get(e["forms_key_confidence"], 0) + 1
    print("question mappings:", len(q), by_conf)
    print("executable:", sum(1 for e in q if e["executable"]))


if __name__ == "__main__":
    main()
