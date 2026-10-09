---
name: dev-loop
description: Take one ticket from description to reviewed, checkpointed change. Picks the lightest path that fits the task size. Use when the user gives a ticket ID, URL or task description and wants it implemented, e.g. "$dev-loop TICKET-42".
---

# Dev loop

You own the task from start to finish. Subagents are tools for speed and fresh eyes, not a ritual. Every handoff costs minutes, so use the fewest that still give a good result.

## 1. Understand (you, not a subagent)

1. Read the `vcs-bridge` skill. Find the project's VCS and tracker, and record the baseline.
2. Read the ticket and its comments. No tracker access: ask the user to paste it.
3. Read the project instructions (`AGENTS.md`/`CLAUDE.md` and those in the folders you will touch).
4. Find the code. Search yourself when you already know where to look. Send a **scout** only for broad or multi-project searches, several in parallel if the areas are independent.
5. Uncertain bug cause: send a **bughunter**. Known cause: skip.

If something would change what you build and the code cannot answer it, ask the user now. Keep going on independent parts while you wait.

## 2. Pick the path

| Size | Signs | Path |
| --- | --- | --- |
| **Small** | One area, a few files, clear ask (add a field or flag, fix an obvious bug, rename). | You implement it yourself, then step 4 with one reviewer. No scout, no plan. |
| **Medium** | Several files or one module, clear ask. | Write a short plan (5 lines max) in the chat, send one **worker**, then step 4. |
| **Large** | Many modules or projects, or open design questions. | Write a plan and **wait for the user to approve it**. Then workers, in parallel only on files that do not overlap. Then step 4. |

When unsure, pick the smaller path. Say which path you picked and why, in one line.

## 3. Build

Whoever builds (you or a worker) follows `ponytail` (the smallest complete change, reuse before writing) and `tdd` (red → green, one behavior at a time).

A worker brief contains exactly:

```
Goal: <one sentence: the behavior to add or change>
Ticket: <ID/link, plus acceptance criteria copied in>
Where: <files/symbols to start from; files the worker may change>
Baseline: <revision/snapshot>, VCS: <tool>
Checks: <exact test/lint/build commands>
Not in scope: <anything tempting but excluded>
Report: the worker's report format
```

Do not paste whole files or the ticket history. Give paths.

After the build, run the checks yourself and read the diff. A worker saying "done" is not proof.

Update docs only where the change makes them wrong (README, docs, memory-bank files near the code). Keep it to what changed.

## 4. Review (max 2 rounds)

Make a local checkpoint (see `vcs-bridge`), then run the `review` skill on the change against the baseline.

- **Verdict ship**: done.
- **Must/should fix findings**: fix them (yourself for small fixes, a worker otherwise), rerun checks, checkpoint, review **once** more.
- After round 2, stop. Report what is still open. No third round.

Nice-to-have findings go into the final report. Do not fix them unless asked.

## 5. Report

```
Path: small | medium | large
Changed: <behavior, 1-3 lines>
Files: <list>
Checks: <command> → <result> (actual output, not hope)
Review: round N → verdict; open findings: <numbers + titles, or none>
Baseline → checkpoint: <ids>
Not done / not checked: <list, or none>
```

Publishing (submit, push, PR) only when the user or project rules allow it. Default: leave a local checkpoint and a review-request description drafted with the `pr` skill.
