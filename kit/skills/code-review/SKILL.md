---
name: code-review
description: Review a fixed task change with independent standards, specification and technical specialists, then consolidate evidence-backed findings into one review round.
---

## Pin the change

Read `../workflow-context/SKILL.md`. Resolve the task, original per-repository baselines and current checkpoints from supplied evidence and workspace VCS tools. For a review request, retrieve metadata, changed files and per-file changes through the project's configured review host and VCS tools. Use stable revision or snapshot identifiers, including supplied non-Git comparisons. Missing task evidence limits specification review; it does not justify inventing a spec. Ask only when the comparison itself remains ambiguous.

Every specialist inspects the complete task change between the original baselines and these checkpoints. Include relevant pre-existing task work in that range. Verify the source state before and after analyses. If files change during review, discard affected conclusions and report the inconsistent state; do not call a mixed-state review complete. Review children are read-only and never run coordinating reviews or repairs.

## Independent analyses

Launch bounded specialists with fresh context, the same task, comparison and checkpoint table, and source/rule references. Use available slots, queueing independent analyses if necessary. Do not pass another specialist's conclusions as evidence. Read direct dependencies needed to understand behavior and record those left unread.

Separate specification and standards analysis. Retain useful judgments from [smells.md](smells.md), with documented project rules taking precedence. Assign applicable technical categories among independent specialists; account for every row below each round.

| Category | Evidence to inspect |
| --- | --- |
| Specification | Acceptance criteria, ticket comments, requested scope, missing or extra behavior |
| Standards | Applicable project rules and referenced conventions; label design smells as judgments |
| Correctness | Boundary inputs, invariants, error handling and changed callers |
| Architecture and maintainability | Interfaces, change coupling and concrete maintenance costs |
| Runtime defects | Lifecycle, concurrency, cleanup, resource use and failure paths |
| Security | Trust boundaries, authorization, injection, secret handling and changed dependencies |
| Accessibility | Relevant semantics, keyboard behavior, focus, labels and contrast evidence |
| Type safety | Invalid states, narrowing, assertions and boundary validation |
| Reuse | Existing code, dependencies and trusted packages, including relevant internal packages; suitability and dependency cost |
| Test quality | Available unit, visual and E2E tests, meaningful regression coverage, TMS alignment when available |
| Documentation | Factual accuracy against source/task, consistency, local rules and prose quality |

For React, inspect hook dependencies, cleanup and stale closures. Consult trusted primary package documentation when reuse findings require facts not present locally. Manual UI validation remains the user's work. Mark each category reviewed, inapplicable with a reason, or unavailable with missing evidence/tool. Missing visual or TMS access is a limit, not proof of a defect. Documentation-only changes require source and prose review, not code tests.

## Consolidate one round

Each finding must include an exact file/line or source reference, category origins, the requirement or rule where applicable, evidence, user impact and a concrete correction. Reject unsupported claims and style preferences. Use these severities consistently:

- P0: immediate catastrophic impact, blocking.
- P1: severe defect in supported use, blocking.
- P2: actionable defect or unmet requirement, blocking when it prevents acceptance.
- P3: optional improvement, nonblocking.

Merge duplicates by root cause and correction while retaining every standards/spec and specialist origin. A duplicate's severity reflects the strongest supported impact. Keep optional suggestions distinct from required corrections. Include the checkpoint/baseline table, category coverage, consolidated findings, unread dependencies and limits. Explicitly state whether blocking issues remain. All specialist outputs together are one review round. Return results to the coordinator; the review skill does not start a repair loop.
