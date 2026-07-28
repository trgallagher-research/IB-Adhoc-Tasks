# Collective Innovation — HTTP Mapping

Working folder for mapping Microsoft Forms responses to their destination
SharePoint list and generating the HTTP request mapping used by the flow.

## Folder structure

| Folder | Contents |
|--------|----------|
| `01-forms-excel/` | Microsoft Forms responses exported to Excel |
| `02-get-response-details/` | Output of the flow's "Get response details" action |
| `03-sharepoint-schema/` | Target SharePoint list schema (columns / internal names) |
| `04-existing-flow/` | Export of the existing Power Automate flow |
| `05-mapping-spec/` | Field mapping specification (source → SharePoint) |
| `06-generated-output/` | Generated mapping artifacts / HTTP request bodies |

Folders `01`–`04` each contain two subfolders:

- **`raw/`** — unredacted, local-only inputs. **Never committed** (git-ignored).
- **`sanitized/`** — redacted inputs that are safe to commit.

`raw/` directories are intentionally absent from git; recreate them locally as
needed. Only `sanitized/` content is version-controlled.

## Data-handling rules

**`raw/` files must never be committed.** They are git-ignored so that
unredacted source data — real Forms exports, flow exports, response payloads —
never leaves the local machine.

**`sanitized/` files must not contain any of the following:**

- personal names
- email addresses
- access tokens
- cookies
- connection credentials
- tenant secrets
- real submission content

**The following *may* be retained in `sanitized/`, because the mapping cannot be
built without them:**

- opaque Microsoft Forms response keys (the question / response identifiers)
- SharePoint internal field names (e.g. `Title`, `field_5`, `OData__x0037_…`)

These are structural identifiers, not personal content.

## Mapping rules

- **Never map on field order alone.** Every generated mapping must be justified by
  a stable identifier (a Forms response key or a SharePoint internal name) or an
  explicit label match. Positional coincidence ("column 3 → column 3") is not a
  valid basis for a mapping.
- **Report unresolved mappings; do not guess.** Any source field that cannot be
  confidently matched to a destination field is listed as *unresolved* in the
  mapping spec for a human to resolve. A guessed mapping is worse than a flagged
  gap.
