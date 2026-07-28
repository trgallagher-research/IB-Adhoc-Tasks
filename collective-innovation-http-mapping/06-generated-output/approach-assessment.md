# Approach assessment — Compose + `Send an HTTP request to SharePoint`

Requested direction: retain the existing flow and replace only the standard
`Create item` mapping with a Compose-built payload posted via the authenticated
SharePoint HTTP action. Assessed critically against the realistic alternatives.

## Options considered

### A. Standard `Create item`, completed field-by-field in the designer

- The connector resolves internal names and types for you and surfaces fields
  in the UI — lowest REST knowledge required.
- **But** it does not remove the real hazards here: blank Forms answers arrive
  as empty strings, and `''` into Number/DateTime/Choice columns fails at run
  time, so each such field needs the *same* `if(empty(…), null, …)` expression
  the HTTP approach needs. The mapping is spread across dozens of designer
  fields, is hard to review as a unit, and cannot be generated, diffed or
  validated offline.
- Multi-choice and Choice handling in the connector has its own quirks (custom
  value toggles, `Enter custom value` per field), and the connector offers no
  way to *omit* a property conditionally.

### B. Compose + `Send an HTTP request to SharePoint` (preferred direction)

- One reviewable payload object; generated from the versioned mapping spec in
  this repository, so every property is traceable to evidence and regenerable.
- Same authenticated SharePoint connection and therefore the same permission
  envelope as the working `Create item` — no new consent, no Entra app, no
  secrets.
- Full control of null vs value (JSON `null` is accepted by the REST endpoint
  for Number/DateTime/text and leaves the column empty), of choice and
  multi-choice serialization, and of the duplicate-check that uses the same
  action type.
- Costs: internal names must be evidenced (this project's whole point), REST
  error messages are raw OData, and future maintainers need to know the payload
  is generated, not hand-typed. Mitigated by the generated artefacts and the
  validation report in this folder.

### C. Graph API / external script / new app registration

Rejected under the stated constraints: needs admin consent or secrets, adds an
external runtime, and provides nothing the site-scoped connector call doesn't.

### D. Power Apps / list forms / manual re-entry

Not automation; out of scope.

## Recommendation

**Proceed with B (Compose + HTTP), as preferred.** With the payload generated
from the reviewed mapping spec it is at least as safe as A and materially more
maintainable and auditable. Two conditions:

1. **Endpoint choice:** use `POST _api/web/lists/getbytitle('Knowledge
   Submissions')/items` with `odata=nometadata` headers (no `__metadata` /
   entity-type body needed). Fall back to `ValidateUpdateListItem` only if a
   Person/Lookup field must be written later — it has different value
   conventions and is not needed for Phase 1.
2. **DLP check (real risk):** some tenants restrict the generic
   `Send an HTTP request to SharePoint` action via Data Loss Prevention policy
   even though `Create item` is allowed. This is testable in five minutes with
   a read-only GET in a copied flow (permission matrix, test P1). If the action
   is blocked, the fallback is option A implemented with the same null-guard
   expressions from the mapping spec — the spec work transfers unchanged.

## Explicitly out of scope for the payload

- AI-layer fields (Innovation Type, Horizon, Categorization, Ownership) and
  `OriginalSubmission` stay with the existing flow actions (`Existing`
  mappings, preserved once the flow export is captured).
- Human-review/governance and projected-impact fields stay blank at creation;
  `ReviewStatus` keeps its agreed default (assumed `Not reviewed`, pending flow
  evidence).
- File attachments: see Phase 1 file scope in the implementation instructions.
