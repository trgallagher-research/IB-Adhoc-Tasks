#!/usr/bin/env python3
"""Build 05-mapping-spec/mapping-spec.json from the source inventories, the live
SharePoint schema evidence, the existing-flow evidence, and the judgments below.

Evidence state (2026-07-28): all three primary sources are in:
  - Forms Excel reference (structure + dummy responses)
  - Get-response-details body for response 6 (48 opaque keys)
  - Live SharePoint schema (all internal names/types/choices/defaults)
  - Existing flow Peek-code captures (04-existing-flow/sanitized/): the
    labelled-submission construction pairs EVERY question label with its
    response key, and Create item holds the working flow-layer mappings.

Rules enforced here and in scripts/validate_spec.py:
  - Existing = preserved from the working flow's own label->key pairing or
    Create item parameters. Never derived from field order.
  - The dummy-test correlations of response 6 independently CORROBORATE the
    flow evidence (9 Confirmed matches, 2 Probables resolved consistently,
    candidate sets bijective) — zero contradictions.
  - executable == True requires BOTH sides Existing/Confirmed with all
    expression sources evidenced.
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

FLOW_EV = ("Existing-flow evidence 2026-07-28 (04-existing-flow/sanitized/run-a-prompt.json): the "
           "labelled-submission construction explicitly pairs this question label with this key")
SCHEMA_EV = ("Live schema export 2026-07-28 (03-sharepoint-schema/sanitized/"
             "knowledge-submissions-schema.json)")
R6 = "response-6 dummy-test correlation"

# column -> key, from the flow's labelled-submission construction (label->key
# pairing, NOT order). corroborated: independent dummy-test evidence agrees.
FLOW_KEYS = {
    7:  ("r5caae6a11afb406a8e77e0b242fb4cab", "corroborated"),
    8:  ("r8140da6e45c84dbcab391c05346d9b16", None),
    9:  ("r8718cecca56b4ed692e9042452d04195", "corroborated"),
    10: ("rf8348c8485dd40b08c00e76f66a3d428", "corroborated"),
    11: ("r587705b554a5436aa6663834b1582469", "candidate-set-consistent"),
    12: ("rf7cbe61f26ab41cfa28f0b2a009e9d7c", None),
    13: ("r072e0a054db54072b75c27d3d8e90140", None),
    14: ("r685fa8b221f64f9188951dfb6fb629ec", None),
    15: ("r1da539bd1a494208849da87ee257c128", "corroborated"),
    16: ("rf9f8fa67e4fb4dfead61d31cba86aa7a", "corroborated"),
    17: ("r516051da52cf4166a478cd83a6e15291", "candidate-set-consistent"),
    18: ("rf81976cae03249ef86d0d299bf126aac", None),
    19: ("r9ec31f96e7b34fb791c734433bb022a3", None),
    20: ("rf0bccf6e481343d1823057965c3271ea", None),
    21: ("r0b456ff26ee24c11a9503908ffea1b53", None),
    22: ("r8d49a8bdd5e94aee82f332fcab962a51", None),
    23: ("rfb959d52f2494d1b92e07856edeee015", None),
    24: ("re8d27932c227466996dbc77f67f71faa", None),
    25: ("r809645c3237a4bb4969b8082026cb3cc", None),
    26: ("r3e390836da294861a927ce63c8d0f2c6", None),
    27: ("rf703806487ab4148994d2fd2edb79941", None),
    28: ("r75f4515f78d946ac8a4274c151307c3e", None),
    29: ("rbb5f5979ba74480fba871dbaaeb381e9", None),
    30: ("rd668321450304780986d33d7e6f474b9", None),
    31: ("rba40cea72cef44df9c70637d7473d033", None),
    32: ("r90c6dc19b575459fa68b7a65b23a9a06", "candidate-pair-consistent"),
    33: ("ra89a8e77654b43a6af62ff1247df9f8f", None),
    34: ("rca68d3a0ad2b45c397fd0523414426b5", "probable-resolved"),
    35: ("re95a3bb4ed594260b8745180ba8d56a7", "candidate-pair-consistent"),
    36: ("r650d9f2a4d1f43e8938032a9cd60c658", "corroborated"),
    37: ("r1903e1b8394140d19377b15fc81edd65", "probable-resolved"),
    38: ("r577a0e5e42554b6f8d82f7c24b8f183b", "corroborated"),
    39: ("rc12c559d019d4f9f9f8ed773c21c686f", "corroborated"),
    40: ("r5d267e063680468b8f77617ee0269b60", "corroborated"),
    41: ("r5f267e3e119041469c62a472d832324f", "candidate-set-consistent"),
    42: ("r011318f6666745c891df6ed52af394b0", None),
    43: ("rf76887b82f1f4414a41f5e65ecef7cbd", None),
    44: ("r074e7a91d52747519a8fe0e9af68e7dd", None),
    45: ("rbc83faed4a274e0fb254a5c4c21edd73", None),
    46: ("r90a4a472716942dfa4b9d5de21931774", None),
    47: ("r7ba397b729054a109e0b046c38744e73", None),
}
CORROBORATION = {
    "corroborated": f" Independently CORROBORATED by {R6} (distinctive dummy value).",
    "probable-resolved": f" Resolves the prior Probable from {R6} (multiset-unique rating) — consistent.",
    "candidate-set-consistent": f" Consistent with the prior five-way 'No' candidate set from {R6} (bijective resolution).",
    "candidate-pair-consistent": f" Consistent with the prior two-way '1' candidate pair from {R6}.",
}

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
NO_DESTINATION = {
    22: "Display-only notice element: its key is now identified from the flow (always blank in every "
        "observed response; included in the AI prompt text) but the live schema has no corresponding "
        "field. Determination: no per-column destination; its (blank) line remains inside the "
        "OriginalSubmission labelled text, as in the existing flow.",
    47: "File-upload answer: key identified from the flow. No supporting-files column exists (only the "
        "standard Attachments facility). Phase 1: excluded from per-column payload; the raw answer "
        "string remains inside the OriginalSubmission labelled text, as in the existing flow.",
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
    "file_upload": "No per-column destination (confirmed). Phase 1: excluded from the payload; raw string "
                   "remains inside OriginalSubmission.",
    "none": "No destination (confirmed); nothing sent per-column.",
}

TYPE_HINTS = {
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
        key, corro = FLOW_KEYS[col]
        assert key in KNOWN_KEYS, f"flow key {key} not in observed body (col {col})"
        ev = f"{FLOW_EV} ('{LABELS[col][:60]}')." + (CORROBORATION.get(corro, "") if corro else "")
        e = {
            "map_id": f"Q{col:02d}",
            "form_question_label": LABELS[col],
            "excel_column": col,
            "forms_answer_shape": answer_shape,
            "forms_response_key": key,
            "forms_key_confidence": "Existing",
            "forms_key_evidence": ev,
            "normalization": NORMALIZATION[norm_key],
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
        e["executable"] = (e["sharepoint"].get("internal_name") is not None)
        if col == 19:
            e["notes"].append("Live choice set includes a third option \"I don't know\" — pass-through, "
                              "never coerce to Yes/No.")
        if col in (15, 30):
            e["notes"].append("Destination CONFIRMED as multiline text (Note), not MultiChoice — "
                              "'; '-joined text serialization applies.")
        entries.append(e)
    return entries


TRIGGER_EV = ("VERIFIED in the flow captures: used as Get response details' response_id parameter, in the "
              "labelled-submission text, and in Create item's FormResponseID parameter "
              "(04-existing-flow/sanitized/).")

METADATA_MAPPINGS = [
    {
        "map_id": "M-TITLE",
        "source": "Opportunity Description key (Q07), truncated, with response-ID fallback",
        "description": "Title (linked-title displays as 'Opportunity').",
        "forms_key_confidence": "Existing",
        "forms_key_evidence": "Existing flow maps Title = raw Q07 key (create-item.json). DELIBERATE DEVIATION "
                              "in the replacement: truncate to 255 chars with ellipsis (the existing raw mapping "
                              "fails at runtime for descriptions over the Text-255 limit) and fall back to "
                              "'Form response <id>' when blank. " + TRIGGER_EV,
        "sharepoint": sp_block("Title"),
        "normalization": "Truncate at 255 with '...'; blank -> 'Form response <id>'. Never null, never ''.",
        "executable": True,
        "notes": [],
    },
    {
        "map_id": "M-RESPONDER",
        "source": "body('Get_response_details')?['responder']",
        "description": "Submitter email (Forms metadata).",
        "forms_key_confidence": "Existing",
        "forms_key_evidence": "Existing flow maps Respondent = responder verbatim (create-item.json); also a "
                              "structural body property corroborated by the response-6 capture.",
        "sharepoint": sp_block("Respondent"),
        "normalization": "Plain string into the Text column (verbatim, as in the existing flow).",
        "executable": True,
        "notes": [],
    },
    {
        "map_id": "M-SUBMITDATE",
        "source": "body('Get_response_details')?['submitDate']",
        "description": "Submission timestamp (Forms metadata).",
        "forms_key_confidence": "Existing",
        "forms_key_evidence": "Existing flow posts the raw 'M/d/yyyy h:mm:ss AM/PM' UTC string to SubmittedDate "
                              "(create-item.json). DELIBERATE DEVIATION in the replacement: normalize to ISO 8601 "
                              "UTC (same instant, explicit format) because the REST endpoint is stricter than the "
                              "connector about date parsing.",
        "sharepoint": sp_block("SubmittedDate"),
        "normalization": "concat(formatDateTime(value, 'yyyy-MM-ddTHH:mm:ss'), 'Z') — source is UTC. Never ''.",
        "executable": True,
        "notes": [],
    },
    {
        "map_id": "M-RESPONSEID",
        "source": "triggerOutputs()?['body/resourceData/responseId']",
        "description": "Form response ID — duplicate-prevention key and audit reference.",
        "forms_key_confidence": "Existing",
        "forms_key_evidence": TRIGGER_EV,
        "sharepoint": sp_block("FormResponseID",
                               extra_note="Text column — send as string; quote it in the duplicate-check $filter."),
        "normalization": "string(response ID) into the Text column. Duplicate-check filter: FormResponseID eq '<id>'.",
        "executable": True,
        "notes": [],
    },
    {
        "map_id": "M-ORIGINALSUBMISSION",
        "source": "outputs('Compose_labelled_submission') — the existing labelled-submission text, preserved verbatim",
        "description": "Full labelled raw submission (audit layer).",
        "forms_key_confidence": "Existing",
        "forms_key_evidence": "The labelled-submission construction is captured verbatim in "
                              "04-existing-flow/sanitized/run-a-prompt.json (SubmissionText). The existing flow "
                              "builds it inline in the AI action and does NOT store it; the replacement moves it "
                              "into a Compose_labelled_submission action referenced by BOTH the AI prompt and "
                              "this property, closing the audit gap without changing the text.",
        "sharepoint": sp_block("OriginalSubmission"),
        "normalization": "Verbatim template output (generated to 06-generated-output/compose-labelled-submission.txt).",
        "executable": True,
        "notes": [],
    },
]

# Flow-layer mappings preserved VERBATIM from the existing Create item — the
# HTTP payload replaces that action, so it must carry these too.
FLOW_LAYER_EV = "Existing Create item parameter, preserved verbatim (04-existing-flow/sanitized/create-item.json)."
FLOW_LAYER_MAPPINGS = [
    {"internal_name": "SourceForm", "expression": None, "constant": "Innovation Intake Form (Knowledge-Bank)"},
    {"internal_name": "AISummary", "expression": "outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/summary']"},
    {"internal_name": "Topics", "expression": "join(body('Select_Topics'), decodeUriComponent('%0A'))"},
    {"internal_name": "KeyFindings", "expression": "join(body('Select_Key_Findings'), decodeUriComponent('%0A'))"},
    {"internal_name": "Examples", "expression": "join(body('Select_Examples'), decodeUriComponent('%0A'))"},
    {"internal_name": "OpenQuestions", "expression": "join(body('Select_Open_Questions'), decodeUriComponent('%0A'))"},
    {"internal_name": "DifferentPerspectives", "expression": "join(body('Select_Different_Perspectives'), decodeUriComponent('%0A'))"},
    {"internal_name": "ClaimsToVerify", "expression": "join(body('Select_Claims_To_Verify'), decodeUriComponent('%0A'))"},
    {"internal_name": "RelatedKnowledge", "expression": "join(body('Select_Related_Knowledge'), decodeUriComponent('%0A'))"},
    {"internal_name": "HumanReviewRequired", "expression": "outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/humanReviewRequired']"},
    {"internal_name": "HumanReviewReason", "expression": "outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/humanReviewReason']"},
    {"internal_name": "ReviewStatus", "expression": None, "constant": "Not reviewed"},
    {"internal_name": "FullAIOutput", "expression": "outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text']"},
    {"internal_name": "ProcessingStatus", "expression": None, "constant": "Processed"},
    {"internal_name": "ProcessedDate", "expression": "utcNow()"},
    {"internal_name": "PromptVersion", "expression": None, "constant": "Knowledge Submission Analyser v1\n",
     "note": "Trailing newline preserved verbatim from the working flow (quirk; trim only as a reviewed change)."},
    {"internal_name": "ContentTypeId", "expression": None,
     "constant": "0x01002470676DA4BBF5468468EDBF918DE47C0082A052FA62248A4A84337267D7DD930B",
     "note": "REST equivalent of the connector's item/{ContentType}/Id parameter."},
]
for m in FLOW_LAYER_MAPPINGS:
    m.update(confidence="Existing", evidence=FLOW_LAYER_EV, executable=True)

BACKEND_FIELDS = [
    {"internal_names": ["AISummary", "Topics", "KeyFindings", "Examples", "OpenQuestions",
                        "DifferentPerspectives", "ClaimsToVerify", "RelatedKnowledge", "FullAIOutput"],
     "layer": "AI-generated analysis",
     "initial_create_behaviour": "Preserved verbatim from the existing Create item (see flow_layer_mappings); "
                                 "sourced from Run_a_prompt / Select actions, never from raw Forms answers."},
    {"internal_names": ["HumanReviewRequired", "HumanReviewReason", "ReviewStatus"],
     "layer": "Human review and governance",
     "initial_create_behaviour": "HumanReview* come from the AI output (existing mapping, preserved). "
                                 "ReviewStatus is explicitly set to 'Not reviewed' by the existing flow, "
                                 "matching the column default — preserved."},
    {"internal_names": ["ProcessingStatus", "ProcessedDate", "ProcessingError", "PromptVersion", "SourceForm"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "ProcessingStatus 'Processed', ProcessedDate utcNow(), PromptVersion and "
                                 "SourceForm constants — all explicitly set by the existing flow, preserved. "
                                 "ProcessingError is NOT set by the existing flow; the new error-handling design "
                                 "writes it only on the catch path."},
    {"internal_names": ["OriginalSubmission"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "NOT populated by the existing flow (gap). The replacement stores the preserved "
                                 "labelled-submission text here — see M-ORIGINALSUBMISSION."},
    {"internal_names": ["FormResponseID", "SubmittedDate", "Respondent"],
     "layer": "Processing and audit metadata",
     "initial_create_behaviour": "All three preserved from the existing Create item; all executable."},
]


def main():
    spec = {
        "_meta": {
            "title": "Forms -> SharePoint 'Knowledge Submissions' mapping specification",
            "generated_by": "scripts/build_mapping_spec.py",
            "generated": GENERATED,
            "confidence_states": {
                "Existing": "Preserved from a working flow mapping (04-existing-flow evidence).",
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
                "existing_flow": "04-existing-flow/sanitized/ (Peek-code captures 2026-07-28: trigger, "
                                 "Get response details, Run a prompt incl. labelled-submission construction, "
                                 "3 of 8 Select actions, Create item)",
            },
            "cross_validation": "The flow's label->key pairings agree with ALL prior dummy-test evidence: 9 "
                                "Confirmed matches, both Probables resolved as predicted, the five-way 'No' set "
                                "and two-way '1' pair resolve bijectively. 41 flow keys + 7 permanently-blank "
                                "surplus keys = 48 observed keys exactly.",
            "layer_model": [
                "1 raw Forms answers (from Get response details only)",
                "2 AI-generated analysis (never overwrites raw fields)",
                "3 human review and governance (defaults/AI at creation)",
                "4 processing and audit metadata (set by the flow)",
            ],
        },
        "forms_metadata_mappings": METADATA_MAPPINGS,
        "question_mappings": question_entries(),
        "flow_layer_mappings": FLOW_LAYER_MAPPINGS,
        "backend_fields_not_form_questions": BACKEND_FIELDS,
        "system_fields_excluded": SCHEMA["system_fields_excluded_from_payload"],
    }
    out = ROOT / "05-mapping-spec/mapping-spec.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    q = spec["question_mappings"]
    by_conf = {}
    for e in q:
        by_conf[e["forms_key_confidence"]] = by_conf.get(e["forms_key_confidence"], 0) + 1
    n_exec = (sum(1 for e in q if e["executable"])
              + sum(1 for e in METADATA_MAPPINGS if e["executable"])
              + len(FLOW_LAYER_MAPPINGS))
    assigned = {e["forms_response_key"] for e in q}
    surplus = sorted(KNOWN_KEYS - assigned)
    print("question mappings:", len(q), by_conf)
    print("executable properties (questions + metadata + flow-layer):", n_exec)
    print("surplus unexplained keys:", len(surplus))


if __name__ == "__main__":
    main()
