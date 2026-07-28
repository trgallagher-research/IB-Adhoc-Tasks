#!/usr/bin/env python3
"""Generate the Power Automate implementation artefacts from the mapping spec.

Modes:
  default      -> 06-generated-output/compose-item-payload.json (+ validation report
                  section data). Only mappings whose Forms side AND SharePoint side
                  are Existing/Confirmed are emitted. Probable/Unresolved rows are
                  structurally excluded — this script is the enforcement point.
  --fixtures   -> scripts/fixtures/output/ : runs the identical pipeline against the
                  DUMMY fixture schema (all internal names ZZFIXTURE_-prefixed) to
                  prove the generator + normalization + escaping behaviour end to
                  end, and simulates the payload against two dummy bodies.

The Compose expressions use the single-token form ("@if(...)", one leading @, no
braces) so a property keeps its native JSON type (null / number / string) instead
of being stringified. GRD_ACTION below must match the live flow's action name.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = "2026-07-28"

GRD_ACTION = "Get_response_details"   # verify against the live flow's action name
RESPONSE_ID_EXPR = "triggerOutputs()?['body/resourceData/responseId']"  # verify in live flow

OK_STATES = {"Existing", "Confirmed"}


def grd(key):
    return f"outputs('{GRD_ACTION}')?['body/{key}']"


def build_expression(kind, key=None):
    """Return the Power Automate expression (without leading @) for one property."""
    v = grd(key) if key else None
    if kind in ("text", "multiline", "date"):
        return f"if(empty({v}), null, {v})"
    if kind == "rating":
        return f"if(empty({v}), null, int({v}))"
    if kind == "multichoice_as_text":
        return f"if(empty({v}), null, join(json({v}), '; '))"
    if kind == "yesno_choice":
        return f"if(empty({v}), null, {v})"
    if kind == "responder":
        return f"outputs('{GRD_ACTION}')?['body/responder']"
    if kind == "submitdate":
        return (f"concat(formatDateTime(outputs('{GRD_ACTION}')?['body/submitDate'], "
                "'yyyy-MM-ddTHH:mm:ss'), 'Z')")
    if kind == "responseid":
        return f"int({RESPONSE_ID_EXPR})"
    if kind == "title_from_description":
        return (f"if(empty({v}), concat('Form response ', {RESPONSE_ID_EXPR}), "
                f"if(greater(length({v}), 255), concat(substring({v}, 0, 252), '...'), {v}))")
    raise ValueError(kind)


SHAPE_TO_KIND = {
    "free text": "multiline",
    "date": "date",
    "rating 1-5": "rating",
    "Yes/No": "yesno_choice",
    "multi-choice": "multichoice_as_text",
}


def executable_properties(spec, fixture_overlay=None):
    """Yield (internal_name, expression, meta) for every executable mapping.

    fixture_overlay: {map_id: (internal_name, sp_type)} marks the SharePoint side
    Confirmed-in-fixture-world; production mode uses only the spec itself.
    """
    props = []
    for e in spec["question_mappings"]:
        sp = dict(e["sharepoint"])
        if fixture_overlay and e["map_id"] in fixture_overlay:
            sp["internal_name"], sp["type"] = fixture_overlay[e["map_id"]]
            sp["confidence"] = "Confirmed (FIXTURE)"
        forms_ok = e["forms_key_confidence"] in OK_STATES
        sp_ok = sp["confidence"].startswith(tuple(OK_STATES)) and sp["internal_name"]
        if not (forms_ok and sp_ok):
            continue
        kind = SHAPE_TO_KIND[e["forms_answer_shape"]]
        props.append({
            "internal_name": sp["internal_name"],
            "sp_type": sp["type"],
            "expression": build_expression(kind, e["forms_response_key"]),
            "kind": kind,
            "map_id": e["map_id"],
            "label": e["form_question_label"],
            "forms_key": e["forms_response_key"],
            "forms_confidence": e["forms_key_confidence"],
            "sp_confidence": sp["confidence"],
        })
    return props


FIXTURE_META = [
    # (map_id-ish, internal name, type, kind, source)
    ("M-TITLE", "Title", "Text", "title_from_description", "Q07 key + response ID"),
    ("M-RESPONDER", "ZZFIXTURE_SubmitterEmail", "Text", "responder", "body responder"),
    ("M-SUBMITDATE", "ZZFIXTURE_SubmittedOn", "DateTime", "submitdate", "body submitDate"),
    ("M-RESPONSEID", "ZZFIXTURE_FormResponseId", "Number", "responseid", "trigger responseId"),
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


def build_payload(spec, fixture=False):
    q07_key = next(e["forms_response_key"] for e in spec["question_mappings"]
                   if e["map_id"] == "Q07")
    props = executable_properties(spec, FIXTURE_OVERLAY if fixture else None)
    payload = {}
    prop_meta = []
    if fixture:
        for map_id, name, sp_type, kind, source in FIXTURE_META:
            expr = build_expression(kind, q07_key if kind == "title_from_description" else None)
            payload[name] = "@" + expr
            prop_meta.append({"internal_name": name, "sp_type": sp_type, "kind": kind,
                              "map_id": map_id, "label": source, "forms_key": None,
                              "forms_confidence": "Confirmed",
                              "sp_confidence": "Confirmed (FIXTURE)", "expression": expr})
    for p in props:
        payload[p["internal_name"]] = "@" + p["expression"]
        prop_meta.append(p)
    return payload, prop_meta


# ---------------- fixture simulation (mirrors expression semantics) ----------------

def simulate(kind, body, key, response_id):
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
    if kind == "responseid":
        return int(response_id)
    if kind == "title_from_description":
        v = val(key)
        if v == "":
            return f"Form response {response_id}"
        return v if len(v) <= 255 else v[:252] + "..."
    raise ValueError(kind)


EDGE_CASE_BODY = {
    "responder": "edge.case@example.invalid",
    "submitDate": "12/31/2026 11:59:59 PM",
    # JSON-sensitive content: quotes, apostrophes, backslash, newline, unicode
    "__edgecase_note": "synthetic body exercising JSON-sensitive characters",
}


def run_fixtures(spec):
    outdir = ROOT / "scripts/fixtures/output"
    outdir.mkdir(parents=True, exist_ok=True)
    schema = json.loads((ROOT / "scripts/fixtures/fixture-sharepoint-schema.json").read_text())
    fields = {f["InternalName"]: f for f in schema["fields"]}

    payload, prop_meta = build_payload(spec, fixture=True)
    for p in prop_meta:  # every fixture property must exist in the fixture schema
        assert p["internal_name"] in fields, p["internal_name"]

    artefact = {
        "_notice": ("FIXTURE OUTPUT — NOT FOR DEPLOYMENT. Internal names are ZZFIXTURE_ "
                    "dummies. Demonstrates the generator against the dummy schema."),
        "generated": GENERATED,
        "compose_input": payload,
    }
    (outdir / "compose-item-payload.FIXTURE.json").write_text(
        json.dumps(artefact, indent=2, ensure_ascii=False) + "\n")

    # Simulation bodies: sanitized response 6 + synthetic edge cases
    body6 = json.loads((ROOT / "02-get-response-details/sanitized/"
                        "get-response-details-response-6.body.json").read_text())["body"]
    q07_key = next(e["forms_response_key"] for e in spec["question_mappings"]
                   if e["map_id"] == "Q07")
    edge = dict(EDGE_CASE_BODY)
    edge[q07_key] = 'He said "let\'s try" — line1\nline2 \\ ünïcödé 🚀 <script>'
    # all other keys blank in the edge body -> exercises null handling everywhere

    results = {}
    for name, body, rid in (("response-6", body6, 6), ("edge-case", edge, 999)):
        sim = {}
        for p in prop_meta:
            key = p["forms_key"] or q07_key
            sim[p["internal_name"]] = simulate(p["kind"], body, key, rid)
        # round-trip through JSON to prove serializability / escaping
        text = json.dumps(sim, ensure_ascii=False)
        back = json.loads(text)
        assert back == sim
        # type assertions against fixture schema
        for iname, v in sim.items():
            t = fields[iname]["TypeAsString"]
            if v is None:
                assert not fields[iname]["Required"], f"null into required {iname}"
                continue
            if t == "Number":
                assert isinstance(v, int), (iname, v)
            elif t in ("Text", "Note", "Choice"):
                assert isinstance(v, str) and v != "", (iname, v)
            elif t == "DateTime":
                assert isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v), (iname, v)
            assert v != "", f"empty string sent to {iname}"
        results[name] = sim

    (outdir / "simulation-results.FIXTURE.json").write_text(json.dumps({
        "_notice": "FIXTURE simulation of the Compose payload semantics against dummy bodies.",
        "checks": ["valid JSON round-trip", "no empty strings emitted",
                   "null (not '' / 0 / 'null') for blank Number, DateTime and text",
                   "int type for Number fields", "JSON-sensitive characters survive round-trip",
                   "required Title never null"],
        "results": results}, indent=2, ensure_ascii=False) + "\n")
    print(f"fixture mode: {len(prop_meta)} properties; simulations passed for "
          f"{', '.join(results)}")
    return prop_meta


def run_production(spec):
    outdir = ROOT / "06-generated-output"
    payload, prop_meta = build_payload(spec, fixture=False)
    artefact = {
        "_status": {
            "generated": GENERATED,
            "generated_by": "scripts/generate_artifacts.py",
            "executable_mappings": len(prop_meta),
            "notice": ("Only mappings with BOTH sides Existing/Confirmed are emitted. "
                       "SharePoint schema evidence is currently ABSENT (03-sharepoint-schema/), "
                       "so this payload is intentionally EMPTY. Populate the schema evidence, "
                       "update the spec, and regenerate. Do not hand-add properties here."),
        },
        "compose_input": payload,
    }
    (outdir / "compose-item-payload.json").write_text(
        json.dumps(artefact, indent=2, ensure_ascii=False) + "\n")
    write_validation_report(prop_meta)
    print(f"production mode: {len(prop_meta)} executable properties emitted")
    return prop_meta


def write_validation_report(prop_meta):
    md = [
        "# Validation report — executable payload properties",
        "",
        f"Generated {GENERATED} by `scripts/generate_artifacts.py` (production mode). "
        "This report lists the source and normalization of every property in "
        "`compose-item-payload.json`, and the checks applied.",
        "",
        f"## Executable properties: {len(prop_meta)}",
        "",
    ]
    if not prop_meta:
        md += [
            "**The production payload is intentionally empty.** No mapping currently has "
            "an Existing/Confirmed SharePoint side, because `03-sharepoint-schema/` holds "
            "no live schema evidence. The generator refuses to emit unevidenced internal "
            "names by construction.",
            "",
        ]
    else:
        md += ["| Property (internal name) | SP type | Source | Forms conf. | SP conf. | Normalization kind |",
               "|--------------------------|---------|--------|-------------|----------|--------------------|"]
        for p in prop_meta:
            src = f"`{p['forms_key']}`" if p.get("forms_key") else p["label"]
            md.append(f"| `{p['internal_name']}` | {p['sp_type']} | {src} | "
                      f"{p['forms_confidence']} | {p['sp_confidence']} | {p['kind']} |")
        md.append("")
    md += [
        "## Pipeline verification against dummy fixtures",
        "",
        "The identical generator + normalization pipeline is exercised end-to-end in "
        "fixture mode (`python3 scripts/generate_artifacts.py --fixtures`), producing 13 "
        "properties against the dummy `ZZFIXTURE_` schema and simulating them against "
        "two dummy bodies (sanitized response 6, and a synthetic edge-case body with "
        "quotes, apostrophes, backslashes, line breaks, Unicode and an emoji). "
        "Checks asserted by the simulation:",
        "",
        "- valid JSON round-trip (escaping of all JSON-sensitive characters);",
        "- blank answers become JSON `null` — never `''`, `0`, `false`, `'N/A'` or the string `'null'`;",
        "- Number fields receive integers; DateTime fields receive ISO-shaped strings;",
        "- the required `Title` is never null (falls back to `Form response <id>`; truncated at 255);",
        "- multi-choice answers (JSON-array strings) serialize to `'; '`-joined text.",
        "",
        "See `scripts/fixtures/output/simulation-results.FIXTURE.json`.",
        "",
        "## Still requiring live verification in Power Automate",
        "",
        "- the actual `Get response details` action name referenced by `outputs('Get_response_details')`;",
        "- the trigger path `triggerOutputs()?['body/resourceData/responseId']`;",
        "- date-only acceptance by the live DateTime column (vs needing `T00:00:00Z`);",
        "- live Choice sets, required flags and any column validation rules;",
        "- behaviour of the live list's Title settings (required/length).",
        "",
    ]
    (ROOT / "06-generated-output/validation-report.md").write_text("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", action="store_true")
    args = ap.parse_args()
    spec = json.loads((ROOT / "05-mapping-spec/mapping-spec.json").read_text())
    if args.fixtures:
        run_fixtures(spec)
    else:
        run_production(spec)
