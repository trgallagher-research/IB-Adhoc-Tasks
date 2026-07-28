# Validation report — executable payload properties

Generated 2026-07-28 by `scripts/generate_artifacts.py` (production mode). This report lists the source and normalization of every property in `compose-item-payload.json`, and the checks applied.

## Executable properties: 0

**The production payload is intentionally empty.** No mapping currently has an Existing/Confirmed SharePoint side, because `03-sharepoint-schema/` holds no live schema evidence. The generator refuses to emit unevidenced internal names by construction.

## Pipeline verification against dummy fixtures

The identical generator + normalization pipeline is exercised end-to-end in fixture mode (`python3 scripts/generate_artifacts.py --fixtures`), producing 13 properties against the dummy `ZZFIXTURE_` schema and simulating them against two dummy bodies (sanitized response 6, and a synthetic edge-case body with quotes, apostrophes, backslashes, line breaks, Unicode and an emoji). Checks asserted by the simulation:

- valid JSON round-trip (escaping of all JSON-sensitive characters);
- blank answers become JSON `null` — never `''`, `0`, `false`, `'N/A'` or the string `'null'`;
- Number fields receive integers; DateTime fields receive ISO-shaped strings;
- the required `Title` is never null (falls back to `Form response <id>`; truncated at 255);
- multi-choice answers (JSON-array strings) serialize to `'; '`-joined text.

See `scripts/fixtures/output/simulation-results.FIXTURE.json`.

## Still requiring live verification in Power Automate

- the actual `Get response details` action name referenced by `outputs('Get_response_details')`;
- the trigger path `triggerOutputs()?['body/resourceData/responseId']`;
- date-only acceptance by the live DateTime column (vs needing `T00:00:00Z`);
- live Choice sets, required flags and any column validation rules;
- behaviour of the live list's Title settings (required/length).
