# Architecture for many forms, one store

Design note. **Nothing here is built** — this is the shape to adopt before a
second form exists, plus one fix worth making to the current flow regardless.

## The problem with scaling the current design

Today the mapping is **form → list, directly**. The payload in the flow encodes
both "which Forms key" and "which SharePoint column" in one place.

Add a second form and you copy the flow, edit 61 properties, and now have two
copies of the same destination knowledge. Change the list and you edit both.
With *N* forms and *M* destination changes that is *N×M* edits, and the copies
drift silently — the second flow keeps writing to a column the first one
stopped using, and nothing tells you.

## ⚠ Fix this now: the duplicate check collides across forms

`Duplicate check` filters on `FormResponseID eq '<id>'`. Response IDs restart
at 1 **per form**. The moment a second form feeds this list, response 7 from
form B matches the item created by response 7 from form A — and the flow
concludes it is a duplicate and **silently skips creating the item**.

Silent data loss, triggered by adding a form, with no error to notice.

The fix is cheap and worth doing now even with one form:

```
$filter=FormResponseID eq '<id>' and SourceForm eq '<form name>'
```

`SourceForm` is already populated as a per-form constant, so nothing else
changes. Alternatively store a composite key (`INTAKE-7`) in `FormResponseID`,
but the two-clause filter is less invasive.

**Do this before cutover.** It is one Uri edit and one re-test.

## The shape to adopt: a canonical contract

Insert one layer so that neither side knows about the other:

```
Form A ─┐
Form B ─┼─→  adapter (per form)  →  CANONICAL SUBMISSION  →  writer (one)  → list
Form C ─┘    r-keys → canonical      a documented contract    canonical → columns
```

- **Adapter, one per form.** Trigger, `Get response details`, and a Compose
  that renames that form's opaque keys into canonical field names. This is the
  *only* place a form's r-keys appear. Small, and it is exactly the artefact
  this project already produces.
- **Canonical submission.** A documented object — `opportunityDescription`,
  `sponsor`, `anticipatedLaunchDate`, `strategicGoals`, … — with defined types
  and null rules. Not tied to Forms or SharePoint.
- **Writer, one for all forms.** Takes canonical, builds the labelled text,
  runs the AI, composes the payload, does the duplicate check and the HTTP
  create. All the logic this project built lives here, once.

Cost model changes from *N×M* to *N+M*: change a form and only its adapter
moves; change the list and only the writer moves.

### In Power Automate terms

The writer becomes a **child flow** (`Run a Child Flow`), which requires the
flows to live in a **solution**. Adapters call it with the canonical object as
a JSON parameter.

If solutions are unavailable or unwelcome, the fallback is to keep one flow per
form but **generate** each payload from a shared spec in this repo, so the
duplication is mechanical and re-derivable rather than hand-maintained. Weaker,
but it preserves the single source of truth.

## How the list should be shaped

Three options, in order of preference for your situation:

1. **One list, core + optional columns.** Define a small set of columns every
   form must supply (description, sponsor, dates, submitter, source form,
   response ID, the audit fields) and let each form additionally populate the
   subset it has. Works well when forms are variants of one another — which
   innovation-intake forms usually are. Sparse columns are cheap in SharePoint.
2. **One list per form plus a rollup view** (Power BI, or a search-driven
   page). Choose this if the forms are genuinely different domains; a union
   schema would otherwise become unreadable.
3. **Dataverse instead of a list.** Proper relational modelling, per-table
   security, real referential integrity. The right answer at scale, but it is a
   licensing and governance decision, not a technical one — do not drift into
   it by accident.

Recommendation: **option 1**, with the discipline that a new form may only add
columns, never repurpose an existing one.

## Repository layout for multiple forms

Current layout assumes one form (`01-forms-excel/`, `02-get-response-details/`).
For several:

```
forms/
  innovation-intake/        evidence + key mapping for this form
  <second-form>/            same structure
shared/
  canonical-contract.md     the field list, types, null rules
  sharepoint-schema/        destination evidence (one per list)
  writer/                   payload generator, harness, test matrix
```

The generator gains a form argument; `mapping-spec.json` becomes one per form,
each mapping r-keys → canonical rather than r-keys → columns. The quality gate
and executability rule are unchanged.

## What to do, and when

**Before cutover (minutes):**
- Add `and SourceForm eq '<form name>'` to the duplicate-check filter. Real bug,
  trivial fix.

**Before the second form (half a day):**
- Write `canonical-contract.md` — the field list is already implicit in the
  current mapping spec, so this is mostly transcription.
- Extract environment values into `config.json` (already recommended in the
  portability assessment).
- Decide solution-vs-generated-duplication for the writer.

**When the second form arrives:**
- Build only its adapter. If you find yourself copying the writer, stop — that
  is the signal the canonical layer is needed and is being skipped.

**Do not do now:** none of this should touch the flow currently under test,
beyond the duplicate-check filter. Ship what works, then refactor deliberately.
