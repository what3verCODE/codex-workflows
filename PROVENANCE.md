# Skill sources

`skills-lock.json` preserves the pre-existing installed-skill inventory. Its `computedHash` values are content identifiers, not commit pins. `manifest.json` selects the kit requirements, records resolved revisions, and pins every downloaded file with SHA-256. The installer does not modify the old lock file or install every skill it lists.

Matt Pocock sources use [mattpocock/skills at 3cca18b368ae95cdbdebbff572ccafa662551015](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015). The source was fetched and inspected on 2026-09-12. Paths below are relative to that repository.

| Skill | Original path | Distribution and changes |
| --- | --- | --- |
| grilling | skills/productivity/grilling | Unmodified upstream download. Keeps design-tree questioning and explicit preparation decisions. |
| grill-me | skills/productivity/grill-me | Local fork. Replaces the Skill tool call with loading the shared grilling file. |
| grill-with-docs | skills/engineering/grill-with-docs | Local fork. Replaces Skill tool calls with loading the grilling and domain-modeling files. |
| wayfinder | skills/engineering/wayfinder | Local fork. Adds file-based skill loading when the Skill tool is unavailable and replaces mandatory setup with tracker resolution and a local Markdown fallback. Keeps the upstream map, ticket types, planning default and session limits. |
| domain-modeling | skills/engineering/domain-modeling | Unmodified upstream download with glossary and ADR formats. |
| research | skills/engineering/research | Unmodified upstream download. |
| prototype | skills/engineering/prototype | Unmodified upstream download with logic and UI references. |
| codebase-design | skills/engineering/codebase-design | Unmodified upstream download with its references. |
| tdd | skills/engineering/tdd | Local fork. Keeps behavioral boundaries, vertical red/green slices and test/mocking references. Accepts previously agreed boundaries, uses file-based skill loading, and yields to project terminology. |
| diagnosing-bugs | skills/engineering/diagnosing-bugs | Local fork. Adds an assignment-boundary paragraph for evidence reuse and diagnosis-only handoff, and replaces the Git-specific bisection command. Original phases, reproduction criteria and fix guidance remain intact. |
| code-review | skills/engineering/code-review | Local fork. Keeps independent standards/spec traceability and all twelve smell judgments in smells.md. Adds fixed multi-repository state, technical specialists, evidence/severity rules and duplicate aggregation. Removes setup and Git-only comparison requirements. |
| to-spec | skills/engineering/to-spec | Local fork. Keeps synthesis, extensive user stories, implementation/testing decisions and scope template. Resolves tools without setup, distinguishes existing-ticket updates from new issues, preserves unrelated content, and reuses agreed testing decisions. |
| to-tickets | skills/engineering/to-tickets | Local fork. Keeps tracer bullets, expand-contract planning, blocking edges and approved breakdowns. Resolves the tracker from intent/context, supports native relationships and partial publication reporting, and removes mandatory setup. |
| writing-for-agents | skills/productivity/writing-for-agents | Local fork. Keeps context pointers, hierarchy and pruning. Adapts invocation metadata to Codex and preserves normal discovery by default. |

The prose-cleanup skill is a local fork from [poteto/plugins at 74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12](https://github.com/poteto/plugins/tree/74dd2291e8e37b12fd6dc49b2acbd655c6bdaf12), original path `pstack/skills/unslop`. Its license comes from `pstack/LICENSE`. Only the discovery description changes: apply it to documentation writing, not conversational answers, scout findings or routine reports. The cleanup rules remain unchanged, and reviewer no longer requires it unconditionally.

Each local fork has `upstream.json` with repository, path, revision and the previous installed hash. Matt's license is included in each fork. Downloaded skills include their upstream license. Upstream agent UI metadata is preserved, including explicit-invocation policy for to-spec, to-tickets, grill-me, grill-with-docs and wayfinder. Unsupported `disable-model-invocation` frontmatter is removed from those forks; the equivalent existing Codex `agents/openai.yaml` policy remains.

`workflow-context`, `prepared-task`, `workflow-writing`, `development-loop`, the TOML roles, installer and evaluation tooling are original kit material derived from this project's specification.

To update a fork, compare its recorded revision with the desired upstream revision, retain relevant changes, and revise its `upstream.json`, manifest entry and this table together. To update a downloaded skill, change its immutable revision and all file hashes together. Never replace a commit with `main` or interpret a successful TOML parse as runtime compatibility evidence.
