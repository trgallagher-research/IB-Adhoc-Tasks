# Git exposure assessment and remediation note

Reviewed 2026‑07‑28. Scope: data previously committed to this repository's
shared history for this project folder. Nothing here is reproduced verbatim;
locations are referenced by commit.

## Findings

1. **Commits `da5a9ce` and `2de68e3`** (branch history, also reachable from
   `master`): the original `Get response details` capture was committed with
   its full HTTP **headers**, which include the tenant ID GUID, environment and
   subscription identifiers, routing/session/correlation GUIDs, and a creator
   object ID — plus the form owner's work **email address** in the `responder`
   property. The commit at `2de68e3` also moved the file to a malformed path
   (`sanitized/02-get-response-details/raw/…`), contradicting the project's own
   raw/sanitized rule.
2. **Commit `c19916d`**: the Forms Excel reference was committed with the
   owner's real **name and email** in the metadata columns (all six responses
   were the owner's own dummy submissions).
3. **No third-party respondent data** was found in either file: every response
   is dummy content submitted by the form owner. No credentials, cookies,
   tokens or secrets were found in any committed file.

## Severity assessment

Low. The exposed items are the owner's own work identity and tenant/instance
*identifiers* — none are credentials and none authenticate anything by
themselves. They do, however, breach the repository's public-safe rule and the
project README's own sanitized-content rules.

## Working-tree remediation applied (this branch, 2026‑07‑28)

- Headers stripped and `responder` redacted into
  `02-get-response-details/sanitized/get-response-details-response-6.body.json`;
  the malformed nested path was removed.
- The Excel reference was re-saved with Email/Name metadata values replaced by
  placeholders (and the doubled `.xlsx.xlsx` extension fixed); the original was
  removed from the working tree.
- The quality gate (`scripts/validate_spec.py`) now scans all committed text
  files for email addresses, token/JWT/cookie patterns and fixture leakage on
  every run.

## History remediation — options, needs your decision

The original files remain reachable in git history (including on `master`).
Per the working rules, shared history has **not** been rewritten.

| Option | What it does | Cost / caveats |
|--------|--------------|----------------|
| A. Accept | Leave history as-is; working tree is clean | Fine while the repo is private; the public-safe rule is then only prospective |
| B. Rewrite | `git filter-repo` to drop the two blobs, force-push `master` + branches | Requires your explicit approval; rewrites shared history; any clones must re-clone; GitHub cached views need a support ticket to purge |
| C. Rotate the repo | New repo from a clean tree; archive this one private | Simplest "truly clean" path if the repo should ever go public; loses issue/PR history |

Recommendation: **A** while the repository stays private, revisited before any
visibility change (then B or C). No action has been taken beyond the working
tree; say the word and I'll prepare B as an exact command script for review.
