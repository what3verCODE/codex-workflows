# Skill selection for the portable workflow kit

## Applied user selection

After reviewing the recommendations, the user selected six additions: verify-this, handoff, cli-for-agents, improve-codebase-architecture, make-pr-easy-to-review and why. These are now maintained forks in the manifest, bringing the kit from 19 to 25 skills. Handoff and improve-codebase-architecture were already installed as unmodified extras in both scopes; this change transfers them to kit ownership. The initial proposal below remains as the evaluation record.

The nine user-selected extras were removed locally and globally: claude-handoff, git-guardrails-claude-code, migrate-to-shoehorn, setup-matt-pocock-skills, setup-pre-commit, setup-ts-deep-modules, triage, wait-what and writing-beats. Other global upstream skills were preserved. Their installation differs from this repository's managed kit, so this task updated only the six chosen global skills and did not replace the global agent configuration.

The writer and development-loop now use make-pr-easy-to-review when preparing a PR. It improves descriptions, verification notes and reading order. It can recommend splitting an oversized PR but does not itself implement a stack of smaller PRs. Commit-history rewriting remains optional and explicitly scoped.

Verification passed: seven installer/bootstrap tests, validation of 25 skills and seven roles, all six skill-authoring validators, and Codex 0.154.0 discovery of all 25 managed skills in a disposable installation. Independent source review found and corrected unavailable Skill-tool calls, overbroad investigation scope and organization-specific analytics assumptions. A temporary Git fixture confirmed that why could recover documented historical intent locally with calibrated citations. This is bounded evidence, not a benchmark across real projects.

Installation copies match the maintained skill sources, and all nine selected directories are absent in both scopes. The rollback snapshot for affected installation paths is `/tmp/skill-selection-backup-d6kgxl9f`; it is temporary local storage. The six globally installed skills are available across projects. The PR-writer integration belongs to this managed kit.

## Original evaluation

Reviewed on 2026-09-12. The recommendation follows your clarified scope: frontend and service development, large work projects using several agents, CLI tools such as Decoy, and varied personal projects. The common kit should work across those repositories; project-specific frameworks and commands belong with each project. This is a source-based assessment of practical value, overlap, maintenance burden and runtime fit. Rankings are judgments, not benchmark results.

I recommend keeping the existing 19-skill kit and adding five adapted skills: verify-this, handoff, control-ui, how and control-cli. That would produce a 24-skill kit. Keep cli-for-agents as an optional addition for repositories where CLI design is recurring work. None of the existing entries has a strong evidence-based case for immediate removal. The strongest optional removal is the grill-me convenience wrapper if a smaller command vocabulary matters more than that shortcut.

The initial review produced documentation only. The applied selection above records the subsequent source and installation changes.

Full inventories, including descriptions, pros, cons, dependencies and kit actions:

- [Matt Pocock: all 37 distributable skills](mattpocock-skills-review.md), including beta and specialist entries.
- [Poteto pstack: all 34 skills](poteto-pstack-skills-review.md), including 20 principle skills.
- [Other Poteto plugins: all 35 skill files](poteto-plugin-skills-review.md).

These inventories account for 106 SKILL.md files across the two repositories. Poteto has 67 unique names across 69 files. Its two pr-review-canvas entries implement different outputs; its two thermo-nuclear-code-quality-review entries have identical bodies. Both repositories also contain tdd, so repository and path matter when selecting a skill.

The fetched revisions match the revisions in the current kit's [provenance](../../PROVENANCE.md): [Matt 3cca18b3](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015) and [Poteto 74dd2291](https://github.com/poteto/plugins/tree/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12). Fourteen selected skills originate from Matt, one from Poteto, and four are original kit workflows. There is no source-version update to perform for those pins.

The table ranks new additions by marginal value. The first five form my proposed default change set. The remaining entries depend on recurring work.

| Rank | Skill | Source | Action | What it adds | + | − / adaptation needed | Use it when |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | verify-this | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cursor-team-kit/skills/verify-this/SKILL.md) | ADD adapted | Controlled baseline and changed-state evidence with an explicit verdict. | Makes unsupported completion claims harder. | A valid baseline may be unavailable; preserve existing artifact authorization. | A fix, speedup or installer change needs proof. |
| 2 | handoff | [Matt](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/handoff/SKILL.md) | ADD adapted | A compact document for another session or agent. | References existing artifacts and redacts sensitive material. | Temp files are not durable storage; replace literal Skill-tool directions. | Switching sessions, machines or agents during unfinished work. |
| 3 | control-ui | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cursor-team-kit/skills/control-ui/SKILL.md) | ADD adapted | Browser interaction, screenshots and traces. | Verifies visible behavior beyond tests. | Needs a browser harness and app environment. | Frontend interactions, regressions, accessibility or rendering need evidence. |
| 4 | how | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/pstack/skills/how/SKILL.md) | ADD adapted | An explanation of subsystem flow and ownership. | Better onboarding and grounding before edits. | Overlaps scouts; port Cursor calls and avoid delegation for tiny questions. | Entering an unfamiliar large project or assigning a subsystem to another agent. |
| 5 | control-cli | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cursor-team-kit/skills/control-cli/SKILL.md) | ADD adapted | Repeatable PTY/tmux interaction and profiling. | Tests prompt flows and hangs that unit tests can miss. | Harness setup and cleanup need care; reuse available PTY tools. | Verifying interactive installers, TUIs or terminal behavior. |
| 6 | cli-for-agents | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cli-for-agent/skills/cli-for-agents/SKILL.md) | OPTIONAL, project fit | Non-interactive CLI design, help examples and retry-safe operations. | Directly relevant to scripts and your installer. | Narrow the broad trigger; clarify fail-fast versus interactive fallback. | Building commands other agents or automation will run. |
| 7 | improve-codebase-architecture | [Matt](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/improve-codebase-architecture/SKILL.md) | OPTIONAL, adapted | Surveys maintenance hotspots and presents refactoring candidates. | Reuses your design vocabulary and domain model. | Forced terminology, CDN report dependencies and interview overhead. | Choosing where to spend an architecture/refactoring budget. |
| 8 | why | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/pstack/skills/why/SKILL.md) | OPTIONAL, scaled down | Historical rationale with evidence and uncertainty. | Helps preserve constraints hidden in old decisions. | Searches every available evidence category by default; can be expensive. | Removing legacy behavior or revisiting a surprising design. |
| 9 | loop-on-ci | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cursor-team-kit/skills/loop-on-ci/SKILL.md) | OPTIONAL, adapted | Watches all PR checks and responds to failures. | Handles external checks as well as GitHub Actions. | Needs publication rules and a stop policy; can push or merge main. | CI follow-up consumes repeated manual attention. |
| 10 | make-pr-easy-to-review | [Poteto](https://github.com/poteto/plugins/blob/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12/cursor-team-kit/skills/make-pr-easy-to-review/SKILL.md) | OPTIONAL | Improves review order, descriptions and commit history. | Protects tree identity during history cleanup. | Partly overlaps writer guidance; history rewrites require deliberate scope. | Large changes are correct but hard for a reviewer to follow. |

Retain the current core as grouped below. Groups express their role, not a deletion order. The source of truth is the [manifest](../../manifest.json), not every skill visible in a session or the older skills-lock inventory.

| Existing skills | Recommendation | Why keep them | Main cost |
| --- | --- | --- | --- |
| development-loop, workflow-context, prepared-task, workflow-writing | KEEP | One coherent implementation system with reusable context, readiness and writing contracts. | Delegation and review overhead on substantial work; use direct work for small tasks. |
| tdd, diagnosing-bugs, code-review | KEEP local versions | Tests, reproducible diagnosis and independent review cover different failures. Local forks fit the kit's evidence and authorization rules. | Diagnosis and review should stay proportional to uncertainty and risk. |
| codebase-design, domain-modeling | KEEP | Shared architecture and domain language support worker and planning tasks. | Documentation and abstractions need ongoing pruning. |
| grilling, grill-with-docs, to-spec, to-tickets | KEEP | Separate unresolved decisions, written specification and executable task breakdown. | Avoid repeating questions or publishing artifacts when already settled. |
| research, prototype | KEEP | Answer factual and design uncertainties before implementation. | Research delegation and prototypes cost time; reserve for real uncertainty. |
| writing-for-agents, unslop | KEEP local versions | Maintain readable instructions and documentation. | Style preferences should not become behavioral blockers. |
| wayfinder | KEEP for large efforts | Preserves a map of unresolved decisions across sessions. | High process overhead for a one-ticket change; planning is intentionally limited per session. |
| grill-me | KEEP by default; optional REMOVE | Convenient six-line wrapper around grilling. | No unique underlying capability; direct grilling still works if the wrapper is removed. |

The local forks are intentional. Replacing them wholesale with their upstream names would reintroduce setup requirements, tool assumptions or repeated approval behavior already adapted out. See the per-skill changes in [PROVENANCE.md](../../PROVENANCE.md).

Avoid adding another full execution or review system. Matt's implement and implement-spec overlap with development-loop. Its beta loop-me designs recurring workflow specifications and is a separate optional planning tool, not another implementation runner. Poteto's poteto-mode, figure-it-out, thermos and interrogate overlap with the existing coordinator and reviewers. Orchestrate is a separate Cursor cloud execution architecture. None is a small capability addition. The detailed reports link each source and explain its dependencies.

Also leave out standalone principle-* skills, duplicate CI helpers, generic compiler/smoke check wrappers, Cursor packaging skills, and the placeholder docs-canvas. Useful principle text can become a bounded review checklist or project rule when a recurring defect justifies it. A generic reminder rarely warrants another independently discoverable skill.

For removals, distinguish the managed kit from the wider installed catalog. A global skill visible in this session is not necessarily one of the 19 manifest entries. Removing a manifest entry does not currently delete its previously installed directory, as documented in the [installer README](../../README.md#manage-the-kit). A real removal must update references and deployment behavior as well as the manifest. No global cleanup is justified by this review alone.

Implementation of the proposed additions should preserve the kit's existing packaging contract:

1. Add maintained ports under kit/skills with source revision, upstream metadata, full relevant supporting resources and license.
2. Register them in manifest.json and PROVENANCE.md. Keep managed installation directories as generated output. Skill availability does not mean every skill must run on every task.
3. Preserve explicit invocation where appropriate, make file-based skill references work, and use existing project authorization rather than adding blanket approval gates.
4. Add role requirements only where a role actually needs the skill. A UI harness should not become a prerequisite for every worker task.
5. Run the repository's structural checks and focused installed discovery checks, then exercise each new behavior in a disposable example. Source inspection does not prove that a model will follow the skill reliably.

The [skills CLI](https://github.com/vercel-labs/skills#options) can list and select individual skills, but bulk installation into this repository would bypass the kit's maintained-source and pinning conventions. Use the repositories as sources for selected additions.

For large projects, retain the current specialized agents and one implementation coordinator. The proposed additions serve specific roles: scouts can use how for an evidence-backed subsystem explanation; workers can use control-ui or control-cli for the relevant application; verify-this supplies comparative evidence; handoff records status, unresolved questions, tested revisions and the next action. None needs to introduce another planner/worker hierarchy.

The handoff port should state repository and branch, original baseline, current checkpoint, dirty work, current review round, failed or unavailable checks, and next steps. This matters because the current development-loop keeps baseline and review-count state in conversation context. A fresh session must not silently reset those boundaries. See [development-loop](../../kit/skills/development-loop/SKILL.md).

Frontend and service framework guidance belongs in each project when stacks differ. Even a useful TypeScript convention should defer to a repository's actual types, build system, tests and architecture. Installing all principles globally would impose one author's defaults across unrelated projects.
