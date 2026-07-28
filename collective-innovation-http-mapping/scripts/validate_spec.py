#!/usr/bin/env python3
"""Quality gate for the mapping project. Exits non-zero on any failure.

Checks:
  1  spec/inventory consistency (counts, key existence, no duplicate assignments)
  2  confidence-state validity and the Probable-never-executable rule
  3  executable output purity: only Existing/Confirmed, evidenced names, no
     fixture identifiers, no Probable/Unresolved keys in the production payload
  4  public-safety scan over committed text files: no email addresses (other
     than *.invalid examples), no tokens/secrets patterns, no cookies
  5  fixture leakage: ZZFIXTURE_ must not appear under 06-generated-output/
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []
warnings = []


def fail(msg):
    failures.append(msg)


KIND_TYPE = {  # answer shape -> acceptable live SharePoint type prefix
    "free text": ("Note", "Text"),
    "date": ("DateTime",),
    "rating 1-5": ("Number",),
    "Yes/No": ("Choice",),
    "multi-choice": ("Note",),
}


def check_spec():
    spec = json.loads((ROOT / "05-mapping-spec/mapping-spec.json").read_text())
    schema_path = ROOT / "03-sharepoint-schema/sanitized/knowledge-submissions-schema.json"
    schema_fields = {}
    if schema_path.exists():
        schema_fields = {f["InternalName"]: f
                        for f in json.loads(schema_path.read_text())["fields"]}
    keys_inv = json.loads((ROOT / "02-get-response-details/sanitized/"
                           "response-keys-inventory.json").read_text())
    forms_inv = json.loads((ROOT / "01-forms-excel/sanitized/"
                            "forms-question-inventory.json").read_text())
    known = {k["response_key"] for k in keys_inv["keys"]}
    q = spec["question_mappings"]

    if len(q) != 41:
        fail(f"expected 41 question mappings, found {len(q)}")
    if forms_inv["_provenance"]["totals"]["columns"] != 47:
        fail("forms inventory no longer has 47 columns")
    if len(known) != 48:
        fail(f"expected 48 opaque keys, found {len(known)}")

    valid_states = {"Existing", "Confirmed", "Probable", "Unresolved"}
    assigned = []
    for e in q:
        if e["forms_key_confidence"] not in valid_states:
            fail(f"{e['map_id']}: invalid confidence {e['forms_key_confidence']}")
        if e["forms_response_key"]:
            if e["forms_response_key"] not in known:
                fail(f"{e['map_id']}: key {e['forms_response_key']} not in observed body")
            assigned.append(e["forms_response_key"])
            if e["forms_key_confidence"] not in ("Existing", "Confirmed", "Probable"):
                fail(f"{e['map_id']}: key assigned but confidence {e['forms_key_confidence']}")
            if not e["forms_key_evidence"]:
                fail(f"{e['map_id']}: assigned key without evidence")
        for c in e.get("forms_key_candidates") or []:
            if c not in known:
                fail(f"{e['map_id']}: candidate {c} not in observed body")
        if e["executable"]:
            sp = e["sharepoint"]
            if e["forms_key_confidence"] not in ("Existing", "Confirmed"):
                fail(f"{e['map_id']}: executable with forms confidence {e['forms_key_confidence']}")
            if sp["confidence"] not in ("Existing", "Confirmed") or not sp["internal_name"]:
                fail(f"{e['map_id']}: executable without evidenced SharePoint internal name")
            if schema_fields:
                f_ = schema_fields.get(sp["internal_name"])
                if f_ is None:
                    fail(f"{e['map_id']}: internal name {sp['internal_name']} not in live schema")
                else:
                    if f_["ReadOnlyField"]:
                        fail(f"{e['map_id']}: {sp['internal_name']} is read-only")
                    ok_types = KIND_TYPE.get(e["forms_answer_shape"])
                    if ok_types and not f_["TypeAsString"].startswith(ok_types):
                        fail(f"{e['map_id']}: answer shape {e['forms_answer_shape']} vs live "
                             f"type {f_['TypeAsString']}")
                    if e["forms_answer_shape"] == "Yes/No" and f_["Choices"]:
                        if not {"Yes", "No"} <= set(f_["Choices"]):
                            fail(f"{e['map_id']}: live choices {f_['Choices']} lack Yes/No")
    dupes = {k for k in assigned if assigned.count(k) > 1}
    if dupes:
        fail(f"duplicate key assignments: {dupes}")
    return spec


def check_production_payload(spec):
    p = ROOT / "06-generated-output/compose-item-payload.json"
    if not p.exists():
        fail("06-generated-output/compose-item-payload.json missing — run generate_artifacts.py")
        return
    art = json.loads(p.read_text())
    payload_text = json.dumps(art["compose_input"])
    if "ZZFIXTURE" in payload_text:
        fail("fixture internal names leaked into production payload")
    schema_path = ROOT / "03-sharepoint-schema/sanitized/knowledge-submissions-schema.json"
    if schema_path.exists():
        schema_names = {f["InternalName"]
                        for f in json.loads(schema_path.read_text())["fields"]}
        schema_names.add("ContentTypeId")  # REST-settable system property (preserved from Create item)
        for name in art["compose_input"]:
            if name not in schema_names:
                fail(f"payload property '{name}' not present in live schema")
    bad_conf = {"Probable", "Unresolved"}
    for e in spec["question_mappings"]:
        if e["forms_key_confidence"] in bad_conf and e["forms_response_key"]:
            if e["forms_response_key"] in payload_text:
                fail(f"{e['map_id']}: non-executable key present in production payload")
        for c in e.get("forms_key_candidates") or []:
            if c in payload_text:
                fail(f"{e['map_id']}: unresolved candidate key present in production payload")
    n_exec = sum(1 for e in spec["question_mappings"] if e["executable"])
    n_props = len(art["compose_input"])
    # metadata/Title properties may add to question props once schema evidence exists
    if n_props < n_exec:
        fail(f"payload has {n_props} properties but spec marks {n_exec} executable")


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SECRET_PATTERNS = [
    (re.compile(r"eyJ[A-Za-z0-9_-]{20,}"), "possible JWT"),
    (re.compile(r"(?i)client_secret\s*[:=]\s*['\"]?[A-Za-z0-9~._-]{10,}"), "client secret"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{20,}"), "bearer token"),
    (re.compile(r"(?i)(fedauth|rtfa)="), "SharePoint auth cookie"),
    (re.compile(r"(?i)[a-z0-9-]+\.sharepoint\.com"), "tenant SharePoint hostname (redact to <site-url>)"),
    # Microsoft Forms form_id: long opaque token containing _ or -. The
    # ContentTypeId constant is long too but is pure hex, so it does not match.
    (re.compile(r"\b(?=[A-Za-z0-9_-]{70,}\b)[A-Za-z0-9]*[_-][A-Za-z0-9_-]{60,}\b"),
     "possible Microsoft Forms form_id (must stay redacted; live flow is its source of truth)"),
]
SCAN_EXT = {".md", ".json", ".py", ".sh", ".txt", ".jsonc"}


def check_public_safety():
    for f in sorted(ROOT.rglob("*")):
        if not f.is_file() or f.suffix not in SCAN_EXT:
            continue
        if "/raw/" in str(f) or "/.git/" in str(f):
            continue
        text = f.read_text(errors="replace")
        rel = f.relative_to(ROOT)
        for m in EMAIL_RE.finditer(text):
            addr = m.group(0)
            if addr.endswith(".invalid") or "@example." in addr:
                continue
            fail(f"{rel}: real-looking email address '{addr}'")
        for pat, label in SECRET_PATTERNS:
            if pat.search(text):
                fail(f"{rel}: {label} pattern")
        # fixture identifiers must never reach executable artefacts; prose docs may
        # reference the prefix when describing the fixture pipeline
        if (f.parts[-2:][0] == "06-generated-output" and f.suffix in (".json", ".jsonc")
                and "ZZFIXTURE" in text):
            fail(f"{rel}: fixture identifier in executable generated output")


if __name__ == "__main__":
    spec = check_spec()
    check_production_payload(spec)
    check_public_safety()
    if failures:
        print("QUALITY GATE FAILED")
        for m in failures:
            print("  FAIL:", m)
        sys.exit(1)
    print("QUALITY GATE PASSED — spec consistent, executable output pure, "
          "no emails/secrets/fixture leakage in committed text files")
