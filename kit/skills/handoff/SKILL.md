---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include suggested skills by their installed names and paths. The next agent can read the relevant SKILL.md files when no skill-loading tool is available.

Record the current objective and accepted constraints, affected repository/workspace paths, chosen VCS and native task/change identifiers, original comparison baselines, current checkpoints, relevant pending local work, completed work, failed or unavailable checks, unresolved decisions, and the next concrete action. Carry forward the review round and remaining work when handing off an active development-loop; a new conversation does not reset those limits. Distinguish observed results from planned checks.

Use a unique temporary filename and return its absolute path. If the user requests a durable destination, use it. Writing a handoff does not launch another agent or publish the document.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, revisions, snapshots, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
