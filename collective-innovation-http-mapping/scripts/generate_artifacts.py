#!/usr/bin/env python3
"""Generate the Power Automate implementation artefacts from the mapping spec.

Modes:
  default      -> 06-generated-output/: compose-item-payload.json (full payload:
                  raw questions + metadata + preserved flow-layer properties),
                  compose-labelled-submission.txt (the OriginalSubmission /
                  AI-prompt text, extracted verbatim from the flow evidence),
                  simulation-results.json, validation-report.md.
  --fixtures   -> scripts/fixtures/output/: regression harness on the DUMMY
                  ZZFIXTURE_ schema.

Compose expressions use the single-token form ("@if(...)") so properties keep
native JSON types. Action names referenced: Get_response_details (VERIFIED),
Run_a_prompt / Select_* (from flow captures), Compose_labelled_submission (new
action introduced by the implementation instructions).
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = "2026-07-28"

GRD_ACTION = "Get_response_details"   # verified against flow captures
RESPONSE_ID_EXPR = "triggerOutputs()?['body/resourceData/responseId']"  # verified


def grd(key):
    return f"outputs('{GRD_ACTION}')?['body/{key}']"


def build_expression(kind, key=None):
    v = grd(key) if key else None
    if kind in ("text", "multiline", "date", "yesno_choice"):
        return f"if(empty({v}), null, {v})"
    if kind == "rating":
        return f"if(empty({v}), null, int({v}))"
    if kind == "multichoice_as_text":
        return f"if(empty({v}), null, join(json({v}), '; '))"
    if kind == "responder":
        return f"outputs('{GRD_ACTION}')?['body/responder']"
    if kind == "submitdate":
        return (f"concat(formatDateTime(outputs('{GRD_ACTION}')?['body/submitDate'], "
                "'yyyy-MM-ddTHH:mm:ss'), 'Z')")
    if kind == "responseid_string":
        return f"string({RESPONSE_ID_EXPR})"
    if kind == "original_submission":
        return "outputs('Compose_labelled_submission')"
    if kind == "title_from_description":
        fallback = f"concat('Form response ', string({RESPONSE_ID_EXPR}))"
        return (f"if(empty({v}), {fallback}, "
                f"if(greater(length({v}), 255), concat(substring({v}, 0, 252), '...'), {v}))")
    raise ValueError(kind)


SHAPE_TO_KIND = {
    "free text": "multiline",
    "date": "date",
    "rating 1-5": "rating",
    "Yes/No": "yesno_choice",
    "multi-choice": "multichoice_as_text",
}
METADATA_KIND = {"M-TITLE": "title_from_description", "M-RESPONDER": "responder",
                 "M-SUBMITDATE": "submitdate", "M-RESPONSEID": "responseid_string",
                 "M-ORIGINALSUBMISSION": "original_submission"}


def q07_key(spec):
    return next(e["forms_response_key"] for e in spec["question_mappings"]
                if e["map_id"] == "Q07")


def extract_labelled_template():
    """Pull the labelled-submission text verbatim from the flow evidence."""
    action = json.loads((ROOT / "04-existing-flow/sanitized/run-a-prompt.json").read_text())
    return action["definition"]["inputs"]["parameters"]["item/requestv2/SubmissionText"]


def production_properties(spec):
    props = []
    k7 = q07_key(spec)
    for e in spec["forms_metadata_mappings"]:
        if not e["executable"]:
            continue
        kind = METADATA_KIND[e["map_id"]]
        props.append({
            "internal_name": e["sharepoint"]["internal_name"],
            "sp_type": e["sharepoint"]["type"],
            "expression": build_expression(kind, k7 if kind == "title_from_description" else None),
            "kind": kind, "map_id": e["map_id"], "label": e["description"],
            "forms_key": k7 if kind == "title_from_description" else None,
            "forms_confidence": e["forms_key_confidence"],
            "sp_confidence": e["sharepoint"]["confidence"],
        })
    for e in spec["question_mappings"]:
        if not e["executable"]:
            continue
        kind = SHAPE_TO_KIND[e["forms_answer_shape"]]
        props.append({
            "internal_name": e["sharepoint"]["internal_name"],
            "sp_type": e["sharepoint"]["type"],
            "expression": build_expression(kind, e["forms_response_key"]),
            "kind": kind, "map_id": e["map_id"], "label": e["form_question_label"],
            "forms_key": e["forms_response_key"],
            "forms_confidence": e["forms_key_confidence"],
            "sp_confidence": e["sharepoint"]["confidence"],
        })
    for m in spec.get("flow_layer_mappings", []):
        props.append({
            "internal_name": m["internal_name"],
            "sp_type": "(flow layer)",
            "expression": m["expression"],           # None => constant
            "constant": m.get("constant"),
            "kind": "verbatim", "map_id": f"F-{m['internal_name']}",
            "label": "preserved Create item parameter",
            "forms_key": None,
            "forms_confidence": m["confidence"], "sp_confidence": "Confirmed",
        })
    return props


def payload_value(p):
    if p["kind"] == "verbatim":
        return p["constant"] if p["expression"] is None else "@" + p["expression"]
    return "@" + p["expression"]


# ---------------- simulation (mirrors expression semantics) ----------------

def render_template(template, body, rid):
    """Render the labelled-submission template against a dummy body."""
    def sub(m):
        return body.get(m.group(1), "")
    text = re.sub(r"@\{outputs\('Get_response_details'\)\?\['body/([A-Za-z0-9]+)'\]\}", sub, template)
    return text.replace("@{triggerOutputs()?['body/resourceData/responseId']}", str(rid))


def simulate(kind, body, key, rid, template):
    def val(k):
        return body.get(k, "")
    if kind in ("multiline", "text", "date", "yesno_choice"):
        v = val(key)
        return None if v == "" else v
    if kind == "rating":
        v = val(key)
        return None if v == "" else int(v)
    if kind == "multichoice_as_text":
        v = val(key)
        return None if v == "" else "; ".join(json.loads(v))
    if kind == "responder":
        return body["responder"]
    if kind == "submitdate":
        dt = datetime.strptime(body["submitDate"], "%m/%d/%Y %I:%M:%S %p")
        return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    if kind == "responseid_string":
        return str(rid)
    if kind == "original_submission":
        return render_template(template, body, rid)
    if kind == "title_from_description":
        v = val(key)
        if v == "":
            return f"Form response {rid}"
        return v if len(v) <= 255 else v[:252] + "..."
    raise ValueError(kind)


def run_simulation(prop_meta, k7, type_of, template):
    body6 = json.loads((ROOT / "02-get-response-details/sanitized/"
                        "get-response-details-response-6.body.json").read_text())["body"]
    edge = {"responder": "edge.case@example.invalid",
            "submitDate": "12/31/2026 11:59:59 PM",
            k7: 'He said "let\'s try" — line1\nline2 \\ ünïcödé 🚀 <script>'}
    results = {}
    for name, body, rid in (("response-6", body6, 6),
                            ("edge-case-all-blank-except-Q07", edge, 999)):
        sim = {}
        for p in prop_meta:
            if p["kind"] == "verbatim":
                continue  # AI/flow-layer values are proven by the working flow, not simulable
            sim[p["internal_name"]] = simulate(p["kind"], body, p["forms_key"] or k7, rid, template)
        text = json.dumps(sim, ensure_ascii=False)
        assert json.loads(text) == sim
        for iname, v in sim.items():
            t = type_of[iname]
            if v is None:
                continue
            if t.startswith("Number"):
                assert isinstance(v, int), (iname, v)
            elif t.startswith(("Text", "Note", "Choice")):
                assert isinstance(v, str) and v != "", (iname, v)
            elif t.startswith("DateTime"):
                assert isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v), (iname, v)
            assert v != "", f"empty string sent to {iname}"
        assert sim.get("Title") not in (None, ""), "Title must never be null/empty"
        results[name] = sim
    return results


def run_production(spec):
    outdir = ROOT / "06-generated-output"
    template = extract_labelled_template()
    (outdir / "compose-labelled-submission.txt").write_text(template + "\n")

    prop_meta = production_properties(spec)
    payload = {p["internal_name"]: payload_value(p) for p in prop_meta}
    n_raw = sum(1 for p in prop_meta if p["map_id"].startswith("Q"))
    n_meta = sum(1 for p in prop_meta if p["map_id"].startswith("M-"))
    n_flow = sum(1 for p in prop_meta if p["map_id"].startswith("F-"))
    artefact = {
        "_status": {
            "generated": GENERATED,
            "generated_by": "scripts/generate_artifacts.py",
            "executable_mappings": len(prop_meta),
            "composition": f"{n_raw} raw question properties + {n_meta} metadata/audit + "
                           f"{n_flow} preserved flow-layer properties",
            "notice": ("This payload fully REPLACES the existing Create item: it carries every "
                       "property that action set (preserved verbatim, incl. constants and the "
                       "ContentTypeId) plus the new raw per-question columns and OriginalSubmission. "
                       "It requires the Compose_labelled_submission action defined in the "
                       "implementation instructions (text in compose-labelled-submission.txt)."),
        },
        "compose_input": payload,
    }
    (outdir / "compose-item-payload.json").write_text(
        json.dumps(artefact, indent=2, ensure_ascii=False) + "\n")

    write_paste_actions(payload, template)
    write_text_template(prop_meta)
    write_smoke_template(prop_meta)

    type_of = {p["internal_name"]: p["sp_type"] for p in prop_meta}
    results = run_simulation(prop_meta, q07_key(spec), type_of, template)
    # cross-check: assembling the simulated values as JSON text (what the text
    # template produces) must parse back to the identical object
    for sim in results.values():
        text = "{\n" + ",\n".join(f"\"{k}\": {json.dumps(v, ensure_ascii=False)}"
                                  for k, v in sim.items()) + "\n}"
        assert json.loads(text) == sim
    (outdir / "simulation-results.json").write_text(json.dumps({
        "_notice": "Semantic simulation of the non-flow-layer payload properties against dummy bodies "
                   "(sanitized response 6; synthetic edge-case). Flow-layer (AI/constants) properties "
                   "are preserved verbatim from the working flow and are exercised by the live test "
                   "matrix instead. All values dummy.",
        "results": results}, indent=2, ensure_ascii=False) + "\n")
    write_validation_report(prop_meta, spec)
    print(f"production mode: {len(prop_meta)} properties ({n_raw} raw + {n_meta} metadata + "
          f"{n_flow} flow-layer); simulations passed")
    return prop_meta


def STR(expr):
    """Expression emitting a QUOTED, JSON-escaped string literal for expr.

    Explicit character escaping — deterministic and independent of how the
    platform formats string()/json() output. Order is load-bearing: backslash
    first (so escapes added later are not re-escaped), then the double quote,
    then CR/LF/TAB via decodeUriComponent so no literal control characters
    appear inside the expression text.

    Power Automate string literals use single quotes and treat backslash as an
    ordinary character, so '\\' below is one literal backslash and '\\\\' is two.
    """
    e = expr
    e = f"replace({e}, '\\', '\\\\')"                                  # \  -> \\
    e = f"replace({e}, '\"', '\\\"')"                                  # "  -> \"
    e = f"replace({e}, decodeUriComponent('%0D'), '\\r')"              # CR -> \r
    e = f"replace({e}, decodeUriComponent('%0A'), '\\n')"              # LF -> \n
    e = f"replace({e}, decodeUriComponent('%09'), '\\t')"              # TAB-> \t
    return f"concat('\"', {e}, '\"')"


def template_fragment(p):
    """Value fragment (text with @{...} interpolations) for one property in the
    input-box-safe JSON text template. Must be semantically identical to the
    object payload's bare-@ expression for the same property."""
    kind, key = p["kind"], p.get("forms_key")
    v = grd(key) if key else None
    if kind in ("text", "multiline", "date", "yesno_choice"):
        return f"@{{if(empty({v}), 'null', {STR(v)})}}"
    if kind == "rating":
        return f"@{{if(empty({v}), 'null', int({v}))}}"
    if kind == "multichoice_as_text":
        j = f"join(json({v}), '; ')"
        return f"@{{if(empty({v}), 'null', {STR(j)})}}"
    if kind == "responder":
        responder = "outputs('" + GRD_ACTION + "')?['body/responder']"
        return "@{" + STR(responder) + "}"
    if kind == "submitdate":
        return ('"@{concat(formatDateTime(outputs(\'' + GRD_ACTION +
                "')?['body/submitDate'], 'yyyy-MM-ddTHH:mm:ss'), 'Z')}\"")
    if kind == "responseid_string":
        return f'"@{{{RESPONSE_ID_EXPR}}}"'
    if kind == "original_submission":
        return "@{" + STR("outputs('Compose_labelled_submission')") + "}"
    if kind == "title_from_description":
        fallback = f"concat('Form response ', string({RESPONSE_ID_EXPR}))"
        title = (f"if(empty({v}), {fallback}, "
                 f"if(greater(length({v}), 255), concat(substring({v}, 0, 252), '...'), {v}))")
        return f"@{{{STR(title)}}}"
    if kind == "verbatim":
        if p["expression"] is None:
            return json.dumps(p["constant"])
        e = p["expression"]
        if p["internal_name"] == "HumanReviewRequired":   # boolean -> raw true/false, null-safe
            return f"@{{coalesce({e}, 'null')}}"
        if p["internal_name"] == "ProcessedDate":         # fixed ISO format, no escapables
            return f'"@{{{e}}}"'
        return f"@{{if(empty({e}), 'null', {STR(e)})}}"   # AI text / joins, null-safe
    raise ValueError(kind)


def write_smoke_template(prop_meta):
    """Three-property cut of the text template: one escaped string, one Number
    (null-capable) and one plain interpolation. Lets the mechanism be proven in
    the designer in two minutes before the full 61-property paste."""
    wanted = ["Title", "OpportunityDescription", "ReputationalImpactScore"]
    chosen = [p for name in wanted for p in prop_meta if p["internal_name"] == name]
    lines = ["{"]
    for i, p in enumerate(chosen):
        comma = "," if i < len(chosen) - 1 else ""
        lines.append(f'"{p["internal_name"]}": {template_fragment(p)}{comma}')
    lines.append("}")
    (ROOT / "06-generated-output/compose-item-payload.SMOKETEST.txt").write_text(
        "\n".join(lines) + "\n")


def write_text_template(prop_meta):
    """Input-box-safe variant of the payload: a JSON *text* template whose
    Compose output is a JSON string (HTTP body accepts it directly). Exists
    because the clipboard-paste of the object-form action is tenant-dependent;
    this file is pasted into the ordinary Compose Inputs field."""
    lines = ["{"]
    for i, p in enumerate(prop_meta):
        comma = "," if i < len(prop_meta) - 1 else ""
        lines.append(f'"{p["internal_name"]}": {template_fragment(p)}{comma}')
    lines.append("}")
    (ROOT / "06-generated-output/compose-item-payload.template.txt").write_text(
        "\n".join(lines) + "\n")


def write_paste_actions(payload, template):
    """Emit clipboard-format action JSON for the two Compose actions.

    Format is the Power Automate clipboard envelope (classic designer 'My
    clipboard' tab accepts Ctrl+V of this JSON; the new designer's 'Paste an
    action' accepts it in most versions). This bypasses the designer input
    fields entirely, so the single-@ expression values and the @{} template
    interpolations land in the definition byte-exact — no escaping risk.
    """
    outdir = ROOT / "06-generated-output/paste-actions"
    outdir.mkdir(parents=True, exist_ok=True)

    def envelope(name, inputs, uid):
        return {
            "id": f"e5b0f5f0-0000-4b6e-9df6-{uid:012d}",
            "brandColor": "#8C3900",
            "connectionReferences": {},
            "connectorDisplayName": "Data Operation",
            "icon": "https://psux.azureedge.net/Content/Images/DesignerOperations/compose.png",
            "isTrigger": False,
            "operationName": name,
            "operationDefinition": {"type": "Compose", "inputs": inputs, "runAfter": {}},
        }

    (outdir / "compose-labelled-submission.action.json").write_text(
        json.dumps(envelope("Compose labelled submission", template, 1),
                   indent=2, ensure_ascii=False) + "\n")
    (outdir / "compose-item-payload.action.json").write_text(
        json.dumps(envelope("Compose item payload", payload, 2),
                   indent=2, ensure_ascii=False) + "\n")
    (outdir / "README.md").write_text(
        "# Paste-ready Compose actions\n\n"
        "Each file is a Power Automate clipboard-format action. To use: open the file, "
        "select ALL its JSON, copy, then in the flow editor add a step via **My clipboard** "
        "(classic designer: + New step -> My clipboard tab -> Ctrl+V; new designer: copy any "
        "action first so 'Paste an action' appears on the + menu, then Ctrl+V-paste this JSON). "
        "After pasting, verify with Peek code: `inputs` must be an OBJECT for the payload "
        "compose (values starting with a single `@`) and a text template for the labelled "
        "submission (interpolations as `@{...}`). If Peek code shows `@@`, the designer "
        "escaped the paste — delete the action and use the clipboard route, not the input "
        "field.\n\nRegenerated by `scripts/generate_artifacts.py`; do not hand-edit.\n")


def write_validation_report(prop_meta, spec):
    excluded = []
    for e in spec["forms_metadata_mappings"] + spec["question_mappings"]:
        if not e["executable"]:
            label = e.get("form_question_label") or e.get("description")
            excluded.append((e["map_id"], label, e["forms_key_confidence"],
                             e["sharepoint"]["confidence"],
                             "no destination (by determination)" if e["sharepoint"].get("no_destination") else ""))
    md = [
        "# Validation report — executable payload properties",
        "",
        f"Generated {GENERATED} by `scripts/generate_artifacts.py`. Lists the source and "
        "normalization of every property in `compose-item-payload.json`, the exclusions, and "
        "the checks applied.",
        "",
        f"## Executable properties: {len(prop_meta)}",
        "",
        "| Property (internal name) | SP type | Source | Confidence | Kind |",
        "|--------------------------|---------|--------|------------|------|",
    ]
    for p in prop_meta:
        if p["kind"] == "verbatim":
            src = f"constant `{json.dumps(p['constant'])}`" if p["expression"] is None \
                else f"`{p['expression'][:70]}`"
        elif p.get("forms_key"):
            src = f"`{p['forms_key']}`"
        else:
            src = p["label"]
        md.append(f"| `{p['internal_name']}` | {p['sp_type']} | {src} | "
                  f"{p['forms_confidence']} | {p['kind']} |")
    md += ["", "## Excluded from per-column payload", "",
           "| ID | Mapping | Forms conf. | SP conf. | Note |",
           "|----|---------|-------------|----------|------|"]
    for mid, label, fc, sc, note in excluded:
        md.append(f"| {mid} | {str(label)[:60]} | {fc} | {sc} | {note} |")
    md += [
        "",
        "Both excluded questions' raw answers still reach SharePoint inside `OriginalSubmission` "
        "(preserved labelled text), as in the existing flow's AI prompt.",
        "",
        "## Dummy-body simulation",
        "",
        "Raw/metadata properties (including the rendered `OriginalSubmission` template) are "
        "simulated against the sanitized response-6 body and a synthetic edge-case body "
        "(quotes, apostrophes, backslash, line breaks, Unicode, emoji; every other answer "
        "blank). Asserted: JSON round-trip escaping; blank -> `null` (never `''`, `0`, `false`, "
        "`'N/A'`, `'null'`); int for Number; ISO shape for DateTime; non-empty strings for "
        "Text/Note/Choice; `Title` never null (truncation at 255; response-ID fallback). "
        "Flow-layer (AI/constant) properties are preserved verbatim from the working flow and "
        "are exercised by the live test matrix instead. Results: `simulation-results.json`.",
        "",
        "## Deliberate deviations from the existing Create item (documented)",
        "",
        "- `Title`: truncated at 255 with ellipsis + blank fallback (existing raw mapping fails "
        "for >255-char descriptions).",
        "- `SubmittedDate`: ISO 8601 UTC instead of the raw US-format string (same instant; REST "
        "is stricter than the connector).",
        "- `OriginalSubmission`: newly populated with the preserved labelled text (existing flow "
        "left it empty).",
        "- Everything else flow-layer: verbatim, including the `PromptVersion` trailing newline.",
        "",
        "## Still requiring manual testing in Power Automate",
        "",
        "- End-to-end create via the copied flow: test matrix T0–T15 (incl. DLP probe T0, "
        "duplicate check T7/T13, choice/boolean/date acceptance).",
        "- AI-layer values arriving through the HTTP payload identically to the connector path "
        "(compare one item created by each).",
        "",
    ]
    (ROOT / "06-generated-output/validation-report.md").write_text("\n".join(md))


# ---------------- fixture mode (regression harness) ----------------

FIXTURE_META = [
    ("M-TITLE", "Title", "Text", "title_from_description"),
    ("M-RESPONDER", "ZZFIXTURE_SubmitterEmail", "Text", "responder"),
    ("M-SUBMITDATE", "ZZFIXTURE_SubmittedOn", "DateTime", "submitdate"),
    ("M-RESPONSEID", "ZZFIXTURE_FormResponseId", "Text", "responseid_string"),
]
FIXTURE_OVERLAY = {
    "Q07": ("ZZFIXTURE_OpportunityDescription", "Note"),
    "Q09": ("ZZFIXTURE_AnticipatedLaunchDate", "DateTime"),
    "Q10": ("ZZFIXTURE_ImplementationTimeline", "Note"),
    "Q15": ("ZZFIXTURE_StrategicGoals", "Note"),
    "Q16": ("ZZFIXTURE_StrategicAlignment", "Note"),
    "Q36": ("ZZFIXTURE_OperationalImpactComments", "Note"),
    "Q38": ("ZZFIXTURE_ReputationalImpactComments", "Note"),
    "Q39": ("ZZFIXTURE_InternalStakeholders", "Note"),
    "Q40": ("ZZFIXTURE_ConsultationOutcomes", "Note"),
}


def run_fixtures(spec):
    outdir = ROOT / "scripts/fixtures/output"
    outdir.mkdir(parents=True, exist_ok=True)
    template = extract_labelled_template()
    k7 = q07_key(spec)
    prop_meta = []
    for map_id, name, sp_type, kind in FIXTURE_META:
        prop_meta.append({"internal_name": name, "sp_type": sp_type, "kind": kind,
                          "forms_key": k7 if kind == "title_from_description" else None,
                          "expression": build_expression(kind, k7 if kind == "title_from_description" else None)})
    for e in spec["question_mappings"]:
        if e["map_id"] in FIXTURE_OVERLAY and e["forms_response_key"]:
            name, sp_type = FIXTURE_OVERLAY[e["map_id"]]
            kind = SHAPE_TO_KIND[e["forms_answer_shape"]]
            prop_meta.append({"internal_name": name, "sp_type": sp_type, "kind": kind,
                              "forms_key": e["forms_response_key"],
                              "expression": build_expression(kind, e["forms_response_key"])})
    payload = {p["internal_name"]: "@" + p["expression"] for p in prop_meta}
    (outdir / "compose-item-payload.FIXTURE.json").write_text(json.dumps({
        "_notice": "FIXTURE OUTPUT — NOT FOR DEPLOYMENT. Internal names are ZZFIXTURE_ dummies.",
        "generated": GENERATED, "compose_input": payload}, indent=2, ensure_ascii=False) + "\n")
    type_of = {p["internal_name"]: p["sp_type"] for p in prop_meta}
    results = run_simulation(prop_meta, k7, type_of, template)
    (outdir / "simulation-results.FIXTURE.json").write_text(json.dumps({
        "_notice": "FIXTURE simulation against dummy bodies.",
        "results": results}, indent=2, ensure_ascii=False) + "\n")
    print(f"fixture mode: {len(prop_meta)} properties; simulations passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", action="store_true")
    args = ap.parse_args()
    spec = json.loads((ROOT / "05-mapping-spec/mapping-spec.json").read_text())
    if args.fixtures:
        run_fixtures(spec)
    else:
        run_production(spec)
