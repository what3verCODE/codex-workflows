# Preparation, writing and diagnosis evaluation

All work used disposable fixtures under `/tmp/workflow-eval-20260912`. No source files in the real repository were changed. Instructions were read from `kit/skills` and `kit/agents`. Unslop and codebase-design were initially read from the workspace installed skills. The supplied dependency path `/tmp/workflow installed kit/.agents/skills` was clarified after two incorrect path attempts. No setup files were introduced.

## Documentation

Read `documentation/AGENTS.md`, `ticket.md`, `app.py`, `memory.md`, `Makefile` and the workflow-writing, writing-for-agents and unslop instructions. Updated only `documentation/memory.md`, retaining its original sentence and adding the requested examples `total([2, 3])` returns `5` and `total([])` returns `0`, with `app.py` as the source. Source returns `sum(values)`. No code tests or testing infrastructure were used. `git diff --check` passed. Independent agent `/root/evaluate_workflow` read the task, instructions, source, memory and diff against baseline `1db8986`, and returned no factual or prose findings. It confirmed both examples and the source attribution, with no code tests or edits. This was independent draft-state review, not a final checkpoint review. No publication or checkpoint is claimed.

## Prepared bug

Read the supplied investigation and reused its established cause. No fresh diagnosis phase was performed. Recorded original `main` baseline `ecb6ec2183f3333b50c7cdda5f610cccc5184f07`; original status was clean except untracked `ticket.md`. Created branch `task/BUG-1` using `git switch -c task/BUG-1`.

Worker instructions and TDD references were read. Added one regression through the existing unittest interface, `Totals.test_empty_total_is_zero`. Ran `python3 -m unittest -v` before application changes. Result was one failure and one pass, with `AssertionError: None != 0`. Changed `app.py` from `sum(values) if values else None` to `sum(values)`. Ran `make test`; both tests passed. `git diff --check` passed. Updated memory with the empty-input result and source/test references. Changes are limited to `app.py`, `test_app.py` and `memory.md`. Worker handoff is ready for the coordinator checkpoint; no checkpoint was created by this worker because worker instructions assign that action to the coordinator.

## Uncertain bug, diagnosis only

Executed in `uncertain-bug`:

```sh
python3 -c 'from app import total; actual = total([]); print("total([]) =", repr(actual)); assert actual == 0, repr(actual)'
```

Exit 1, `total([]) = None`, `AssertionError: None`. Empty input is already the smallest basket. Ranked hypotheses were an explicit empty conditional, a summation primitive returning None, and a different imported module. Then executed:

```sh
python3 -c 'import app; print("module:", app.__file__); print("sum([]):", sum([])); print("total([0]):", app.total([0])); print("total([]):", app.total([])); assert app.total([]) == 0'
```

The loaded module was the expected fixture, built-in `sum([])` and `total([0])` returned zero, and `total([])` still returned None. The conditional at `uncertain-bug/app.py:2` selects None for the empty list. This is the established cause. Implementation handoff is a regression at the existing total/unittest interface expecting literal zero, then removal of the conditional. No application edits or checkpoint were made. Python created `__pycache__`; it remains a reported disposable runtime artifact. No instrumentation was added.

Evaluator deviation: the initial bundled fixture read exposed application source before the first red-capable command. The later reproducer and predictions were actually run, but this was not a clean blind diagnosis test. Also, the distinguishing probe printed several observations in one command rather than separate one-variable probes. These are evaluation limitations, not skill failures.

## Tracker operations, explicitly a local stub

Available tool metadata was searched for MCP/search capabilities. No tracker MCP or general tool-search callable was exposed. This establishes only unavailable tracker access in this runtime; it does not establish anything about live issue state. No live tracker operation was attempted.

Created `/tmp/workflow-tracker-stub.py`, a temporary JSON CLI with read, conditional update, create and blocking operations. The requested tracker state is `/tmp/workflow-eval-20260912/tracker.json`. It stores every call under `stub_calls`, including read results and expected full content for update. This stub is an evaluation fixture, not a workflow setup file.

The observed call sequence was `read 17`, `read 17`, `update 17`, `create 18`, `read 17`, `create 19`, `create 20`, `block 20 by 19`. Immediately before updating, the full issue was reread; the update compared its full expected content. Replaced only `Old spec.` within Specification. Actual preservation assertions passed for the complete Operations prefix, comments and customer label. No ready-for-agent label was added because none was exposed as available. Issue 18 represents the separate explicit new-issue request. Issue 17 was unchanged during the subsequent two-ticket publication.

The spec states agreed behavior: ignore negatives, zero for empty input, use the existing unittest interface. The approved two-slice plan was represented by issue 19, negative filtering through the public total function with tests, followed by issue 20, zero after empty/filtering with tests. Issue 20 has both textual and stub-native blocking links to 19. This fixture has no API/UI layers. The claimed native relationship exists only in the JSON stub; no platform integration has been verified.

Ambiguous destination exercise emitted the focused question `Which tracker and project should receive this spec?` and compared the tracker SHA-256 before/after that branch. The hashes matched. This was a simulated user interaction printed by the test driver, not a real pending user question. The later resolved stub case proceeded separately.

## Bounded scout

Read `discovery/AGENTS.md`, which maps Billing to `services/billing`. Read package instruction `discovery/services/billing/AGENTS.md:1`, requiring `rules.md`, then `rules.md:1`, which says amounts are integer cents. Bounded `rg -n 'invoice_total|cents|rules' discovery/services/billing` found `invoice.py:1` defining `invoice_total(items)` and line 2 summing each item's `cents`. Relevant relationship is the billing total consuming item cents under the integer-cents rule. No searches traversed the archive. No source edits were made. Suggested next read for a concrete billing change is the caller/test location, which was not established within this assigned region. No MCP references were fabricated.

## Independent review fixture observation

At the coordinator's request, independently read the review fixture without mutation. `review/app.py:2` returns `sum(value for value in values if value > 0) or None`. `review/memory.md:1` promises zero for an empty list, and the ticket requires source and memory to agree. Empty and zero-only inputs instead yield None. Reported this concrete source/documentation mismatch to the coordinator. This was inspection, not an executed test or full code-review specialist round.

## Additional independent checkpoint review

At `/root/evaluate_workflow` request, read the review-specialist role and code-review skill, then reviewed specification, correctness, test quality and documentation for the four fixed comparisons in `/tmp/workflow-code-checkpoints.json`. These were prepared `1db8986..0849c3d`, existing-edits `1db8986..f666564`, multi/service `1db8986..a3145f6`, and multi/client `bd3e20a..fec910f`. Read all task bodies, package instructions, multi ancestor instructions, implementation, tests, memory, Makefiles and complete original-baseline diffs. This included the pre-existing task code change in existing-edits.

No findings or blockers in the assigned categories. The `>= 0` filter matches the requested behavior. Literal interface tests cover mixed values, all-negative input, empty input and existing positive totals. Memory matches implementation. Git HEAD and status were checked before and after review, and working implementation/tests/memory matched fixed checkpoints afterward. No fixture mutations or redundant test runs. Dependencies were the standard library `sum` and unittest, with no unread project dependency. TMS and visual tools were unavailable; no UI exists here. This was independent review in an existing evaluator context, not a fresh specialist context. Other categories remained the coordinating reviewer's responsibility.

## Instruction issues and limits

- `to-spec` requires a LONG and extremely extensive list of stories even for this two-behavior fixture. Following that literally would invent or duplicate scope. The artifact uses only two grounded stories. This is a template proportionality issue; publication and preservation behavior worked.
- The diagnosing skill's demand that removing every remaining element makes the reproducer green is awkward for an already empty input. The empty basket cannot be reduced further. No artificial input was introduced to satisfy that wording.
- Stub calls demonstrate executable read/update/create/preservation/link behavior, not real MCP permission handling or a live platform relationship.
- Role instructions were executed in this evaluator context. Independent writer review passed in another existing agent context. Coordinator checkpoints were not completed. No success claim includes those missing steps.
