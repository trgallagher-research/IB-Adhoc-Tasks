# Consolidated evidence request

Everything repository-local that could be built from current evidence has been
built. The items below are the only remaining blockers; each lists exactly what
to capture, where to put it, and what it unblocks. Work them in order — EV‑1
and EV‑2 unblock the most.

Reminder for all captures: place unredacted originals in the relevant
`raw/` folder (git-ignored), then a redacted copy in `sanitized/` following the
folder's instructions file. Dummy submissions only; never real submission text.

## EV‑1 — Live SharePoint schema export — ✅ COMPLETE (2026‑07‑28)

Captured via browser GET (ATOM XML), transcribed and redacted into
`03-sharepoint-schema/sanitized/knowledge-submissions-schema.json`. Key results:
every question has a uniquely corresponding destination field; `FormResponseID`
exists but is **Text** (quote filter values, send strings); `ReviewStatus`
default `Not reviewed` confirmed; `ProcessingStatus` default `Processed`;
`ComplianceBoundaryAdaptation` has a third choice "I don't know";
`StrategicGoals`/`ImpactedProgrammes` are multiline text; Title not required;
no supporting-files column. The executable payload now carries 12 properties.

## EV‑2 — Existing flow Peek-code captures — ✅ COMPLETE (2026‑07‑28)

Captured: trigger, Get response details, Run a prompt (containing the
labelled-submission construction that pairs ALL 41 question labels with their
keys), 3 of 8 Select actions, and Create item. Filed sanitized in
`04-existing-flow/sanitized/`. Result: **every question key is now `Existing`**,
the trigger response-ID path and the `Get_response_details` action name are
verified, all flow-layer mappings are preserved verbatim, and the payload is
complete at 61 properties. The five uncaptured Selects are non-blocking (names
and join expressions evidenced via Create item; the AI layer is preserved
as-is) — capture them only if you ever rebuild that layer.

## EV‑3 and EV‑4 — ✅ SUPERSEDED by EV‑2

The response‑2 capture and the three disambiguation submissions existed only to
resolve Forms keys. EV‑2's labelled-submission construction resolved all 41
keys directly (and consistently with every piece of dummy-test evidence), so
neither is needed. A full dummy submission still happens anyway as test T2 in
the test matrix, which doubles as an end-to-end cross-check of every mapping.

## EV‑5 — Small confirmations

1. **Still open:** in the Forms editor, confirm **Implementation Readiness
   Notice** is a text/section element with no input (current determination:
   no SharePoint destination — now also supported by the schema having no
   corresponding field).
2. ✅ List title confirmed `Knowledge Submissions` (EV‑1 capture succeeded on it).
3. ✅ `FormResponseID` column exists (Text, 255). No column creation needed.
4. Site URL: keep it out of the repo; you have it for the action configs.

## What happens when evidence lands

```
./scripts/run_checks.sh
```

regenerates inventories → spec → reports → payload → validation report and runs
the quality gate. Mapping upgrades happen only in `scripts/build_mapping_spec.py`
(with evidence strings), never by hand-editing generated files.
