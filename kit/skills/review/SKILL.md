---
name: review
description: Review a change against a fixed baseline using code-review (standards + spec) and ponytail-review (bugs, risk, lean) in parallel, then verify every finding before reporting. Use for "review this change/ticket", and as step 4 of dev-loop.
---

# Review

Goal: a short list of real problems the user can trust without re-checking. A wrong finding costs more than a missed nit.

## 1. Pin the change

- Baseline and diff command from `vcs-bridge`. A bad baseline or an empty diff stops here.
- The spec: ticket text, acceptance criteria, or the plan from dev-loop. None: say so.

## 2. Two reviews at once

Start both in the same turn:

1. **`code-review`**: run the skill yourself. It starts its own Standards and Spec subagents. Give it the baseline, the diff command and the spec.
2. **`ponytail-review`**: send one **reviewer** subagent with this brief:

```
Run the ponytail-review skill on this change.
Baseline: <id>, diff: <command>, VCS: <tool>
Spec: <ticket/acceptance criteria or "none">
Expected load: <if known>
Return its full report.
```

If subagents are unavailable, run both yourself one after the other and say the review was not independent.

## 3. Verify every finding

For each finding from either review that is a bug, risk, spec gap or must/should fix:

1. Open the cited lines. Confirm the code is there and does what the finding claims.
2. Check the concrete case: the input or situation, and the wrong result. If cheap, prove it: run the existing test, a one-off command, or a small failing test.
3. Mark it **confirmed** (you saw it), **likely** (the reasoning holds, but not run) or **dropped** (wrong, already handled, or no concrete case).

Drop style opinions, "consider…", and anything a linter or the type checker already enforces. Merge duplicates and keep the clearer one.

## 4. Report

Use ponytail-review's format: `What this change does:`, then numbered findings under **Must fix / Should fix / Nice to have**, each with location, problem, fix and "if we skip it". Add the source and status to each title:

`2. **Orders land on the wrong day** (billing/close_day.py:40) [ponytail, confirmed]`

End with:

```
Verdict: Ship. | Fix 1, 3 first.
Spec: <covered / gaps: numbers>
Dropped: <count> (<one-line reason each>)
Not checked: <what mattered but could not be checked>
```

This skill lists findings and changes no code.
