---
name: workflow-context
description: Resolve ticket evidence, project paths, local instructions and VCS scope for a workflow task or bounded scout assignment.
---

Resolve explicit user instructions first, applicable project rules and workspace evidence second, and defaults last. Use available tracker and VCS tools and their usage instructions. Tracker configuration and readiness labels are optional. A URL identifies a destination, not proof of tool access. Read ticket details, comments and supplied artifacts; report unavailable access and missing evidence.

Use an existing project-name/path table to locate relevant projects. Assign scouts independent, bounded path regions or MCP questions when useful. Keep broad search output in scouts. A scout returns exact paths, symbols or MCP references, relevant relationships, instruction-file locations, uncertainties and suggested next reads. Scope is the ticket's affected projects, not the whole table. Read mandatory instructions yourself before acting on a handoff, including ancestor and package instructions and referenced rules outside the starting directory.

Before implementation, resolve each project's chosen VCS and review host from its instructions and available tools. The review host and storage backend do not determine the working CLI: a GitHub review or a co-located .git directory does not override a project using another VCS. Use the documented native operations and inspect local help when syntax is uncertain.

Record repository or workspace path, VCS, original comparison baseline, current task/change identifier and relevant pre-existing edits. A task may use a branch, bookmark, changelist, revision, stream or snapshot; record only concepts the project actually uses. Include pending, staged and untracked work where supported. Preserve unrelated edits and use the task's original baseline rather than silently moving it to the current state. Local edits alone do not block work.

Reuse the existing task context. Create a branch, pending change or other isolated context only when the project's workflow calls for one; a branch and a staging area are not prerequisites. Ask only if ownership, baseline selection or overlapping edits remain ambiguous after inspection. Preserve unrelated task history. Additional working copies and concurrent tasks remain user-managed.

Use stable native revision or snapshot identifiers for comparisons and checkpoints. If a checkpoint operation also publishes shared state, such as a centralized submit, it needs existing publication authorization; do not submit merely to satisfy a local checkpoint step. Prefer an available local snapshot or review artifact when publication is outside scope. If no VCS exists, preserve comparable file snapshots or supplied artifacts and report the missing history or checkpoint capability without initializing a repository automatically.

Clarifications pause dependent work. Continue independent discovery, accept information supplied during implementation, and update the in-context task understanding before resuming. Never substitute elapsed time or a fixed failed-test count for the missing answer.
