# Portability — moving the list, changing the form, moving tenant

Honest assessment of what survives a move and what has to be re-derived, with
effort estimates and a re-targeting checklist.

## The short answer

**The method and the machinery port cleanly. The identifiers never do.**

Everything expensive about this project was *establishing evidence* — proving
which opaque Forms key belongs to which question, and which SharePoint internal
name is the destination. That evidence is specific to one form and one list. It
cannot be carried over; it has to be re-established.

What *is* reusable is worth more than it looks: the evidence discipline, the
generator pipeline, the payload design decisions (null typing, escaping,
truncation, duplicate prevention), the sandbox harness and the test matrix.
Second time round you are re-running a known procedure rather than discovering
one.

## What breaks, by scenario

### A. Same form, new list or new site — **easy, ~30–60 min**

| Changes | Where |
|---------|-------|
| Site Address | both HTTP actions |
| List title in the Uri | both HTTP actions |
| `ContentTypeId` | payload — **list-specific, must be re-captured** |
| Internal names | payload — *only if the new list's differ* |

The trap: **internal names are fixed at column creation from the display name
at that moment**, and never change afterwards even if the display name does.
Hand-rebuilding a list almost never reproduces them exactly — you get
`Opportunity_x0020_Description` where the original had
`OpportunityDescription`, and every mapping silently breaks with a 400.

Mitigation, in order of preference:

1. **Save the existing list as a template** (or export a site script / PnP
   provisioning template) and create the new list from it. Internal names are
   preserved by construction.
2. Failing that, re-run the EV‑1 schema capture against the new list and
   regenerate — the mapping is by *label*, so re-pointing is mechanical, just
   not free.

Either way: re-capture the schema, re-run `./scripts/run_checks.sh`, re-run the
test matrix. The Forms side is untouched.

### B. Adding or removing questions on the existing form — **cheap, ~1 hour**

Forms response keys are **stable**. Adding, reordering or editing the wording
of a question does not change existing keys. Only new questions get new keys,
and deleted questions leave their key behind as one of the unexplained-surplus
kind already documented.

Procedure: capture one `Get response details` body after the change, diff the
key list against `response-keys-inventory.json`, and add the new keys to
`FLOW_KEYS` / `SP_ASSIGNMENTS` in `build_mapping_spec.py` with their evidence.

Do **not** forget the labelled-submission template — a new question must be
added there too, or the AI never sees it.

### C. A different form — **the expensive one, ~half a day**

Every one of the 41 keys is new. Nothing about the current mapping transfers.

Cost depends entirely on one thing: **does the new form's flow have a
labelled-submission construction?** That artefact — the thing that pairs each
question label with its key — is what collapsed this project from "design
disambiguation experiments" to "read the mapping off the flow". Response 8's
whole evidence chain came from it.

- **With one:** re-derivation is mechanical. Read label→key pairs, populate
  `FLOW_KEYS`, regenerate. Half a day including testing.
- **Without one:** you are back to correlating dummy submissions, and the
  Yes/No and 1–5 questions cannot be resolved from a single response. The
  disambiguation design (permuted ratings, unique Yes/No triples) is still in
  the repo history for exactly this case — budget two days.

**Recommendation: make a labelled-submission construction mandatory in any
future intake flow.** It costs nothing to build, it feeds the AI anyway, and it
doubles as a permanent, self-maintaining key registry.

### D. Different tenant — **add ~1 day of plumbing**

Everything in A and C, plus: form ID, connection references for all three
connectors, the AI Builder prompt (its `recordId` is environment-specific — the
prompt must be recreated and re-versioned), DLP policy re-check (test T0), and
the permission matrix re-run from scratch. None of it hard; all of it needs
someone with access.

## What ports unchanged

- **The mapping methodology** — confidence states, the never-map-on-order rule,
  the rule that a value like Yes/No/1–5 is not distinctive evidence. This is the
  part that stopped the project shipping a plausible-but-wrong mapping.
- **The generator pipeline** — `scripts/` is data-driven. Re-targeting means
  editing two dictionaries and re-running, not rewriting.
- **The quality gate** — the executability rule (nothing Probable or Unresolved
  reaches executable output) is domain-independent.
- **The payload design** — object-mode transfer, blank→JSON null typing, Number
  vs DateTime handling, Title truncation with fallback, duplicate prevention on
  response ID, TRY/CATCH. All of it is Forms→SharePoint generic.
- **The sandbox harness** — replay any response by ID with no writes. Rebuild in
  ten minutes against any form.
- **Test matrix, cutover and rollback plans** — reusable as-is.

## Re-targeting checklist

When moving, work in this order and stop at the first failure:

1. Capture the new list schema (EV‑1) → `03-sharepoint-schema/sanitized/`
2. Capture the new flow's actions (EV‑2), especially any labelled-submission
   construction → `04-existing-flow/sanitized/`
3. Update in `scripts/build_mapping_spec.py`: `FLOW_KEYS`, `SP_ASSIGNMENTS`,
   `NO_DESTINATION`, and the `ContentTypeId` constant in `FLOW_LAYER_MAPPINGS`
4. Update in `scripts/generate_artifacts.py`: `GRD_ACTION` and
   `RESPONSE_ID_EXPR` if the new flow names differ
5. `./scripts/run_checks.sh` — the gate fails loudly on any name not present in
   the new schema
6. Rebuild the sandbox harness, replay one response, check the payload
7. Rebuild the flow tail (Composes, TRY/CATCH, HTTP actions), new site and list
   in both Uris
8. Run the test matrix; T0 first if the tenant changed

## One change that would cut future cost

Environment-specific values are currently spread across the scripts (`GRD_ACTION`,
`RESPONSE_ID_EXPR`, `ContentTypeId`) and the flow (site URL, list title, form
ID). Extracting them into a single `config.json` — read by the generator,
with site/list/form as documented placeholders — would turn steps 3 and 4 above
into "edit one file".

Not done yet because it is refactoring with no benefit to the current
deployment. Worth doing **before** the first port, not after.
