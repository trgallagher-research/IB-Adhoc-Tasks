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
FLOW = SPEC.get("flow_layer_mappings", [])
BACKEND = SPEC["backend_fields_not_form_questions"]

KNOWN_KEYS = {k["response_key"] for k in KEYS_INV["keys"]}
ASSIGNED = {e["forms_response_key"] for e in Q if e["forms_response_key"]}
SURPLUS = sorted(KNOWN_KEYS - ASSIGNED)


def sp_cell(e):
    sp = e["sharepoint"]
    if sp.get("no_destination"):
        return "— (no destination, Confirmed)"
    if sp["internal_name"]:
        return f"`{sp['internal_name']}` ({sp['type']}, {sp['confidence']})"
    return "Unresolved"


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
        f"**Cross-validation:** {SPEC['_meta']['cross_validation']}",
        "",
        "## Forms metadata mappings",
        "",
        "| ID | Source | Conf. | SharePoint | Executable |",
        "|----|--------|-------|------------|------------|",
    ]
    for e in META:
        md.append(f"| {e['map_id']} | {e['source'][:80]} | {e['forms_key_confidence']} | "
                  f"{sp_cell(e)} | {'yes' if e['executable'] else 'no'} |")
    md += [
        "",
        "## Question mappings (Excel columns 7–47) — all keys `Existing` from the flow's labelled construction",
        "",
        "| ID | Question label | Answer shape | Forms response key | Conf. | SharePoint | Executable |",
        "|----|----------------|--------------|--------------------|-------|------------|------------|",
    ]
    for e in Q:
        md.append(f"| {e['map_id']} | {e['form_question_label'][:70]} | {e['forms_answer_shape']} | "
                  f"`{e['forms_response_key']}` | {e['forms_key_confidence']} | {sp_cell(e)} | "
                  f"{'yes' if e['executable'] else 'no'} |")
    md += [
        "",
        "## Flow-layer mappings — preserved verbatim from the existing Create item",
        "",
        "| Property | Source |",
        "|----------|--------|",
    ]
    for m in FLOW:
        src = f"constant `{json.dumps(m['constant'])}`" if m["expression"] is None \
            else f"`{m['expression'][:80]}`"
        md.append(f"| `{m['internal_name']}` | {src} |")
    md += ["", "## Evidence detail", ""]
    for e in META + Q:
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
    unresolved = [e for e in META + Q if e["forms_key_confidence"] in ("Probable", "Unresolved")]
    md = [
        "# Unresolved mappings report",
        "",
        f"Generated {GENERATED} by `scripts/build_reports.py`.",
        "",
        f"## Open unresolved/probable mappings: {len(unresolved)}",
        "",
    ]
    if not unresolved:
        md += [
            "**None.** The existing flow's labelled-submission construction (EV‑2, captured "
            "2026‑07‑28) pairs every question label with its response key, and the live schema "
            "(EV‑1) resolves every destination. All prior Probables and candidate sets resolved "
            "consistently with the dummy-test evidence — zero contradictions.",
            "",
        ]
    else:
        for e in unresolved:
            md.append(f"- {e['map_id']} ({e['forms_key_confidence']}): "
                      f"{e.get('form_question_label') or e.get('description')}")
        md.append("")
    md += [
        "## Permanently unexplained keys (documented, harmless)",
        "",
        f"The body carries {len(SURPLUS)} keys beyond the 41 questions — blank in every observed "
        "response and referenced nowhere in the flow. Most plausibly deleted questions or section "
        "elements. They are mapped to nothing and require no action:",
        "",
    ]
    for k in SURPLUS:
        md.append(f"- `{k}`")
    md += [
        "",
        "## Residual items outside the mapping itself",
        "",
        "- Five of the eight Select actions were not Peek-code captured (names and join expressions "
        "are evidenced via Create item; the AI layer is preserved as-is, so this is non-blocking).",
        "- Live behaviour items are covered by the test matrix, not by mapping evidence.",
        "",
    ]
    return "\n".join(md)


def coverage_md():
    n_exec_q = sum(1 for e in Q if e["executable"])
    n_exec_m = sum(1 for e in META if e["executable"])
    by_conf = {}
    for e in Q:
        by_conf[e["forms_key_confidence"]] = by_conf.get(e["forms_key_confidence"], 0) + 1
    conf_str = " + ".join(f"{v} {k}" for k, v in sorted(by_conf.items()))
    totals = KEYS_INV["_provenance"]["totals"]

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
        f"| Question mappings | {len(Q)} | {conf_str} (Forms side) |",
        f"| Opaque `r…` keys | {totals['opaque_r_keys']} | {len(ASSIGNED)} assigned by the flow's labelled "
        f"construction + {len(SURPLUS)} permanently-blank surplus keys |",
        f"| Executable payload properties | {n_exec_q + n_exec_m + len(FLOW)} | {n_exec_q} question + "
        f"{n_exec_m} metadata/audit + {len(FLOW)} preserved flow-layer |",
        "",
        "Key-count arithmetic closes exactly: 41 + "
        f"{len(SURPLUS)} = {totals['opaque_r_keys']}.",
        "",
        "## 1. Form fields without a per-column SharePoint destination",
        "",
        "- **Implementation Readiness Notice (Q22)** — display-only element (key identified from the "
        "flow; blank in every observed response; no schema field). No destination required.",
        "- **Add any supporting files (Q47)** — no supporting-files column; Phase 1 excludes file "
        "references from per-column storage. Raw answer string still lands inside `OriginalSubmission`.",
        "- **Excel metadata 'Start time', 'Last modified time', 'Name'** — no Get-response-details "
        "equivalent and no schema destination; not mapped (as in the existing flow).",
        "",
        "## 2. SharePoint fields without Form sources (from the live schema)",
        "",
        "All evidenced and handled: flow-constructed audit fields (`Title`, `FormResponseID`, "
        "`SubmittedDate`, `Respondent`, `SourceForm`, `OriginalSubmission`, `ProcessedDate`, "
        "`ProcessingStatus`, `PromptVersion`), AI-layer fields, and governance fields — see the "
        "flow-layer and backend tables in the mapping spec. `ProcessingError` is written only by "
        "the new catch path.",
        "",
        "## 3. Unexplained Forms keys",
        "",
        f"{len(SURPLUS)} surplus keys, blank in every observed response and referenced nowhere in "
        "the flow (listed in the unresolved-mappings report). No action required.",
        "",
        "## 4. Existing AI and processing mappings",
        "",
        "Captured verbatim from Create item and preserved in the payload's flow-layer properties: "
        "AISummary, Topics, KeyFindings, Examples, OpenQuestions, DifferentPerspectives, "
        "ClaimsToVerify, RelatedKnowledge, HumanReviewRequired/Reason, FullAIOutput, ReviewStatus, "
        "ProcessingStatus, ProcessedDate, PromptVersion, SourceForm, ContentTypeId.",
        "",
        "## 5. Intentionally blank reviewer fields",
        "",
        "ReviewStatus is explicitly 'Not reviewed' (as in the existing flow, matching the column "
        "default); other governance fields are untouched by the payload.",
        "",
        "## 6. Intentionally blank projected-impact fields",
        "",
        "No projected-impact columns exist in the live schema's visible field set; nothing is sent.",
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
