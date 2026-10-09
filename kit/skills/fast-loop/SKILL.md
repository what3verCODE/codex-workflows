---
name: fast-loop
description: Fast path for a small, clear task: the main agent builds it alone, runs the checks, and gets one parallel review pass. No plan, no workers, one review round. Use when the user says "$fast-loop TICKET-42" or asks for a quick change (add a field or flag, an obvious fix, a rename).
---

# Fast loop

The user picked speed. You do the whole task yourself. The only subagent is one reviewer, and it runs while you run the checks. Aim for minutes, not a process.

## 1. Understand

1. `vcs-bridge`: find the VCS and record the baseline. Skip anything you already know from this session.
2. Read the ticket. No tracker access: ask the user to paste it.
3. Read the project instructions for the folders you will touch.
4. Search yourself. No scout.

Stop and suggest `dev-loop` if the task is bigger than it looked: more than one module, an open design question, a bug with an unclear cause, or an ask you cannot pin down in one sentence. One line, then wait.

## 2. Build

Follow `ponytail`: reuse what exists, make the smallest complete change, and finish every caller the change breaks.

Tests: add or update the test for the changed behavior next to the existing ones. Write it first when that is cheap. If the project has no tests in that area, say so and skip.

## 3. Check and review at once

Make a local checkpoint (see `vcs-bridge`). Then, in the same turn:

- Send one **reviewer** with this brief:

```
Run the ponytail-review skill on this change.
Baseline: <id>, diff: <command>, VCS: <tool>
Spec: <ticket/acceptance criteria>
Return only Must fix and Should fix findings.
```

- Meanwhile, run the checks yourself: the tests closest to the change, then lint/type/build for the touched files. Full suites only if they are fast.

The user says "no review", or subagents are unavailable: skip the reviewer and read the diff once yourself against the ponytail-review questions. Say the review was not independent.

## 4. Fix once

For each reviewer finding, open the cited lines and check the concrete case. Fix the ones you confirm, rerun the affected checks, and checkpoint. No second review. Drop the findings you cannot confirm, and list them in the report.

## 5. Report

```
Changed: <behavior, 1-2 lines>
Files: <list>
Checks: <command> → <result> (actual output)
Review: <fixed: titles | open: titles | none | skipped>
Baseline → checkpoint: <ids>
Not checked: <list, or none>
```

Publishing (submit, push, PR) only when the user or project rules allow it.
