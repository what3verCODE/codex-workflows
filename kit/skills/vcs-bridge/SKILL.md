---
name: vcs-bridge
description: Map git, GitHub and branch wording in other skills to the project's real version control and tracker. Use before any diff, commit, branch, worktree, PR or issue step when the project may not use git or GitHub.
---

# VCS bridge

Other skills are written for git and GitHub. Many projects use something else. Translate; never force git onto a project that does not use it.

## 1. Find the real tools (once per task)

Check, in order, and stop at the first answer:

1. Project instructions: `AGENTS.md`, `CLAUDE.md`, `docs/agents/issue-tracker.md`, contributing docs.
2. What exists on disk: `.git`, `.hg`, `.jj`, `.svn`, `.p4config`, or a project-specific VCS directory or CLI named in the docs.
3. Ask the user once. Record the answer in the conversation.

A `.git` folder or a GitHub URL does not prove the project uses git for work. Project instructions win.

## 2. Translate

| Other skills say | Do instead |
| --- | --- |
| `git diff <base>...HEAD` | The project's diff between the recorded baseline and the current state, including uncommitted work. |
| `git log`, commit SHA | The project's history command and its stable revision or change ID. |
| commit | The project's local checkpoint (commit, shelve, snapshot, pending change). Never a shared submit unless the user allowed publishing. |
| branch, integration branch | The project's unit of isolated work (branch, change, changelist, workspace). If it has none, work in place. |
| worktree | A separate working copy only if the project supports it and the user manages it. Otherwise run sequentially. |
| PR / MR | The project's review request. Draft it; publish only when allowed. |
| `gh issue …`, GitHub Issues | The tracker in `docs/agents/issue-tracker.md` or the project docs. No access: say so and ask for the ticket text. |

If a command is unknown, read the tool's `--help` before guessing.

## 3. Rules

- Record the baseline (revision or snapshot) before the first edit. Diffs and reviews compare against it, not against "latest".
- Keep unrelated local edits. Never revert, stash or overwrite work you did not make.
- No VCS at all: copy the touched files to a scratch folder before editing, and diff against that copy.
