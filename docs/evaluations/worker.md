# Worker and writer evidence

Read oracle, worker, and writer role instructions and their required skills. This agent handled oracle, then worker, then writer sequentially at coordinator request because a thread-limit failure prevented another role dispatch. These were sequential role changes, not independent agent contexts.

## PREP-1

In `/tmp/workflow-eval-20260912/prepared`, added only the mixed negative regression first. `make test` exited 2: 2 tests ran, existing positive test passed, new test failed with `AssertionError: 1 != 3`. Changed app.py to sum values >= 0. `make test` exited 0 with 2 passing tests. Added all-negative and empty-input coverage; `make test` exited 0 with 4 passing tests.

## MULTI-1

Applied the same sequence separately in `/tmp/workflow-eval-20260912/multi/service` and `/tmp/workflow-eval-20260912/multi/client`. Each first `make test` exited 2 with `AssertionError: 1 != 3`, while the existing positive test passed. After minimal filtering implementation each `make test` exited 0 with 2 passing tests. After adding all-negative and empty-input coverage each final `make test` exited 0 with 4 passing tests.

## EDIT-1

Preserved the existing app.py implementation without writing it. Added mixed-negative, all-negative, and empty-input tests. Extracted original app.py using `git show 1db8986b10c958a9feb111c66d731131f568dd75:app.py` and copied new tests into `/tmp/edit-1-historical-r89dih6c`. In that temporary directory, `python3 -m unittest -v` exited 1: mixed-negative failed with `1 != 3`, all-negative failed with `-5 != 0`, positive and empty tests passed. This establishes historical regression sensitivity; it is not newly implemented TDD. Current repository `make test` exited 0 with 4 passing tests. notes.txt remains exactly `Unrelated personal draft, preserve exactly.` followed by newline.

## Documentation

Updated memory.md in all four affected repositories after inspecting current app.py and test_app.py. Each now records that total adds zero and positive values, ignores negative values, and returns 0 for empty or all-negative input. Claims match source and observed tests. No extra tests were run for these prose-only edits. No unresolved factual questions. No commits or publication performed.
