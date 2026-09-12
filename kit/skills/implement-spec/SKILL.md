---
name: implement-spec
description: Implement an agreed specification across its dependency-linked tickets, coordinating existing roles and reviewing the combined result with the project's VCS and review tools.
---

# Implement a specification

Own delivery of one agreed specification and its ticket graph. Use `../development-loop/SKILL.md` for a standalone ticket instead. This coordinator reuses the existing context, readiness, implementation and review disciplines; it does not invoke a complete development-loop for every ticket.

## Establish the graph and baseline

Read `../workflow-context/SKILL.md`, the specification, its tickets and relevant discussion. Record acceptance criteria, dependency edges, completed work, original per-project comparison baselines and the existing integration context. A ticket is ready when its required predecessor changes are integrated and their agreed prerequisite checks are satisfied. For an explicitly planned wide refactor, combined acceptance checks may be deferred to an integration ticket. Record those deferred obligations and observed intermediate failures; they do not block successors whose purpose is to complete that agreed integration. Unexpected failures or unagreed breakage still block dependent work. Detect cycles, missing dependencies and ambiguous scope before dispatching dependent work.

Use an available scout for bounded discoveries that tickets need. Share paths, symbols, source links and findings through context pointers. Ask oracle to assess readiness and approach with `../prepared-task/SKILL.md`, reusing decisions and evidence already supplied. For uncertain defects, bughunter uses `../diagnosing-bugs/SKILL.md` to establish a cause before implementation.

Use the project's native integration context, which may be a pending change, workspace, branch or patch series. Extra working copies remain user-managed under workflow-context. Parallel implementation requires available isolated contexts and independent changes. If they are unavailable, integrate tickets sequentially in the current task context; creating branches or worktrees is not a prerequisite. Do not dispatch agents to overlapping mutable files.

## Implement and integrate

Dispatch ready tickets to workers using `../prepared-task/SKILL.md` and `../tdd/SKILL.md`. Give each worker its acceptance criteria, permitted paths/context, dependency state, any explicitly deferred checks and expected handoff. Deferred validation is not passing validation; report it separately. The coordinator owns the integration context, ticket graph and publication decisions. Documentation-only tickets use writer with `../workflow-writing/SKILL.md`.

Use available role configuration and concurrency limits. Each handoff records changed behavior and native change identifiers, checks actually run, unresolved concerns and dependent tickets it may unblock. A worker reporting completion does not by itself make successors ready.

Integrate one completed result at a time using the project's VCS operations. A worker may own a bounded integration assignment; the coordinator remains responsible for its result. If conflicts appear, use `../resolving-merge-conflicts/SKILL.md`. Check combined behavior at the affected boundaries, record an integrated checkpoint or snapshot, then update the ready frontier. For sequential work, the worker's checked result may already be the integrated state.

If a ticket is blocked, report the precise missing decision or dependency and continue independent ready tickets. Update tracker state only within existing authorization. Preserve handoff evidence and completed work so resuming does not redo tickets or reset original baselines.

## Verify and review the whole specification

When the graph is integrated, map the complete change back to the specification and run appropriate combined checks. Have writer update affected documentation. Capture current native checkpoints or snapshots for all affected projects without moving the original comparison baselines.

Reviewer reads `../code-review/SKILL.md` and reviews the whole specification change against those original baselines. All specialists in this pass belong to review round one. Correct blocking or actionable in-scope findings with workers and writer, rerun affected checks and checkpoint the corrections. Review the complete change once more when corrections were made. Stop after round two and report remaining findings; optional redesigns stay separate.

For an authorized review submission, writer uses `../make-pr-easy-to-review/SKILL.md`. Prepare or update the project's pull/merge request, changelist or patch review using actual verification evidence. A draft, publication, closing-link update or ready-for-review transition follows the task's existing authorization. Without publication authority, return the prepared local review material. Do not mark the work ready while blocking findings remain.

Return the ticket outcomes, integrated identifiers, original baselines, acceptance coverage, checks, review rounds, remaining blockers and review location or draft. Preserve user-managed working copies. Remove only temporary artifacts created for this invocation when their useful evidence has been retained and cleanup is within scope. When the user requests a session handoff, read `../handoff/SKILL.md` to carry the graph state and current review round into the next session.
