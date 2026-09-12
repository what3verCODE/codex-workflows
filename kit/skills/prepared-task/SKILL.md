---
name: prepared-task
description: Assess a resolved task and implement code through TDD, project verification and a VCS checkpoint, using oracle and worker roles.
---

Read `../workflow-context/SKILL.md` and resolve task evidence, project instructions, existing edits, task context and original baselines before changing behavior.

Oracle reads the task, comments, source and agreed testing decisions. Return the proposed approach, acceptance criteria mapped to observable behavior, relevant regression boundaries and meaningful unresolved questions. Ready work proceeds without routine approval. Existing test decisions satisfy seam agreement. Missing understanding pauses dependent implementation; do not invent defaults that change the requested behavior.

Worker reads `../tdd/SKILL.md` and its applicable references. Implement one behavior slice at a time through an observed failing test, minimal change and passing test. Run the actual project's appropriate checks. Report command outcomes and distinguish a failure in the changed behavior from missing tools or unrelated baseline failures. Normal test/fix cycles do not consume review rounds. Preserve unrelated work and avoid fixed retry counts.

If relevant existing edits already implement a slice, preserve them and add missing coverage. Use an isolated original baseline to demonstrate the regression's red result when feasible, as described in TDD. Report unavailable red evidence rather than altering user work to create it.

Send documentation-only tasks to writer instead of worker; code tests and new test infrastructure are unnecessary for prose changes. After behavior changes, have writer update affected documentation and memory banks using current code evidence. Then create a checkpoint of completed task changes with the configured VCS and checkpoint conventions. A local checkpoint must not become an unauthorized shared submit. Confirm its contents and return per-repository checkpoint identifiers and original baselines. If checks or checkpoint creation are unavailable, report the limitation rather than claiming completion. Publication follows existing user/workspace instructions.
