# Skill sources

`skills-lock.json` records the separately installed skill inventory. The nine user-selected retired extras were removed from that inventory on 2026-09-12. All managed skill definitions are now owned and updated by the manifest, so their old skills CLI update records were removed too; unrelated extras remain in that inventory. Its `computedHash` values are content identifiers, not commit pins. `manifest.json` selects the kit requirements, records resolved revisions, and pins every downloaded file with SHA-256. The installer does not modify that lock file or install every skill it lists.

Matt Pocock sources use [mattpocock/skills at 3cca18b368ae95cdbdebbff572ccafa662551015](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015). The source was fetched and inspected on 2026-09-12. Paths below are relative to that repository.

| Skill | Original path | Distribution and changes |
| --- | --- | --- |
| grilling | skills/productivity/grilling | Unmodified upstream download. Keeps design-tree questioning and explicit preparation decisions. |
| grill-me | skills/productivity/grill-me | Local fork. Replaces the Skill tool call with loading the shared grilling file. |
| grill-with-docs | skills/engineering/grill-with-docs | Local fork. Replaces Skill tool calls with loading the grilling and domain-modeling files. |
| wayfinder | skills/engineering/wayfinder | Local fork. Adds file-based skill loading when the Skill tool is unavailable and replaces mandatory setup with tracker resolution and a local Markdown fallback. Keeps the upstream map, ticket types, planning default and session limits. |
| domain-modeling | skills/engineering/domain-modeling | Unmodified upstream download with glossary and ADR formats. |
| research | skills/engineering/research | Unmodified upstream download. |
| prototype | skills/engineering/prototype | Local fork with logic and UI references. Preserves prototypes in native isolated changes or local artifacts, without requiring a branch or main; production integration and publication follow task authorization. |
| codebase-design | skills/engineering/codebase-design | Unmodified upstream download with its references. |
| tdd | skills/engineering/tdd | Local fork. Keeps behavioral boundaries, vertical red/green slices and test/mocking references. Accepts previously agreed boundaries, uses file-based skill loading, and yields to project terminology. |
| diagnosing-bugs | skills/engineering/diagnosing-bugs | Local fork. Adds an assignment-boundary paragraph for evidence reuse and diagnosis-only handoff, and replaces the Git-specific bisection command. Original phases, reproduction criteria and fix guidance remain intact. |
| code-review | skills/engineering/code-review | Local fork. Keeps independent standards/spec traceability and all twelve smell judgments in smells.md. Adds fixed multi-repository state, technical specialists, evidence/severity rules and duplicate aggregation. Removes setup and Git-only comparison requirements. |
| to-spec | skills/engineering/to-spec | Local fork. Keeps synthesis, extensive user stories, implementation/testing decisions and scope template. Resolves tools without setup, distinguishes existing-ticket updates from new issues, preserves unrelated content, and reuses agreed testing decisions. |
| to-tickets | skills/engineering/to-tickets | Local fork. Keeps tracer bullets, expand-contract planning, blocking edges and approved breakdowns. Resolves the tracker from intent/context, supports native relationships and partial publication reporting, and removes mandatory setup. |
| writing-for-agents | skills/productivity/writing-for-agents | Local fork. Keeps context pointers, hierarchy and pruning. Adapts invocation metadata to Codex and preserves normal discovery by default. |
| resolving-merge-conflicts | skills/engineering/resolving-merge-conflicts | Local fork. Uses native conflict state and source intent, task-scoped resolution, meaningful clarification and verification. Removes forced completion, stage-all and Git-only commands; shared submit remains publication. |
| implement-spec | skills/in-progress/implement-spec | Local fork of an upstream beta skill. Preserves explicit invocation and dependency-graph delivery. Reuses current roles and native integration contexts, offers sequential fallback, verifies integrated predecessors and reviews the whole change in at most two rounds. |
| handoff | skills/productivity/handoff | Local fork. Preserves explicit invocation and artifact references; removes the unsupported argument-hint field. Adds repository, baseline, checkpoint, dirty-work, verification and review-round continuity; uses file-based skill loading and unique temporary output. |
| improve-codebase-architecture | skills/engineering/improve-codebase-architecture | Local fork. Preserves candidate survey, decision records, supporting report examples and explicit invocation. Uses available scouts, project terminology, file-based skill loading, Mermaid 12 CDN reports with explicit classic layout settings, optional offline output and file links. The report reference preserves project vocabulary. |

The prose-cleanup skill is a local fork from [poteto/plugins at 74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12](https://github.com/poteto/plugins/tree/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12), original path `pstack/skills/unslop`. Its license comes from `pstack/LICENSE`. Only the discovery description changes: apply it to documentation writing, not conversational answers, scout findings or routine reports. The cleanup rules remain unchanged, and reviewer no longer requires it unconditionally.

Additional Poteto forks use the same `74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12` revision. Paths are relative to poteto/plugins.

| Skill | Original path | Maintained changes |
| --- | --- | --- |
| verify-this | cursor-team-kit/skills/verify-this | Keeps comparative claims, controlled measurements and three verdicts. Reuses valid task evidence, preserves the working tree, accepts prior artifact authorization and uses available project harnesses. |
| cli-for-agents | cli-for-agent/skills/cli-for-agents | Keeps flags, help, pipelines, idempotency and dry-run guidance. Narrows invocation to CLI design/review and distinguishes unattended failure from human interactive mode. |
| make-pr-easy-to-review | cursor-team-kit/skills/make-pr-easy-to-review | Applies to normal PR preparation through writer and development-loop. Supports pre-PR drafts, project templates, current verification and short descriptions for small diffs; preserves publication scope and optional history cleanup. |
| why | pstack/skills/why | Keeps confidence tiers and all source playbooks. Replaces Cursor/model assumptions with available roles/tools, follows relevant evidence rather than every integration, allows local synthesis, and retains normal automatic discovery. |

Each Poteto fork includes its plugin's license. The nine retired extras are `claude-handoff`, `git-guardrails-claude-code`, `migrate-to-shoehorn`, `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `triage`, `wait-what` and `writing-beats`. They were outside the managed manifest; their removal does not remove framework features, Git hooks already installed in other projects, or project configuration previously generated by those skills.

Each local fork has `upstream.json` with repository, path, revision and the previous installed hash when previously installed. Matt's license is included in each fork. Downloaded skills include their upstream license. Upstream agent UI metadata is preserved, including explicit-invocation policy for to-spec, to-tickets, grill-me, grill-with-docs and wayfinder. Unsupported `disable-model-invocation` frontmatter is removed from those forks; the equivalent existing Codex `agents/openai.yaml` policy remains.

`workflow-context`, `prepared-task`, `workflow-writing`, `development-loop`, the TOML roles, installer and evaluation tooling are original kit material derived from this project's specification.

To update a fork, compare its recorded revision with the desired upstream revision, retain relevant changes, and revise its `upstream.json`, manifest entry and this table together. To update a downloaded skill, change its immutable revision and all file hashes together. Never replace a commit with `main` or interpret a successful TOML parse as runtime compatibility evidence.

## VCS-neutral workflow adaptations

The managed skills use the target project's VCS and review host rather than Git/GitHub defaults. Workflow-context now resolves native task/change identifiers and pending work, treats shared submits as publication, and supports local snapshots when no VCS exists. Prepared-task, development-loop, code-review, workflow-writing, handoff, verification, ticket integration and wayfinder use that contract.

Make-pr-easy-to-review supports pull/merge requests, changelists and patch reviews. It replaces git/gh commands with native metadata and complete content comparison, including pending changes. Architecture surveying uses native history with an explicit unavailable-history fallback. Why's source-history reference and investigator prompts use native revisions, reviews and source-history tools. Prototype is now a maintained fork so its entrypoint and UI/logic references no longer mandate throwaway branches or main. Source repository URLs and revision pins remain unchanged for attribution.
