# SharePoint schema — collection instructions

Goal: capture the **live** schema of the `Knowledge Submissions` list — internal
names, types, required flags, choice sets, defaults — as the authoritative
evidence for the SharePoint side of every mapping. No admin rights are needed:
any account that can *read* the list can read its schema.

Place results in `03-sharepoint-schema/raw/` (git-ignored) first, then copy a
redacted version into `03-sharepoint-schema/sanitized/` per the checklist below.

## Method A — browser REST call (recommended; read-only, no admin)

1. Sign in to the SharePoint site that hosts the list in a normal browser tab.
2. Open a new tab and paste this URL, replacing `<site-url>` with the site's
   URL up to (not including) `/Lists/`:

   ```
   <site-url>/_api/web/lists/getbytitle('Knowledge Submissions')/fields?$filter=Hidden eq false&$format=json
   ```

3. Save the full JSON response to
   `03-sharepoint-schema/raw/knowledge-submissions-fields.json`.
4. Also capture the list's entity type name (needed by the HTTP create call):

   ```
   <site-url>/_api/web/lists/getbytitle('Knowledge Submissions')?$select=ListItemEntityTypeFullName,Title,Id&$format=json
   ```

   Save to `03-sharepoint-schema/raw/knowledge-submissions-list.json`.
5. If the list title contains a typo or the call returns 404, list all lists to
   find the real title: `<site-url>/_api/web/lists?$select=Title&$format=json`.

Note: some tenants return an ATOM/XML feed despite `$format=json`. If so, either
save the XML (fine — it contains the same fields) or use Method B.

## Method B — one-off Power Automate action (uses the existing connection)

In a **copy** of the flow (or a throwaway instant flow with the same SharePoint
connection), add a `Send an HTTP request to SharePoint` action:

- Site Address: the site hosting the list
- Method: `GET`
- Uri: `_api/web/lists/getbytitle('Knowledge Submissions')/fields?$filter=Hidden eq false`
- Headers: `Accept` = `application/json;odata=nometadata`

Run it once, copy the raw outputs body from the run history into
`03-sharepoint-schema/raw/knowledge-submissions-fields.json`. Repeat with
`Uri = _api/web/lists/getbytitle('Knowledge Submissions')?$select=ListItemEntityTypeFullName`
for the entity type. This also *proves* the connection can read the list —
useful for the permission matrix.

## What the mapping needs from each field

`InternalName`, `Title` (display name), `TypeAsString`, `Required`,
`ReadOnlyField`, `Hidden`, `Choices` (for Choice fields), `DefaultValue`,
`EnforceUniqueValues`. Keep the whole field objects; do not trim properties.

## Redaction checklist for `sanitized/`

Remove or replace before committing:

- any real person names or emails appearing in field `DefaultValue`s or
  descriptions;
- the tenant/site URL (replace with `<site-url>`);
- GUIDs are structural and MAY stay, but the site URL must not;
- nothing else should need redaction — schema is structure, not content.

Suggested sanitized filename: `sanitized/knowledge-submissions-fields.json`.

## After ingest

Run `python3 scripts/ingest_sharepoint_schema.py` (see `scripts/README.md`) to
normalize the export, then re-run the spec build, reports and generator. The
SharePoint side of mappings only then becomes `Confirmed`.
