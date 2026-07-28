# Permission matrix

Scope: the SharePoint connection already used by the working flow, exercised
through `Send an HTTP request to SharePoint`. No Entra app registration, no
client secret, no Graph application permissions. You are not assumed to be a
SharePoint/Power Platform/tenant admin.

| # | Capability | Status | Evidence / test |
|---|-----------|--------|-----------------|
| P1 | Flow can run `Send an HTTP request to SharePoint` at all (not DLP-blocked) | **Requires controlled test** | In a copied flow, run the read-only schema GET from `03-sharepoint-schema/COLLECTION-INSTRUCTIONS.md` Method B. Instant pass/fail; a DLP block shows before/at run start, not as a SharePoint error. |
| P2 | Connection can read the `Knowledge Submissions` schema | **Likely but unproven** | Read normally accompanies write (Contribute includes read). Proven automatically by running P1's GET. |
| P3 | Connection can read list items (duplicate check) | **Likely but unproven** | Same reasoning as P2; proven by running the duplicate-check GET with a dummy response ID. |
| P4 | Connection can create items in the list | **Demonstrated** — by the currently working flow's `Create item` | The HTTP POST uses the same connection and the same underlying permission (AddListItems); carry-over is near-certain but confirm with one dummy POST in the copied flow (test matrix T1). |
| P5 | Connection can update items (only if a later phase updates processing status post-create) | **Likely but unproven** | Not needed for Phase 1 create-only design; test only if the design grows an update step. |
| P6 | Add a column to the list (e.g. `FormResponseId` if absent) | **Requires controlled test; possibly admin/list-owner action** | Try List settings → Create column in the browser. If the option is missing, ask the site owner — this is a site permission, not a tenant-admin task. |
| P7 | Index a column (throttling protection for the dup-check filter) | Same as P6 | List settings → Indexed columns. Only matters if the list can exceed 5,000 items. |
| P8 | Change tenant DLP policy (only if P1 fails) | **Administrative action** | Power Platform admin; outside your control — the fallback in the approach assessment avoids needing it. |
| P9 | Anything requiring Graph application permissions / app registration | **Not required by this design** | By construction. |

Reading the results: a P1 failure changes the approach (fallback to the typed
`Create item` with the same null-guard expressions); a P4 failure would
contradict the working flow and means the connection identity differs between
the original and copied flow — check which account owns the copied flow's
connection reference.
