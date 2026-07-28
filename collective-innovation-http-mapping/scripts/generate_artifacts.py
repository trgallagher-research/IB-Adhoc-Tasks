#!/usr/bin/env python3
"""Generate the Power Automate implementation artefacts from the mapping spec.

Modes:
  default      -> 06-generated-output/: compose-item-payload.json, a dummy-body
                  simulation (simulation-results.json) and validation-report.md.
                  Only mappings marked executable in the spec (both sides
                  Existing/Confirmed, all sources evidenced) are emitted —
                  Probable/Unresolved rows are structurally excluded.
  --fixtures   -> scripts/fixtures/output/: the same pipeline against the DUMMY
                  ZZFIXTURE_ schema, kept as a regression harness.

Compose expressions use the single-token form ("@if(...)", one leading @, no
braces) so a property keeps its native JSON type (null / number / string).
GRD_ACTION must match the live flow's Get response details action name —
verify it against the flow export (04-existing-flow/) before deployment.
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = "2026-07-28"

GRD_ACTION = "Get_response_details"   # VERIFY against the live flow's action name


def grd(key):
    return f"outputs('{GRD_ACTION}')?['body/{key}']"


def build_expression(kind, key=None):
    """Power Automate expression (without leading @) for one property."""
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
    if kind == "title_from_description":
        fallback = f"concat('Form submission ', outputs('{GRD_ACTION}')?['body/submitDate'])"
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
                 "M-SUBMITDATE": "submitdate"}


def q07_key(spec):
    return next(e["forms_response_key"] for e in spec["question_mappings"]
                if e["map_id"] == "Q07")


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
            "forms_key": None if kind != "title_from_description" else k7,
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
    return props


# ---------------- simulation (mirrors expression semantics) ----------------

def simulate(kind, body, key):
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
    if kind == "title_from_description":
        v = val(key)
        if v == "":
            return f"Form submission {body['submitDate']}"
        return v if len(v) <= 255 else v[:252] + "..."
    raise ValueError(kind)


def run_simulation(prop_meta, k7, type_of):
    """Run both dummy bodies through the semantic mirror; assert type contract."""
    body6 = json.loads((ROOT / "02-get-response-details/sanitized/"
                        "get-response-details-response-6.body.json").read_text())["body"]
    edge = {"responder": "edge.case@example.invalid",
            "submitDate": "12/31/2026 11:59:59 PM",
            k7: 'He said "let\'s try" — line1\nline2 \\ ünïcödé 🚀 <script>'}
    results = {}
    for name, body in (("response-6", body6), ("edge-case-all-blank-except-Q07", edge)):
        sim = {}
        for p in prop_meta:
            sim[p["internal_name"]] = simulate(p["kind"], body, p["forms_key"] or k7)
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
    prop_meta = production_properties(spec)
    payload = {p["internal_name"]: "@" + p["expression"] for p in prop_meta}
    artefact = {
        "_status": {
            "generated": GENERATED,
            "generated_by": "scripts/generate_artifacts.py",
            "executable_mappings": len(prop_meta),
            "notice": ("Only mappings with BOTH sides Existing/Confirmed and fully evidenced "
                       "expression sources are emitted. Still pending evidence (excluded here): "
                       "FormResponseID (trigger response-ID path unverified), OriginalSubmission "
                       "(flow expression), all Probable/Unresolved Forms keys. Before deployment, "
                       "verify the Get response details action name matches 'Get_response_details' "
                       "(underscores for spaces) or rename the references."),
        },
        "compose_input": payload,
    }
    (outdir / "compose-item-payload.json").write_text(
        json.dumps(artefact, indent=2, ensure_ascii=False) + "\n")

    type_of = {p["internal_name"]: p["sp_type"] for p in prop_meta}
    results = run_simulation(prop_meta, q07_key(spec), type_of)
    (outdir / "simulation-results.json").write_text(json.dumps({
        "_notice": "Semantic simulation of the production Compose payload against dummy bodies "
                   "(sanitized response 6; synthetic edge-case with JSON-sensitive characters and "
                   "all-blank answers). All values dummy.",
        "checks": ["valid JSON round-trip / escaping", "blank -> JSON null (never '', 0, false, 'N/A', 'null')",
                   "int for Number, ISO-shaped string for DateTime, non-empty string for Text/Note/Choice",
                   "Title never null or empty"],
        "results": results}, indent=2, ensure_ascii=False) + "\n")
    write_validation_report(prop_meta, spec)
    print(f"production mode: {len(prop_meta)} executable properties emitted; simulations passed")
    return prop_meta


def write_validation_report(prop_meta, spec):
    excluded = []
    for e in spec["forms_metadata_mappings"] + spec["question_mappings"]:
        if not e["executable"]:
            label = e.get("form_question_label") or e.get("description")
            excluded.append((e["map_id"], label, e["forms_key_confidence"],
                             e["sharepoint"]["confidence"],
                             "no destination" if e["sharepoint"].get("no_destination") else ""))
    md = [
        "# Validation report — executable payload properties",
        "",
        f"Generated {GENERATED} by `scripts/generate_artifacts.py`. Lists the source and "
        "normalization of every property in `compose-item-payload.json`, the exclusions, and "
        "the checks applied.",
        "",
        f"## Executable properties: {len(prop_meta)}",
        "",
        "| Property (internal name) | SP type | Source | Forms conf. | SP conf. | Normalization kind |",
        "|--------------------------|---------|--------|-------------|----------|--------------------|",
    ]
    for p in prop_meta:
        src = f"`{p['forms_key']}`" if p.get("forms_key") and p["kind"] != "title_from_description" \
            else p["label"]
        md.append(f"| `{p['internal_name']}` | {p['sp_type']} | {src} | "
                  f"{p['forms_confidence']} | {p['sp_confidence']} | {p['kind']} |")
    md += [
        "",
        "## Excluded from executable output (by rule)",
        "",
        "| ID | Mapping | Forms conf. | SP conf. | Note |",
        "|----|---------|-------------|----------|------|",
    ]
    for mid, label, fc, sc, note in excluded:
        md.append(f"| {mid} | {str(label)[:60]} | {fc} | {sc} | {note} |")
    md += [
        "",
        "## Dummy-body simulation (production payload)",
        "",
        "The payload semantics are mirrored in Python and run against the sanitized response-6 "
        "body and a synthetic edge-case body (quotes, apostrophes, backslash, line breaks, "
        "Unicode, emoji; every other answer blank). Asserted:",
        "",
        "- valid JSON round-trip — all JSON-sensitive characters survive;",
        "- blank answers become JSON `null` — never `''`, `0`, `false`, `'N/A'` or the string `'null'`;",
        "- Number columns receive integers; DateTime columns ISO-shaped strings; Text/Note/Choice "
        "columns non-empty strings;",
        "- `Title` is never null or empty (truncation at 255 with ellipsis; submitDate-based fallback).",
        "",
        "Results: `06-generated-output/simulation-results.json`.",
        "",
        "## Still requiring live verification in Power Automate",
        "",
        "- the actual `Get response details` action name referenced by `outputs('Get_response_details')`;",
        "- the trigger path `triggerOutputs()?['body/resourceData/responseId']` (blocks FormResponseID "
        "and the duplicate check — flow-export evidence EV-2);",
        "- date-only acceptance by `AnticipatedLaunchDate` (schema says Format=DateOnly; T1/T3 confirm);",
        "- end-to-end create via the copied flow (test matrix T0–T15).",
        "",
    ]
    (ROOT / "06-generated-output/validation-report.md").write_text("\n".join(md))


# ---------------- fixture mode (regression harness, unchanged behaviour) ----------------

FIXTURE_META = [
    ("M-TITLE", "Title", "Text", "title_from_description"),
    ("M-RESPONDER", "ZZFIXTURE_SubmitterEmail", "Text", "responder"),
    ("M-SUBMITDATE", "ZZFIXTURE_SubmittedOn", "DateTime", "submitdate"),
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
    results = run_simulation(prop_meta, k7, type_of)
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
