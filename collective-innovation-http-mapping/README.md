# Collective Innovation — HTTP Mapping

Working folder for mapping Microsoft Forms responses to their destination
SharePoint list and generating the HTTP request mapping used by the flow.

This project is developed with **dummy data committed straight to the repo**.
Nothing here is git-ignored, so there is one rule:

> **No real respondent data.** Fake all names, email addresses and answer
> content.

It is fine — and useful — to keep the *real* column headers, Microsoft Forms
response keys and SharePoint internal field names. Those are structural
identifiers, not personal content, and the mapping is built against them. So
the ideal input file has **real field structure with dummy row content**.

## Folder structure

| Folder | Contents (dummy) |
|--------|------------------|
| `01-forms-excel/` | Microsoft Forms responses exported to Excel |
| `02-get-response-details/` | Output of the flow's "Get response details" action |
| `03-sharepoint-schema/` | Target SharePoint list schema (columns / internal names) |
| `04-existing-flow/` | Export of the existing Power Automate flow |
| `05-mapping-spec/` | Field mapping specification (source → SharePoint) |
| `06-generated-output/` | Generated mapping artifacts / HTTP request bodies |

## Mapping rules

- **Never map on field order alone.** Every mapping must be justified by a stable
  identifier (a Forms response key or a SharePoint internal name) or an explicit
  label match — never by positional coincidence ("column 3 → column 3").
- **Report unresolved mappings; do not guess.** Any source field that cannot be
  confidently matched to a destination field is listed as *unresolved* in the
  mapping spec for a human to resolve. A guessed mapping is worse than a flagged
  gap.
