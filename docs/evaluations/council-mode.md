# Council-mode validation

Checked on 2026-09-12 with Codex CLI 0.154.0 on WSL.

## Installation and discovery

`make check` passed all seven installer tests and validated 28 skills and eight roles. The skill-creator validator accepted `kit/skills/council-mode`. `make smoke` installed the manifest into an isolated temporary workspace and discovered `council-mode` among all 28 required skills.

The smoke check verifies skill discovery and role-file installation. It does not verify selection of the new named advisor role or a complete council conversation. The current session's available role list predates this addition.

## Independent scenario check

A fresh evaluator read the initial version of the skill and received an open language-choice question without project context or candidate answers. It requested the project purpose, programming experience and decision priorities before launching advisors. It accepted a grilling summary as optional. This version used a smaller roster with task-specific responsibilities; the five-style revision below supersedes that roster.

In a second scenario, both supplied advisor reports assumed ten million daily users even though the project was personal and prioritized learning. The evaluator rejected agreement as sufficient evidence and proposed correcting the shared premise in the second pass. It identified ambiguity in stopping rules that referred only to disagreements. The skill now explicitly permits challenging a shared unsupported premise and includes it in the stopping condition.

## Five-style revision

A second fresh evaluator read the revised skill and advisor role. Its scenario was a personal tool with learning as the main preference, existing Python experience, offline laptop deployment and no candidate list. It assigned all five stable thinking styles without selecting a language or assigning advocates to predefined answers. The Outsider received every factual constraint.

For three available slots with agent release, it planned independent batches of three and two, retained reports before release and withheld earlier conclusions from later advisors. For a host unable to free slots, it reported three completed perspectives and named the two missing ones as an incomplete council. It preserved the fresh-context fallback for follow-up and checked unanimous recommendations for unsupported assumptions rather than manufacturing dissent.

`make check`, skill validation and whitespace checks passed after the revision. Installation structure and manifest entries were unchanged from the earlier discovery smoke check.

These were bounded simulations of coordinator decisions, not end-to-end council runs. Actual advisor research, follow-up delivery, fresh-context fallback and degraded execution remain unverified behavior. A future runtime trial should exercise an evidence-backed early agreement, a material dispute requiring follow-up, and failure to obtain the full five-advisor roster.
