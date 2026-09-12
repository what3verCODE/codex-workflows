# Code workflow forward test

Scope: disposable PREP-1, EDIT-1, MULTI-1 fixtures and read-only ASK-1 clarification inspection. Live trackers and publication were excluded by evaluator instruction. Named custom-role selection is unavailable; child tasks read installed TOML instructions as the documented fallback. This evaluates behavior, not runtime or token guarantees.

## Initial inspection

Read development-loop and installed workflow-context, prepared-task, TDD including tests.md and mocking.md, workflow-writing, code-review including smells.md, role TOMLs, and applicable fixture AGENTS.md files. All four affected repositories initially passed `make test`, one unittest each. No staged changes existed. `prepared/ticket.md` and `existing-edits/ticket.md` were untracked fixture inputs. EDIT-1 had the complete relevant app.py implementation already unstaged and unrelated untracked notes.txt. Its SHA-256 was eb3d19da310bb99fbe585fc2d70bb17934d362343e3aa41c5f8d28a31f1e6382.

Reused task/EDIT-1. Created task/PREP-1 from configured main and task/MULTI-1 from configured main in both service and client. No task worktrees were created. Original baselines remain those supplied in baselines.json, not new checkpoint tips.

## Clarification

ASK-1 asks for correct discounts without defining their meaning. Blocking question: What do discounts mean for total: how are they represented, and how should they change the result, including when the discount exceeds the subtotal? No dependent edits, branch operations or tests were performed in clarification.

## Instruction friction under evaluation

`kit/skills/prepared-task/SKILL.md:10` mandates observed failing test and minimal change for each behavior slice; `kit/skills/tdd/SKILL.md:34-35` similarly require red before green. EDIT-1 already has the correct behavior as user work, so an honest regression test passes immediately. The text does not distinguish completing coverage for existing implementation from implementing new behavior. Safest fallback is preserving source and checking test sensitivity against the original baseline in a temporary directory, explicitly reporting that this is retrospective regression evidence rather than a new implementation red-green cycle.

## Implementation and documentation

Oracle assessed each ticket separately as ready without routine approval. Named-role tool unavailable, so a bounded child loaded installed oracle TOML instructions. Creating a second child returned `agent thread limit reached` even after oracle finished. The same child then loaded worker and writer instructions sequentially. These are role changes, not independent contexts.

PREP-1 and each MULTI-1 repository added a public total regression before code. `make test` failed with exit 2 and `AssertionError: 1 != 3`, with the original positive test still passing. Minimal negative filtering then passed both tests. All-negative and empty coverage brought each final suite to 4 passing tests. EDIT-1 retained its existing app.py without rewriting it, added regression tests, and tested original baseline source in `/tmp/edit-1-historical-r89dih6c`. Historical unittest exited 1 with failures `1 != 3` and `-5 != 0`; current `make test` passed 4. Added boundary tests already passed the implementation; they are regression coverage, not further red-green cycles. Full observed evidence is `/tmp/workflow-worker-evidence.md`.

Writer read current code and tests and updated all four memory.md files to describe zero/positive inclusion, negative exclusion and zero for empty/all-negative input. No tests were invented for prose changes. Coordinator ran `git diff --check`, staged exactly app.py, test_app.py and memory.md, inspected staged names, created commits, and inspected commit stats and working states. Notes hash remained identical. Untracked tickets, notes and generated __pycache__ stayed outside checkpoints.

## Fixed comparison table

| Repository | Original baseline | Checkpoint | Branch |
| --- | --- | --- | --- |
| /tmp/workflow-eval-20260912/prepared | 1db8986b10c958a9feb111c66d731131f568dd75 | 0849c3d01ea2f1f3f6ebe2bea77ee6d0babfccfd | task/PREP-1 |
| /tmp/workflow-eval-20260912/existing-edits | 1db8986b10c958a9feb111c66d731131f568dd75 | f6665642045695001c36a87c42fa1add81f9d888 | task/EDIT-1 |
| /tmp/workflow-eval-20260912/multi/service | 1db8986b10c958a9feb111c66d731131f568dd75 | a3145f614e3a6f35e44abfe0439335d0c30eeaae | task/MULTI-1 |
| /tmp/workflow-eval-20260912/multi/client | bd3e20a59f382fa477e9c5e3c6145980ddb17019 | fec910fd99618bcb350239e9cae9cd80d884fee3 | task/MULTI-1 |

## Review execution

Round one was requested against the complete original ranges, including EDIT-1's pre-existing implementation. Due the thread limit, separate already-running evaluators were assigned bounded read-only specialist categories rather than fresh dedicated reviewer children. This is an independence/context limitation of this evaluation, not a full demonstration of installed reviewer dispatch. Specification/correctness/test quality/documentation went to evaluate_preparation, which had not implemented these fixture tickets. Standards and remaining technical categories were requested from the parent evaluator, which also had not implemented these fixtures. Specification, correctness, test quality and documentation specialist returned no findings or blockers. It read every task, applicable rules, full diff, app/test/memory and Makefile. Source and HEAD/status matched before and after. Literal public-interface tests cover required behavior. No project dependencies were left unread; dependencies are Python built-ins/unittest. Standards and remaining categories are pending parent review.

## Outcome and limits

Implementation, documentation, available project checks and local checkpoints completed for PREP-1, EDIT-1 and MULTI-1. Independent review of specification, correctness, test quality and documentation found no blocking issues. No corrections or second review round were triggered. Coordinator rechecked all checkpoint HEADs and task-file contents after the specialist returned; they remained fixed.

At this report handoff, independent standards, architecture/maintainability, runtime, security, accessibility, type-safety and reuse analysis remains pending with the parent evaluator. Therefore this report does not claim a completed full-category review round. Parent may append actual results. There is no UI in these fixtures, so manual UI validation is inapplicable; visual tooling and TMS access were not exercised. Live tracker access and publication were deliberately excluded. Multi-repository checkpointing was demonstrated, but not atomic cross-repository rollback or any non-Git workflow. No runtime/token guarantee was tested.

The main actionable instruction gap is existing correct user implementation versus mandatory chronological red-green wording, identified above. Historical-baseline test sensitivity was a documented evaluator judgment; the skill currently does not specify that fallback.

## Completed round one

Parent independently reviewed the remaining categories against all four original-baseline ranges and checked checkpoint HEAD/status. Standards, architecture/maintainability, runtime, security, type safety and reuse returned no findings. Accessibility is inapplicable because there is no UI. The generator and built-in sum fit this small numeric boundary; no added dependency is warranted. No external input/authentication/resource behavior changed. Relevant project code was fully read; standard-library internals were not needed. Together with the separate specification/correctness/test-quality/documentation analysis, this completes one review round with no blocking findings. No corrections or second round were needed. The existing-context and thread-limit limitations above still apply.
