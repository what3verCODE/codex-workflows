---
name: workflow-context
description: Resolve ticket evidence, project paths, local instructions and VCS scope for a workflow task or bounded scout assignment.
---

Resolve explicit user instructions first, applicable project rules and workspace evidence second, and defaults last. Use available tracker and VCS tools and their usage instructions. Tracker configuration and readiness labels are optional. A URL identifies a destination, not proof of tool access. Read ticket details, comments and supplied artifacts; report unavailable access and missing evidence.

Use an existing project-name/path table to locate relevant projects. Assign scouts independent, bounded path regions or MCP questions when useful. Keep broad search output in scouts. A scout returns exact paths, symbols or MCP references, relevant relationships, instruction-file locations, uncertainties and suggested next reads. Scope is the ticket's affected projects, not the whole table. Read mandatory instructions yourself before acting on a handoff, including ancestor and package instructions and referenced rules outside the starting directory.

Before implementation, inspect each affected repository's VCS, configured base, branch conventions and existing edits. Record in conversation context a table of repository path, original comparison baseline, branch and relevant pre-existing edits. Include untracked and staged work in the inventory. For relevant existing task commits use the task's original base, not the current tip. Preserve unrelated edits and keep them out of checkpoints. A dirty workspace alone is not a blocker.

Reuse the task branch. Otherwise use the configured VCS to create a task branch from the configured base, preserving existing work. Ask only if task ownership, base selection or overlapping edits remain ambiguous after inspection. Do not reset, discard or silently carry unrelated task history into a new task. The user manages worktrees and concurrent tickets. A workspace may contain several repositories or use a non-Git VCS; capture fixed revision/snapshot identifiers and use its native comparison and checkpoint operations.

Clarifications pause dependent work. Continue independent discovery, accept information supplied during implementation, and update the in-context task understanding before resuming. Never substitute elapsed time or a fixed failed-test count for the missing answer.
