---
name: make-pr-easy-to-review
description: Prepare or update a code review request for human review with an accurate description, verification evidence and reading order. Use during pull/merge request, changelist or patch-review preparation, reviewability cleanup, or explicitly requested history cleanup.
---

# Make PR Easy to Review

Use whenever preparing or updating a review request, including a pull request, merge request, changelist or patch series, including the PR preparation portion of an authorized delivery task. Help the reviewer understand the problem, resulting behavior, important files, risk and verification. This step improves presentation; it does not replace correctness review.

## Workflow

1. Resolve the project's chosen VCS, review host, target change and comparison baseline from project instructions and the request. Use native tools. A hosting URL or co-located .git directory does not select the working VCS. If no hosted review exists, prepare a local review description against supplied revisions or file snapshots.
2. Inspect the task's revision/change sequence, pending edits, diff size, changed paths, generated files and existing review description. Include relevant pending work without mixing in unrelated changes.
3. Identify reviewability issues: noisy change history, stale description, unrelated changes, mixed mechanical and logic changes, missing tests, or unclear reviewer entry points.
4. Prefer description and reading-order improvements. Rewrite history only within an explicit user request or an agreed concrete plan. Reuse existing authorization; history cleanup is optional.
5. Apply authorized review updates, or return the prepared description when publication is not requested. Preserve unrelated existing description content and discussion. Verify that presentation-only work has not changed the code tree. Posting review comments is a separate external action requiring user authorization.

## History Cleanup

Only rewrite history when the user requests it or agrees to a concrete plan, and the chosen VCS supports the requested operation. An immutable submitted revision may require a follow-up change rather than a rewrite. Preserve the existing task context; neither a branch nor a staging area is required.

Before rewriting, record the original change identifiers, review metadata, pending work and exact task file contents using native snapshots or an equivalent complete content manifest. Compare the content intended for review, including relevant pending edits, rather than only a published revision. Preserve file paths, additions/deletions, executable modes and symlink targets where supported.

Group changes into coherent, independently understandable units, keeping tests with the behavior they verify. Schema, core logic, integration and UI changes can provide a useful reading order, but do not separate them mechanically when that breaks the dependency story.

After rewriting, verify content identity with the recorded snapshot using native comparison tools. Metadata changes alone should not change the deliverable. Unexpected content differences block publication until resolved. A centralized submit or shared update is publication even if it is also called a checkpoint by the VCS; existing authorization still applies.

## Reviewer Guidance

When code behavior should stay untouched, prefer the review description and reading notes:

- Lead with the concrete problem and resulting behavior, matching the final diff and project review template. For a small change, one or two sentences plus validation can be enough.
- Separate core files from generated or mechanical files.
- Call out risky behavior changes, migration order, rollout plan, and test coverage.
- Link issue trackers, dashboards, or design docs when they explain intent.
- Report checks actually run and their results, including unavailable validation and relevant rollout constraints. Scale reading-order guidance to the diff; a one-file fix does not need a walkthrough.
- Use structured tool arguments for multiline updates, or write the exact body to a temporary file and use the CLI's body-file option.

## Guardrails

- Never hide meaningful behavior changes inside "cleanup".
- Do not bypass hooks unless the user explicitly asks.
- If the change is too large to make reviewable with notes, recommend splitting instead of polishing around the problem.
