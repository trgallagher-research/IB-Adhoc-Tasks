# Cutover and rollback plan

Principle: the original working flow is never edited. All changes live in a
copy; cutover is a trigger swap; rollback is the reverse swap. Both flows must
never be enabled simultaneously (double-processing).

## Deployment checklist (before any cutover)

- [ ] All evidence gaps in `EVIDENCE-REQUEST.md` closed; `./scripts/run_checks.sh` passes
- [ ] Every payload property `Existing` or `Confirmed` (validation report shows non-zero executable count and no placeholders)
- [ ] Copied flow built per `implementation-instructions.md`; action names match the expressions
- [ ] `Get response details` action name in the copy matches `outputs('…')` references
- [ ] Trigger concurrency = 1 set on the copy
- [ ] Duplicate-check column exists (and is indexed if the list can grow past 5,000 items)
- [ ] Permission tests P1–P4 passed and recorded
- [ ] Test matrix T0–T15 passed and recorded in `test-results-<date>.md`
- [ ] Dummy test items deleted from the list (identifiable by your responder email / known response IDs)
- [ ] Reviewer sign-off on the mapping spec (someone other than the author reads `05-mapping-spec/mapping-spec.md`)

## Cutover (5 minutes, reversible)

1. Note the last processed Form response ID in the production flow's run history.
2. **Turn off** the original flow.
3. **Turn on** the copied flow.
4. Submit one dummy response end-to-end; verify the created item (raw columns,
   AI columns, blank governance columns, ProcessingStatus, no duplicate).
5. Check no real submission arrived during the swap window: compare the Forms
   response list against items in SharePoint by response ID. If one is missing,
   process it by resubmitting the trigger is impossible for Forms — instead use
   the copied flow's manual replay path: temporarily create the item by running
   the copy's logic on the missed response ID (Get response details accepts a
   response ID parameter in a manually triggered utility flow).
6. Delete the cutover dummy item.
7. Leave the original flow **disabled but unchanged** for the rollback window
   (suggested: 2 weeks or 10 real submissions, whichever is later).

## Rollback (any time in the window)

1. Turn off the copied flow.
2. Turn on the original flow (unchanged, so behaviour is exactly pre-project).
3. Reconcile by response ID as in cutover step 5 for anything submitted during
   the incident.
4. Items created by the copied flow are identifiable by the duplicate-check
   column being populated; they can stay (they are supersets of what the old
   flow wrote) unless a mapping error corrupted them — in which case delete the
   affected items by response ID and reprocess after the fix.

## Post-cutover

- After the rollback window: keep the original flow exported (already in
  `04-existing-flow/raw/`) before deleting or archiving it; prefer disabling
  over deleting indefinitely.
- Any later mapping change follows the same loop: evidence → spec → regenerate
  → copy-edit → test matrix subset → swap.
