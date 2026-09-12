---
name: why
description: Investigate why existing code or a design decision exists using history, PRs, tickets and other available evidence. Separate documented intent, inference, contradictions and unknowns before changing legacy behavior.
---

# Why

Recover the reasons behind a specific piece of code or design choice. Code establishes what happens; author intent needs historical evidence. Treat the user's proposed explanation as a hypothesis. This investigation returns findings and constraints, without editing the implementation or contacting people.

Read [references/epistemics.md](references/epistemics.md) for confidence tiers and calibrated wording. Keep those distinctions in the final answer.

## Anchor the question

Resolve the target from the request and current task. Locate the relevant repository, files, symbols and behavior. Clarify only when different plausible targets would change the investigation.

Start with the local historical record, using the repository's VCS. Useful native operations include line attribution, file history through renames, and inspecting the introducing revision or change record and its linked reviews. Read diffs and discussion around the original decision, not only the latest touch. Record the code anchor and seed links before delegation so investigators can reuse them.

If history is shallow, absent or inaccessible, state that limitation. Version history, a review host and a searchable tracker are not guaranteed. Use the available VCS and source tools instead of treating a missing tool as evidence that no rationale exists.

## Follow the evidence

Start with source history, nearby tests/comments, linked PR discussion, decision records and tickets. Follow concrete leads and unresolved hypotheses to additional available sources. For broad investigations, map the relevant evidence categories:

- Source history and code archaeology.
- Issues and work tracking.
- Design documents and decision records.
- Team discussion.
- Infrastructure logs and incident records.
- Exception tracking.
- Product analytics and experiments.

Inspect available tool metadata to discover access. An example vendor in a reference is not a required integration. Record sources searched, unavailable sources that limit the answer, and relevant searches that returned no result. An empty search does not prove no decision was recorded.

Use [references/source-playbook.md](references/source-playbook.md) to choose a category reference. Adapt its example queries to the actual tools, schema and target. Read only the categories being investigated. For defensive code, also consult [references/sources/incident-postmortem.md](references/sources/incident-postmortem.md) when incident evidence may explain the behavior.

Answer locally when the introducing PR or decision record directly resolves the question and plausible contradictory evidence has been checked. For independent searches across sources, delegate bounded assignments to available scouts with the code anchor, question, source tools and [references/investigator-prompt.md](references/investigator-prompt.md). Use the current role and model configuration. One investigator owns each independent source assignment; a different provider's model is not required. Preserve read-only behavior through the tools actually available.

Stop when the question is answered with calibrated evidence, or when relevant accessible leads are exhausted. Report residual uncertainty. A broad audit can justify more searches; an ordinary question does not require exhausting every integration. Respect task-specific time and cost limits. No source search authorizes messages, comments, tickets, or other external writes.

## Synthesize and return

Read the evidence yourself. For a large or contradictory record, an independent synthesizer may use [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Check important citations against their original sources. A parent remains responsible for factual scope and must retain uncertainty when editing an investigator's answer.

Scale the output to the question while preserving:

- The target and question.
- Documented reasons with direct citations.
- Supported interpretations and the inference connecting their evidence.
- Contradictions or competing explanations when present.
- Unanswered questions and the source-access or search gaps behind them.
- Sources actually consulted and a clear confidence assessment.

Distinguish explicit rationale from observations that merely fit it. Absence of evidence is an acceptable result. Do not fill gaps with a convincing story or impose invented gaps when the record answers the question.

When the investigation informs a planned change, finish with constraints to preserve, changes the record supports, approaches to avoid, and unresolved risks. Findings inform the current task; they do not start an implementation or redesign automatically.
