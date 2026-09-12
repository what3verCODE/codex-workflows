---
name: resolving-merge-conflicts
description: Resolve conflicts in an in-progress merge, rebase, update, integration or change application using the project's VCS and the intent of both changes.
---

Read `../workflow-context/SKILL.md` to resolve the project's chosen VCS, current operation, task scope and pending work. Inspect native conflict state and record the source and target revisions or change identifiers. An unresolved conflict does not authorize starting a different integration or publishing the result.

Find primary evidence for each side: change descriptions, review discussion, linked tickets, tests and surrounding behavior. Determine what each change intends to preserve. Regenerate generated files and dependency lockfiles with the project's tools when appropriate.

Resolve conflicts to preserve both intents where compatible. When they conflict, follow the operation's established goal and explain the trade-off. If that goal does not settle the behavior, ask for the missing decision and continue only independent resolutions. Preserve unrelated local work. A failed resolution attempt does not authorize discarding work or aborting the operation; use existing instructions for recovery.

Run the project's relevant automated checks against the integrated result. Distinguish defects introduced by integration from pre-existing failures and unavailable tooling. Fix integration defects within scope and rerun affected checks.

Use native resolution markers or task-scoped staging where supported. Continue the existing operation when its intent is clear and doing so stays within authorization; some operations expose more conflicts across successive changes. Apply the same evidence and checks to later conflicts. A centralized submit or other shared update counts as publication and needs existing authorization. If finishing would publish without it, leave the resolved local state ready and report the remaining operation.

Return the resolutions and reasons, native operation status, checks and results, unresolved decisions, and any remaining continuation or publication step. Confirm conflict state through the VCS as well as the edited files before claiming resolution is complete.
