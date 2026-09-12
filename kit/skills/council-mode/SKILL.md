---
name: council-mode
description: Convene independent advisors to explore an open question or compare options when the user asks for council mode or an advisor debate.
---

Run a standalone consultation on one decision. Accept an open question without candidate answers, a preferred option, a ticket or a prior grilling session. The main agent coordinates and returns a decision brief; advisors investigate read-only. Council does not start implementation, publish decisions or count as a code-review round.

## Establish the brief

Use the question, supplied context and relevant project evidence to establish the objective, constraints, preferences and unknowns. In a separate session, ask for missing context rather than assuming access to another conversation. A grilling handoff is optional input, not a prerequisite.

Ask only questions whose answers could materially change the recommendation and cannot be resolved from available evidence. Pause dependent advice for essential answers; where useful, present conditional alternatives with explicit assumptions. Never require the user to supply candidate solutions. Distinguish hard constraints from preferences and advisor assumptions.

Prepare a shared factual brief with the question, scope, evidence references, decision criteria and remaining unknowns. Preserve user preferences as evidence, but withhold the coordinator's preferred answer and other advisors' conclusions from the first pass.

## Convene advisors

Launch five independent instances of the installed `advisor` role, one for each thinking style below. Give each fresh context, the same factual brief and its assigned style from this table. Use these stable names and keep each instance's identifier and report for follow-up. Tell the user the roster and pass cap before launch.

| Advisor | Thinking style |
| --- | --- |
| Contrarian | Test the framing and candidate options for weak assumptions, hidden costs and plausible failure modes. Acknowledge options that survive scrutiny. |
| First-principles thinker | Derive options from the objective, hard constraints and underlying mechanisms. Check whether conventional requirements are actually necessary. |
| Expansionist | Explore overlooked alternatives and upside, including approaches outside the initial framing. Explain the conditions and costs needed to realize that upside. |
| Outsider | Question unexplained conventions, jargon and assumptions from a newcomer's perspective. Use the full factual brief, including all essential constraints. |
| Executor | Compare practical effort, dependencies, learning demands and reversibility. Identify a feasible first step or experiment for the strongest options. |

Each advisor may discover and compare any viable options. Apply the thinking style to the question without assigning an answer to defend or inventing objections to perform a personality. All five may agree when evidence warrants it. The coordinator synthesizes their reasoning and is not a sixth independent advisor.

Use the host's available agent tools and concurrency slots, running independent assessments in batches when necessary. Preserve first-pass independence across batches by withholding earlier reports. Retain reports before releasing completed agents if the host supports releasing slots; use the fresh-context follow-up fallback below when needed. If the host cannot accommodate the full roster, report the missing perspectives instead of waiting indefinitely or substituting the parent's own role-play.

Advisors read relevant source and authoritative references themselves; verify changing technical claims against current primary sources. Distinguish evidence from inference and record inaccessible evidence. Multiple instances, styles or models do not by themselves prove diverse or correct reasoning.

If named roles are unavailable, read the installed `advisor.toml` under workspace `.codex/agents` or global `$CODEX_HOME/agents` (default `~/.codex/agents`) and pass its instructions and assigned thinking style to a fresh child. Forward configured model/reasoning overrides only when supported. Disclose that this fallback inherits the parent's environment and cannot apply role-level sandbox or skill settings; retain the read-only task boundary. If fewer than five independent advisors complete, label the council incomplete and name the missing perspectives. If fewer than two complete, return a limited consultation and label it degraded. Do not present the parent's own perspectives as independent agents.

## Assess and challenge

1. Request independent reports: viable options, recommendation and rationale, supporting references, assumptions, strongest counterargument, uncertainty and evidence that would change the recommendation. Keep each report focused on the decision, normally under 600 words. Advisors return questions to the coordinator and do not contact the user or one another.
2. Compare the reports in the parent. Separate agreements, factual disputes, differing preferences and missing evidence. Tell the user which material disagreements remain. Agreement alone is not proof; check whether recommendations rest on the same unsupported assumption.
3. When evidence could resolve a disagreement or a shared unsupported premise affecting the recommendation, send the relevant advisors a curated challenge packet with the disputed claim or premise, counterevidence or competing reasoning, and a concrete question. Relay at most five material claims per advisor rather than entire peer transcripts. Ask for a revised or defended conclusion with reasons. Use follow-up on the retained advisor when possible; otherwise launch a fresh instance with its earlier report and challenge packet and disclose the context reset.
4. Stop after independent assessment if no material evidence-resolvable disagreement or unsupported premise remains, or after one cross-examination. A third pass is allowed only when the user requests it and a specific remaining dispute or premise can be settled with evidence. Respect user interruption and report failed advisors without an endless replacement loop. Pass caps are behavioral instructions, not runtime guarantees.

Preference tradeoffs belong to the user. Preserve unresolved dissent when evidence is insufficient; do not force consensus or settle correctness by vote. Suggest a small experiment when it would discriminate between options, without running implementation work as part of the consultation.

## Return the decision brief

Make the answer self-contained so it can be pasted into another session. Include:

- The question, relevant facts, constraints and explicit assumptions.
- A recommendation, or conditional recommendations when essential uncertainty remains, with reasons and credible alternatives.
- Material feedback accepted or rejected and why; remaining disagreements and owner decisions.
- Supporting references, confidence and what evidence or experiment would change the recommendation.
- Advisor names and thinking styles, actual passes, missing perspectives, context resets, unavailable evidence and execution limitations.

Keep agent identifiers alongside the execution record when available; they are session references, not a promise of cross-session resumability. Return the brief in the conversation unless the user requests a file. The user can bring it back to grilling or another planning session without adopting the recommendation automatically.
