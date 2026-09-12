---
name: workflow-writing
description: Update project documentation and memory banks from task and code evidence, or draft requested prose for independent factual and prose review.
---

Read the target project's applicable instructions, documentation conventions and existing memory-bank files. Use task decisions, changed code and observed verification to identify which documents need updates. Preserve unrelated content. Record unknowns as unknowns; do not infer supported behavior from a plan or an unrun test.

Read the installed `../unslop/SKILL.md` when drafting or editing documentation and memory-bank files. It is not required for conversational answers, status updates or agent reports. For agent-facing files, also read `../writing-for-agents/SKILL.md` and applicable references. Use project terminology and cite source paths or references where they support factual claims.

Documentation-only work needs factual, consistency, local-rule and prose review in independent context, without code tests or new testing infrastructure. Use existing documentation checks if available. Drafted tickets and comments remain drafts unless publication was requested. An implementation correction may invalidate earlier documentation; reread changed code and update affected docs before the next checkpoint and review.

When preparing or updating a code review request, read `../make-pr-easy-to-review/SKILL.md`. Match the description and reading guidance to the final diff, use the project template, and report actual verification. Use the project's review host and keep small change descriptions short. Existing publication authorization applies; history rewriting remains optional and separately scoped.

Return changed documents, evidence supporting behavioral claims, checks performed and unresolved factual questions. The independent reviewer receives the task, source state and documentation without the writer's conclusions as a substitute for inspection.
