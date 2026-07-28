#!/usr/bin/env python3
"""Render human-readable reports from 05-mapping-spec/mapping-spec.json.

Outputs (regenerated, do not hand-edit):
  05-mapping-spec/mapping-spec.md
  05-mapping-spec/unresolved-mappings.md
  05-mapping-spec/coverage-report.md
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "05-mapping-spec/mapping-spec.json").read_text())
KEYS_INV = json.loads((ROOT / "02-get-response-details/sanitized/response-keys-inventory.json").read_text())
GENERATED = SPEC["_meta"]["generated"]

Q = SPEC["question_mappings"]
META = SPEC["forms_metadata_mappings"]
BACKEND = SPEC["backend_fields_not_form_questions"]


def sp_cell(e):
    sp = e["sharepoint"]
    if sp["internal_name"]:
        return f"`{sp['internal_name']}` ({sp['type']}, {sp['confidence']})"
    return f"Unresolved — no schema evidence"


def mapping_spec_md():
    md = [
        "# Mapping specification — Forms → SharePoint `Knowledge Submissions`",
        "",
        f"Generated {GENERATED} by `scripts/build_reports.py` from `mapping-spec.json` "
        "(the machine-readable source of truth). Do not hand-edit; edit the spec builder "
        "and regenerate.",
        "",
        "## Confidence states",
        "",
    ]
    for k, v in SPEC["_meta"]["confidence_states"].items():
        md.append(f"- **{k}** — {v}")
    md += [
        "",
        f"**Executability rule:** {SPEC['_meta']['executability_rule']}",
        "",
        "## Evidence base",
        "",
    ]
    for k, v in SPEC["_meta"]["evidence_sources"].items():
        md.append(f"- `{k}`: {v}")
    md += [
        "",
        "The SharePoint side is **Confirmed for every mapping** from the live schema "
        "export of 2026-07-28 (unique label correspondence, types, required flags and "
        "choice sets). Executability now turns on the Forms side and on expression-source "
        "verification.",
        "",
        "## Forms metadata mappings",
        "",
        "| ID | Source expression | Forms conf. | SharePoint | Normalization |",
        "|----|-------------------|-------------|------------|---------------|",
    ]
    for e in META:
        md.append(f"| {e['map_id']} | `{e['source']}` | {e['forms_key_confidence']} | "
                  f"{sp_cell(e)} | {e['normalization'][:140]} |")
    md += [
        "",
        "## Question mappings (Excel columns 7–47)",
        "",
        "| ID | Question label | Answer shape | Forms response key | Forms conf. | SharePoint | Executable |",
        "|----|----------------|--------------|--------------------|-------------|------------|------------|",
    ]
    for e in Q:
        key = f"`{e['forms_response_key']}`" if e["forms_response_key"] else (
            f"candidates: {len(e['forms_key_candidates'])}" if e["forms_key_candidates"] else "—")
        md.append(f"| {e['map_id']} | {e['form_question_label'][:70]} | {e['forms_answer_shape']} | "
                  f"{key} | {e['forms_key_confidence']} | {sp_cell(e)} | "
                  f"{'yes' if e['executable'] else 'no'} |")
    md += ["", "## Evidence detail (Confirmed and Probable rows)", ""]
    for e in META + Q:
        if e["forms_key_confidence"] in ("Confirmed", "Probable", "Existing"):
            label = e.get("form_question_label") or e.get("description")
            md += [f"### {e['map_id']} — {label}", "",
                   f"- Confidence: **{e['forms_key_confidence']}**",
                   f"- Evidence: {e['forms_key_evidence']}",
                   f"- Normalization: {e['normalization']}"]
            for n in e["notes"]:
                md.append(f"- Note: {n}")
            md.append("")
    md += ["## Backend fields — not Form questions (internal names evidenced by live schema)", "",
           "| Fields | Layer | Behaviour at item creation |",
           "|--------|-------|----------------------------|"]
    for b in BACKEND:
        names = ", ".join(f"`{n}`" for n in b["internal_names"])
        md.append(f"| {names} | {b['layer']} | {b['initial_create_behaviour']} |")
    md.append("")
    return "\n".join(md)


def unresolved_md():
    unresolved = [e for e in Q if e["forms_key_confidence"] == "Unresolved"]
    probable = [e for e in Q if e["forms_key_confidence"] == "Probable"]
    md = [
        "# Unresolved mappings report",
        "",
        f"Generated {GENERATED} by `scripts/build_reports.py`. Every row here is excluded "
        "from executable output. Resolution paths are in `EVIDENCE-REQUEST.md`.",
        "",
        "## A. SharePoint side — RESOLVED (live schema export 2026-07-28)",
        "",
        "Every SharePoint internal name, type, required flag and choice set is now "
        "Confirmed from `03-sharepoint-schema/sanitized/knowledge-submissions-schema.json`. "
        "Remaining unresolved items are Forms-side keys and flow-layer expressions only.",
        "",
        "## B. Probable Forms keys (human resolution required; not executable)",
        "",
        "| ID | Question | Candidate key | Why capped at Probable |",
        "|----|----------|---------------|------------------------|",
    ]
    for e in probable:
        md.append(f"| {e['map_id']} | {e['form_question_label'][:60]} | "
                  f"`{e['forms_response_key']}` | 1–5 rating values are ruled "
                  "non-distinctive; multiset-unique match only. |")
    md += [
        "",
        "## C. Unresolved Forms keys with known candidate sets",
        "",
        "Ambiguity within response 6 (values 'No' and '1' are non-distinctive):",
        "",
        "| ID | Question | Candidate keys |",
        "|----|----------|----------------|",
    ]
    for e in unresolved:
        if e["forms_key_candidates"]:
            keys = ", ".join(f"`{k}`" for k in e["forms_key_candidates"])
            md.append(f"| {e['map_id']} | {e['form_question_label'][:60]} | {keys} |")
    md += [
        "",
        "## D. Unresolved Forms keys with no candidate evidence",
        "",
        "Blank in response 6; blank properties cannot be attributed to questions. "
        "Most will resolve from a capture of reference response 2 (richly distinctive "
        "dummy content).",
        "",
        "| ID | Question |",
        "|----|----------|",
    ]
    for e in unresolved:
        if not e["forms_key_candidates"]:
            md.append(f"| {e['map_id']} | {e['form_question_label'][:80]} |")
    md += [
        "",
        "## E. Flow-layer items awaiting the flow export",
        "",
        "- `OriginalSubmission` source expression (labelled-submission construction) — must be "
        "preserved, not reconstructed.",
        "- AI Builder / Select action mappings for Innovation Type, Horizon, Categorization, Ownership.",
        "- The working default written to `ReviewStatus` (assumed 'Not reviewed'; unproven).",
        "- The exact trigger expression for the Form response ID.",
        "",
    ]
    return "\n".join(md)


def coverage_md():
    conf = [e for e in Q if e["forms_key_confidence"] == "Confirmed"]
    prob = [e for e in Q if e["forms_key_confidence"] == "Probable"]
    unres = [e for e in Q if e["forms_key_confidence"] == "Unresolved"]
    cand_pool = sorted({k for e in Q if e["forms_key_candidates"] for k in e["forms_key_candidates"]})
    assigned = {e["forms_response_key"] for e in Q if e["forms_response_key"]}
    totals = KEYS_INV["_provenance"]["totals"]
    blank = totals["blank"]
    unaccounted = totals["opaque_r_keys"] - len(assigned) - len(cand_pool) - blank

    md = [
        "# Coverage report",
        "",
        f"Generated {GENERATED} by `scripts/build_reports.py` from `mapping-spec.json` and the "
        "response-key inventory.",
        "",
        "## Totals reconciliation",
        "",
        "| Population | Count | Breakdown |",
        "|------------|-------|-----------|",
        f"| Excel columns | 47 | 6 Forms metadata + 41 questions |",
        f"| Question mappings | {len(Q)} | {len(conf)} Confirmed + {len(prob)} Probable + {len(unres)} Unresolved (Forms side) |",
        f"| Opaque `r…` keys | {totals['opaque_r_keys']} | {len(assigned)} assigned (Confirmed+Probable) + "
        f"{len(cand_pool)} in candidate pools + {blank} blank/unattributable + {unaccounted} otherwise unaccounted |",
        f"| Executable mappings | {sum(1 for e in Q if e['executable']) + sum(1 for e in META if e['executable'])} | "
        f"{sum(1 for e in Q if e['executable'])} question + "
        f"{sum(1 for e in META if e['executable'])} metadata/Title (both sides Confirmed) |",
        "",
        "Key-count arithmetic: 48 keys − 41 questions = **at least 7 surplus keys** even if "
        "every question maps 1:1; with 30 blank keys against 23 unanswered questions in "
        "response 6, the surplus is consistent but the specific surplus keys cannot be "
        "identified from current evidence.",
        "",
        "## 1. Form fields without a SharePoint destination",
        "",
        "- **Implementation Readiness Notice (Q22)** — determined to need NO destination: blank in "
        "all six reference responses including the fully completed one, so it is a display-only "
        "element. (Verify once against the live form.)",
        "- **Add any supporting files (Q47)** — no ordinary-field destination; Phase 1 treats file "
        "references separately (see implementation instructions).",
        "- **Excel metadata 'Start time' and 'Last modified time'** — no Get-response-details "
        "equivalent; no destination proposed.",
        "- **Excel metadata 'Name'** — no Get-response-details equivalent (only `responder` email); "
        "destination undecided.",
        "- All other question fields have an *intended* destination that is Unresolved pending schema "
        "evidence — they are not 'no destination' cases.",
        "",
        "## 2. SharePoint fields without Form sources (from the live schema)",
        "",
        "Flow-constructed / control fields: `Title` (from Q07 + fallback), `FormResponseID` "
        "(response ID; pending trigger verification), `SubmittedDate`, `Respondent`, "
        "`SourceForm` (column default), `OriginalSubmission` (existing flow expression, pending "
        "flow export). AI-layer, governance and processing fields are listed in the backend "
        "table of the mapping spec — none is sourced from raw Forms answers.",
        "",
        "## 3. Unexplained Forms keys",
        "",
        f"- {blank} keys are blank in response 6 and unattributable.",
        f"- Of the {totals['non_blank']} non-blank keys: {len(assigned)} assigned, {len(cand_pool)} sit in "
        "candidate pools (five 'No' values, two '1' values).",
        "- At least 7 keys are surplus to the 41 questions (possible section/notice elements, deleted or "
        "hidden questions). Their identity is unknowable from current evidence.",
        "",
        "## 4. Existing AI and processing mappings",
        "",
        "Innovation Type, Horizon, Categorization, Ownership, OriginalSubmission and the labelled-submission "
        "construction remain with the existing flow actions. **Pending `04-existing-flow/` export**; they are "
        "preserved, not rebuilt, and are out of scope for the raw-answer payload.",
        "",
        "## 5. Intentionally blank reviewer fields",
        "",
        "Human-review/governance fields (including ReviewStatus default 'Not reviewed' pending flow proof) are "
        "intentionally not populated by the create payload.",
        "",
        "## 6. Intentionally blank projected-impact fields",
        "",
        "Projected-impact measures (Word model, governance layer) are intentionally blank at item creation.",
        "",
        "## 7. Excluded SharePoint system fields (from the live schema)",
        "",
    ]
    for name in SPEC.get("system_fields_excluded", []):
        md.append(f"- `{name}`")
    md.append("")
    return "\n".join(md)


if __name__ == "__main__":
    (ROOT / "05-mapping-spec/mapping-spec.md").write_text(mapping_spec_md())
    (ROOT / "05-mapping-spec/unresolved-mappings.md").write_text(unresolved_md())
    (ROOT / "05-mapping-spec/coverage-report.md").write_text(coverage_md())
    print("reports written")
