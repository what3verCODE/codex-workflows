---
name: factory
description: Run one ticket through real agents in herdr panes next to you (implementer, reviewers, e2e) instead of subagents. You stay the main pane and coordinate. Use when the user says "$factory TICKET-42", "factory", or asks for workers in herdr panes.
---

# Factory

You are the main pane. Workers are full agents (same kind as you) in herdr panes on the right half of your tab. Each starts with an empty context, keeps it across rounds, and the user can watch or talk to any of them. Do not use subagents in this skill.

Drive panes only through `factory.sh` (next to this file). It always targets your own pane, tab and workspace by ID. Do not call `herdr tab create`, `herdr workspace ...` or `herdr pane split` yourself: without explicit IDs they land in whatever workspace the UI has focused.

```sh
F=<this skill's dir>/factory.sh
sh $F up [--tab] ROLE... [-- AGENT-ARGS]  # start workers; --tab puts them in a new tab of this workspace
sh $F ask ROLE "TEXT"                     # send work
sh $F wait ROLE...                        # blocks up to 9 min; call again while any role is still "working"
sh $F read ROLE [LINES]                   # the worker's full reply (its reply file, else the pane's last lines)
sh $F status                              # roles, panes, states
sh $F down                                # close the worker panes
```

`up` fails outside herdr: say so and stop. After `wait`, get each reply with `read`. `ask` has each worker write its full reply to `<factory dir>/<role>.md`, because a pane only gives back about its own height of text; `read` prints that file, or the pane's last lines when there is none.

A worker stuck on a question sends it to your pane as `[role] question` and ends its turn. It may arrive while you are mid-task: answer with `ask ROLE "..."` and carry on. A question you cannot answer from the ticket or code goes to the user.

A worker in state `blocked` is waiting on an approval or a question in its pane (often a permission prompt or an agent update notice). Do not answer it yourself. Tell the user which pane, and keep going with the others.

## Roles

Pick the roles the task needs. Default: `impl ponytail pocock rules`, plus `e2e` when the project has slow visual/e2e tests. Drop `rules` when the project has no rules files (no `AGENTS.md`/`CLAUDE.md`, folder rules or docs/agents).

| Role | Job |
| --- | --- |
| `impl` | Builds the change with `ponytail` and `tdd`. Owns all production code. Fixes review findings later. |
| `ponytail` | Runs `ponytail-review` on the change. Read-only. |
| `pocock` | Runs `code-review` (standards + spec) on the change. Read-only. |
| `rules` | Checks the change against the project's own rules (`AGENTS.md`/`CLAUDE.md`, folder rules, docs/agents). Read-only. |
| `e2e` | Writes and runs visual/e2e tests for the acceptance criteria. Touches only e2e test files. |

## 1. Understand (you)

1. `vcs-bridge`: find the VCS and tracker, record the baseline.
2. Read the ticket. No tracker access: ask the user to paste it.
3. Read the project rules and find the code yourself.
4. Write the brief to `brief.md` in the factory dir (`up` prints it):

```
Goal: <one sentence>
Ticket: <ID/link + acceptance criteria copied in>
Where: <files/symbols to start from>
Baseline: <id>, VCS: <tool>, diff: <command>
Checks: <exact test/lint/build commands>
Not in scope: <...>
```

Open questions that change what gets built: ask the user before step 2.

## 2. Build

Run `up` with the chosen roles. Then, in one turn:

- `ask impl`: "Read <brief>. Implement it with the ponytail and tdd skills. Do not touch e2e test files. Run the checks. Do not commit or checkpoint. Report: changed files, checks run with real output, anything not done."
- `ask e2e` (if up): "Read <brief>. Write visual/e2e tests for the acceptance criteria, touching only e2e test files. Do not run them yet. Report the test files and how to run them."

Reviewers stay idle until there is a change. `wait impl e2e`. `read` both replies, then read the diff yourself. "Done" is not proof.

## 3. Review (max 2 rounds)

Make a local checkpoint (`vcs-bridge`). Then in one turn send each reviewer the common part plus its lane. Reviewers that all chase the same edge case waste the round, so each one stays in its lane.

Common part:

```
Change: baseline <id> → checkpoint <id>, diff: <command>. Brief: <brief path>.
Do not edit tracked files. Scratch scripts go in <factory dir>/<role>/.
A finding counts only with proof: the command you ran (a one-off script, a REPL line,
or a test that fails) and its actual output, next to path:line. Reasoning without a run
is "unproven": list it separately, at most 3.
Rank by harm on inputs the code really gets (its callers, the ticket's examples, real
data), not by how clever the input is. Exotic inputs outside the ticket go last.
Return Must fix and Should fix only. Say "nothing found" if so; do not pad.
```

Lanes:

- `ponytail`: "Run the ponytail-review skill. Try to break the change: read every caller of the changed code and feed the code what those callers really pass. Then boundaries (empty, one, many, huge), wrong types, errors from what it calls, and concurrency or ordering if there is any state."
- `pocock`: "Run the code-review skill. Then check each acceptance criterion in the brief against a run, not the text. Check the tests: for each new test, would it fail on the baseline? Run it there if cheap: copy the baseline version of the file into your scratch dir (never stash or checkout: other panes share this tree). A test that passes on the baseline proves nothing: report it."
- `rules`: "Check the change only against the project's rules: AGENTS.md/CLAUDE.md, rules in the touched folders, docs/agents. Quote the rule for each violation. Logic bugs are other lanes' job."

In the same turn, `ask e2e` "Run your tests against the current tree and report results."

`wait` for all of them and `read` each reply. Verify every finding yourself as the `review` skill describes (open the lines, rerun the proof, mark confirmed / likely / dropped). A finding whose proof you cannot reproduce is dropped. Merge duplicates. Out-of-scope findings (outside the brief's goal and acceptance criteria) go to the report as "not fixed", not to `impl`, unless they break a real caller.

Confirmed must/should findings and e2e failures: `ask impl` with the numbered list, the reviewers' proofs and suggested fixes, and: "Fix the class of problem, not only the cited input: check the similar inputs too (e.g. other quote or whitespace kinds, other callers). Add a failing test first. In your reply, list the similar inputs you checked." `wait impl`, rerun checks, checkpoint. Round 2: ask the reviewers who had findings to recheck only those against the new checkpoint, and `e2e` to rerun. After round 2 stop and report what is still open.

## 4. Report

```
Roles: <list>
Changed: <behavior, 1-3 lines>
Files: <list>
Checks: <command> → <result> (actual output)
E2E: <result | not run>
Review: round N; fixed: <titles>; open: <titles | none>; dropped: <count>
Baseline → checkpoint: <ids>
Panes: still open (sh $F down closes them)
```

Leave the panes open so the user can follow up with any worker. Close them only when the user says so. Publishing (submit, push, PR) only when the user or project rules allow it.
