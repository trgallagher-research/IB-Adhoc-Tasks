#!/usr/bin/env python3
"""Build 05-mapping-spec/mapping-spec.json from the source inventories, the live
SharePoint schema evidence, and the evidence judgments encoded below.

The inventories/schema are mechanical extracts; this file is where mapping
*judgment* lives, so every non-Unresolved assignment carries its evidence
string. Rules enforced here and in scripts/validate_spec.py:

  - Confirmed requires distinctive-value, structural, or explicit-label-match
    evidence, never position.
  - Yes/No/blank/1-5 values are not distinctive evidence (rule from the brief),
    so multiset-unique rating matches are capped at Probable.
  - executable == True requires BOTH sides Existing/Confirmed AND every
    expression source evidenced (the unverified trigger response-ID path keeps
    FormResponseID out of executable output until the flow export lands).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = "2026-07-28"

FORMS_INV = json.loads((ROOT / "01-forms-excel/sanitized/forms-question-inventory.json").read_text())
KEYS_INV = json.loads((ROOT / "02-get-response-details/sanitized/response-keys-inventory.json").read_text())
SCHEMA = json.loads((ROOT / "03-sharepoint-schema/sanitized/knowledge-submissions-schema.json").read_text())

LABELS = {c["excel_column"]: c["label"] for c in FORMS_INV["columns"]}
KNOWN_KEYS = {k["response_key"] for k in KEYS_INV["keys"]}
FIELDS = {f["InternalName"]: f for f in SCHEMA["fields"]}

R6 = "response-6 correlation: Excel row ID 6 vs sanitized Get-response-details body for response 6"
SCHEMA_EV = ("Live schema export 2026-07-28 (03-sharepoint-schema/sanitized/"
             "knowledge-submissions-schema.json)")

# Candidate sets for ambiguous non-distinctive values in response 6
NO_KEYS = ["r516051da52cf4166a478cd83a6e15291", "r5f267e3e119041469c62a472d832324f",
           "rf76887b82f1f4414a41f5e65ecef7cbd", "r587705b554a5436aa6663834b1582469",
           "rbc83faed4a274e0fb254a5c4c21edd73"]
NO_COLS = [11, 17, 41, 43, 45]
ONE_KEYS = ["r90c6dc19b575459fa68b7a65b23a9a06", "re95a3bb4ed594260b8745180ba8d56a7"]
ONE_COLS = [32, 35]

# column -> (key, confidence, evidence)  — Forms side
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

# column -> SharePoint internal name — SharePoint side, evidenced by the live
# schema: each destination's display/internal name corresponds uniquely to the
# question label (explicit label match per project README); none has a
# competing candidate field.
SP_ASSIGNMENTS = {
    7: "OpportunityDescription", 8: "Sponsor", 9: "AnticipatedLaunchDate",
    10: "ImplementationTimeline", 11: "ExternalPartnerInvolved",
    12: "PartnerOrganisation", 13: "PartnerContactPerson", 14: "PartnerContactRole",
    15: "StrategicGoals", 16: "StrategicAlignmentRationale",
    17: "LocalMarketImpact", 18: "LocalMarketDetails",
    19: "ComplianceBoundaryAdaptation", 20: "ChiefSupportSecured",
    21: "ChiefSupportDetails",
    23: "StrategicImportanceScore", 24: "StrategicImportanceExplanation",
    25: "LocalizedServiceOfferingScore", 26: "LocalizedServiceOfferingExplanat",
    27: "ImpactDescription", 28: "DataEvidence", 29: "ExpectedEvidence",
    30: "ImpactedProgrammes", 31: "StakeholderFeedbackSummary",
    32: "FinancialImpactScore", 33: "FinancialImpactExplanation",
    34: "OperationalSupportScore", 35: "OperationalChangesScore",
    36: "OperationalImpactExplanation", 37: "ReputationalImpactScore",
    38: "ReputationalImpactExplanation", 39: "InternalStakeholdersConsulted",
    40: "InternalConsultationOutcomes", 41: "IBENImpact",
    42: "IBENImpactDescription", 43: "ProfessionalLearningImpact",
    44: "ProfessionalLearningImpactDescri", 45: "AdditionalFactors",
    46: "AdditionalFactorsDescription",
}
# Columns with confirmed NO SharePoint destination (absent from live schema):
NO_DESTINATION = {
    22: "Display-only notice element (blank in all six reference responses) and the live schema has no "
        "corresponding field. Determination: no destination required.",
    47: "File-upload answer. The live schema has no supporting-files column (only the standard Attachments "
        "facility). Phase 1 excludes file references from the payload — see implementation instructions.",
}


def sp_block(internal_name, extra_note=None):
    f = FIELDS[internal_name]
    ev = (f"{SCHEMA_EV}: field '{internal_name}' ({f['TypeAsString']}"
          f"{', DateOnly' if f.get('Format') == 'DateOnly' else ''}) — display name corresponds "
          "uniquely to this source; no competing candidate field.")
    if extra_note:
        ev += " " + extra_note
    return {
        "display_name": f["DisplayName"],
        "internal_name": internal_name,
        "type": f["TypeAsString"] + (" (DateOnly)" if f.get("Format") == "DateOnly" else ""),
        "required": f["Required"],
        "allowed_choices": f["Choices"],
        "default_value": f.get("DefaultValue"),
        "confidence": "Confirmed",
        "evidence": ev,
    }


NORMALIZATION = {
    "text": "Trim; blank answer -> JSON null. Pass the value as a JSON object member (never "
            "string-concatenated JSON) so quotes, apostrophes, line breaks and Unicode are escaped by the platform.",
    "multiline": "Pass through unmodified (preserve line breaks); blank -> JSON null. Object-member escaping as for text.",
    "date": "DateTime (DateOnly) destination: send the key's 'yyyy-MM-dd' string as-is. Blank -> JSON null. NEVER send ''.",
    "rating": "Number destination: int(value). Blank -> JSON null. NEVER send '' or 0 for unanswered.",
    "yesno": "Choice destination (choices verified in live schema): pass the answer string through verbatim "
             "('Yes'/'No', and for ComplianceBoundaryAdaptation also \"I don't know\"). Blank -> JSON null; "
             "never invent 'N/A' or false.",
    "multichoice_as_text": "Value arrives as a JSON-array *string* (e.g. '[\"A\",\"B\"]'). Destination is CONFIRMED "
                           "multiline text (Note): join(json(value), '; '). Blank -> JSON null.",
    "file_upload": "No list-field destination (confirmed). Phase 1: excluded from the payload entirely.",
    "none": "No destination (confirmed); nothing sent.",
}

TYPE_HINTS = {  # forms-side answer shape
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

OK = ("Existing", "Confirmed")


def question_entries():
    entries = []
    for col in range(7, 48):
        norm_key, answer_shape = TYPE_HINTS[col]
        e = {
            "map_id": f"Q{col:02d}",
            "form_question_label": LABELS[col],
            "excel_column": col,
            "forms_answer_shape": answer_shape,
            "forms_response_key": None,
            "forms_key_confidence": "Unresolved",
            "forms_key_evidence": None,
            "forms_key_candidates": None,
            "normalization": NORMALIZATION[norm_key],
            "executable": False,
            "notes": [],
        }
        if col in NO_DESTINATION:
            e["sharepoint"] = {
                "display_name": None, "internal_name": None, "type": None,
                "required": None, "allowed_choices": None,
                "confidence": "Confirmed",
                "evidence": f"{SCHEMA_EV}: {NO_DESTINATION[col]}",
                "no_destination": True,
            }
        else:
            e["sharepoint"] = sp_block(SP_ASSIGNMENTS[col])
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
        elif col not in NO_DESTINATION:
            e["forms_key_evidence"] = (
                "Blank in response 6, and blank Forms properties cannot be attributed to questions "
                "(30 blank keys vs 23 blank questions). Resolve by capturing the Get-response-details body "
                "for reference response 2, whose distinctive dummy answers cover most of these fields.")
        # executable: both sides Existing/Confirmed with a concrete key + name
        e["executable"] = (e["forms_key_confidence"] in OK
                           and e["forms_response_key"] is not None
                           and e["sharepoint"].get("internal_name") is not None
                           and e["sharepoint"]["confidence"] in OK)
        if col == 19:
            e["notes"].append("Live choice set includes a third option \"I don't know\" — pass-through, "
                              "never coerce to Yes/No.")
        if col in (15, 30):
            e["notes"].append("Destination CONFIRMED as multiline text (Note), not MultiChoice — "
                              "'; '-joined text serialization applies.")
        entries.append(e)
    return entries


METADATA_MAPPINGS = [
    {
        "map_id": "M-TITLE",
        "source": "Opportunity Description key (Q07) with a submitDate-based fallback",
        "description": "Required-by-convention Title, built by the flow.",
        "forms_key_confidence": "Confirmed",
        "forms_key_evidence": "Built solely from Confirmed sources: the Q07 key and the structural submitDate "
                              "property. (Live schema shows Title is not actually Required on this list; it is "
                              "populated anyway for usable views. Fallback deliberately avoids the trigger "
                              "response-ID path, which is unverified until the flow export lands.)",
        "sharepoint": sp_block("Title"),
        "normalization": "Opportunity Description truncated to 255 chars with ellipsis; if blank, "
                         "'Form submission <submitDate>'. Never null, never ''.",
        "executable": True,
        "notes": ["Linked-title view column displays as 'Opportunity'."],
    },
    {
        "map_id": "M-RESPONDER",
        "source": "body('Get_response_details')?['responder']",
        "description": "Submitter email (Forms metadata, not an r-key).",
        "forms_key_confidence": "Confirmed",
        "forms_key_evidence": "Structural property of the Get-response-details body; observed populated in the "
                              "response-6 capture and corresponding to the Excel 'Email' metadata column.",
        "sharepoint": sp_block("Respondent"),
        "normalization": "Plain string into the Text column. (Not a Person field — no claims resolution needed.)",
        "executable": True,
        "notes": ["Excel 'Name' column has no Get-response-details equivalent; no destination exists for it "
                  "in the live schema either."],
    },
    {
        "map_id": "M-SUBMITDATE",
        "source": "body('Get_response_details')?['submitDate']",
        "description": "Submission timestamp (Forms metadata).",
        "forms_key_confidence": "Confirmed",
        "forms_key_evidence": "Structural property of the body. Observed 'M/d/yyyy h:mm:ss AM/PM' in UTC: the "
                              "response-6 capture shows 3:23:34 PM against the Excel completion time 17:23:34 "
                              "(tenant-local, UTC+2 at capture).",
        "sharepoint": sp_block("SubmittedDate"),
        "normalization": "concat(formatDateTime(value, 'yyyy-MM-ddTHH:mm:ss'), 'Z') — source is UTC. Never ''.",
        "executable": True,
        "notes": [],
    },
    {
        "map_id": "M-RESPONSEID",
        "source": "triggerOutputs()?['body/resourceData/responseId']",
        "description": "Form response ID — duplicate-prevention key and audit reference.",
        "forms_key_confidence": "Probable",
        "forms_key_evidence": "Documented output path of the 'When a new response is submitted' trigger; the "
                              "standard pattern, but NOT yet verified against this flow's export — so this "
                              "mapping stays out of executable output despite its destination being Confirmed. "
                              "Verify via 04-existing-flow evidence (trigger.json / get-response-details.json).",
        "sharepoint": sp_block("FormResponseID",
                               extra_note="NOTE: Text column, not Number — send the ID as a quoted string and "
                                          "quote it in the duplicate-check $filter."),
        "normalization": "string(response ID) into the Text column. Duplicate-check filter: "
                         "FormResponseID eq '<id>'.",
        "executable": False,
        "notes": [],
    },
]

BACKEND_FIELDS = [
    {"internal_names": ["AISummary", "Topics", "KeyFindings", "Examples", "OpenQuestions",
                        "DifferentPerspectives", "ClaimsToVerify", "RelatedKnowledge", "FullAIOutput"],
     "layer": "AI-generated analysis",
     "initial_create_behaviour": "Preserve the existing flow's AI/Select mappings once the flow export is in "
                                 "04-existing-flow/; never source from raw Forms answers."},
    {"internal_names": ["HumanReviewRequired", "HumanReviewReason", "ReviewStatus"],
     "layer": "Human review and governance",
     "initial_create_behaviour": "Not in the raw-answer payload. ReviewStatus default 'Not reviewed' is CONFIRMED "
                                 "by the live schema (column default) — omitting it from the payload applies it. "
                                 "HumanReviewRequired defaults to No (0); whether the flow's AI branch overrides "
                                 "it awaits the flow export."},
    {"internal_names": ["ProcessingStatus", "ProcessedDate", "ProcessingError", "PromptVersion", "SourceForm"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "ProcessingStatus choices Received/Processing/Processed/Failed with column "
                                 "default 'Processed' (confirmed); SourceForm defaults to the form name; "
                                 "PromptVersion defaults '1.0'. Whether the flow sets these explicitly awaits "
                                 "the flow export — until then the payload omits them and defaults apply."},
    {"internal_names": ["OriginalSubmission"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "Destination CONFIRMED (Note). Source expression is the existing "
                                 "labelled-submission construction — preserved verbatim once the flow export is "
                                 "available; absent from the payload until then."},
    {"internal_names": ["FormResponseID", "SubmittedDate", "Respondent"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "All three CONFIRMED to exist. SubmittedDate/Respondent are executable now; "
                                 "FormResponseID awaits trigger-expression verification (see M-RESPONSEID)."},
]


def main():
    spec = {
        "_meta": {
            "title": "Forms -> SharePoint 'Knowledge Submissions' mapping specification",
            "generated_by": "scripts/build_mapping_spec.py",
            "generated": GENERATED,
            "confidence_states": {
                "Existing": "Preserved from a working flow mapping (requires 04-existing-flow evidence).",
                "Confirmed": "Supported by authoritative structural, distinctive dummy-test, or unique "
                             "label-match evidence.",
                "Probable": "Strongly suggested but unproved; requires human resolution; NEVER executable.",
                "Unresolved": "Missing, ambiguous, obsolete, or contradictory.",
            },
            "executability_rule": "executable == true requires forms side AND SharePoint side each "
                                  "Existing/Confirmed, with every expression source evidenced. Enforced by "
                                  "scripts/validate_spec.py and scripts/generate_artifacts.py.",
            "evidence_sources": {
                "forms_excel": "01-forms-excel/sanitized/Innovation-Intake-Form-responses-reference.xlsx (6 dummy responses)",
                "get_response_details": "02-get-response-details/sanitized/get-response-details-response-6.body.json (dummy response 6)",
                "sharepoint_schema": "03-sharepoint-schema/sanitized/knowledge-submissions-schema.json (live export 2026-07-28)",
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
        "system_fields_excluded": SCHEMA["system_fields_excluded_from_payload"],
    }
    out = ROOT / "05-mapping-spec/mapping-spec.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    q = spec["question_mappings"]
    by_conf = {}
    for e in q:
        by_conf[e["forms_key_confidence"]] = by_conf.get(e["forms_key_confidence"], 0) + 1
    n_exec = sum(1 for e in q if e["executable"]) + sum(1 for e in METADATA_MAPPINGS if e["executable"])
    print("question mappings:", len(q), by_conf)
    print("executable (incl. metadata/Title):", n_exec)


if __name__ == "__main__":
    main()
