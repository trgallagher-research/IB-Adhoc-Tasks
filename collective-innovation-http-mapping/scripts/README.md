# Scripts

Deterministic pipeline from evidence to artefacts. Run everything with:

```
./scripts/run_checks.sh
```

| Script | Reads | Writes |
|--------|-------|--------|
| `build_inventories.py` | Excel reference, sanitized response-6 body | `01-…/forms-question-inventory.{json,md}`, `02-…/response-keys-inventory.{json,md}` |
| `build_mapping_spec.py` | the two inventories + the evidence judgments encoded in the script | `05-mapping-spec/mapping-spec.json` |
| `build_reports.py` | `mapping-spec.json` | `05-mapping-spec/mapping-spec.md`, `unresolved-mappings.md`, `coverage-report.md` |
| `generate_artifacts.py` | `mapping-spec.json` | `06-generated-output/compose-item-payload.json`, `validation-report.md` |
| `generate_artifacts.py --fixtures` | spec + `fixtures/fixture-sharepoint-schema.json` | `fixtures/output/*.FIXTURE.json` (dummy demo + simulations) |
| `validate_spec.py` | everything above | exit code — the quality gate |

Rules enforced by the gate: spec/inventory consistency; every assigned key
exists in the observed body; Probable/Unresolved never reach executable output;
no fixture identifiers in executable artefacts; no email addresses (outside
`*.invalid` examples), tokens, JWTs or cookie patterns in committed text files.

Requires Python 3 with `openpyxl` (only for `build_inventories.py`).

When SharePoint schema / flow evidence arrives: add an ingest step or extend
`build_mapping_spec.py` with the internal-name assignments plus their evidence
strings, then re-run the pipeline. `generate_artifacts.py` will emit the
non-empty payload automatically once mappings become executable.
