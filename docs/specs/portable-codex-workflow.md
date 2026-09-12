# Portable Codex workflow kit

## Problem Statement

The developer currently uses grilling, specification, and ticket-writing skills to prepare work, then asks a main Codex agent to read a ticket, investigate, clarify uncertainties, and implement it. Each subsequent step often needs another explicit request. Occasional delegation has no consistent role or skill assignment.

Large monorepos and workspaces containing many services and packages make discovery expensive. File searches and MCP responses fill the main agent's context with material that implementation does not need. Tasks can span arbitrary projects, not just one frontend and its backend.

The developer needs a reusable configuration that coordinates specialists, follows local project instructions, verifies changes, updates documentation, and performs bounded review and correction. It must work from a workspace root or global installation, across home and work environments, without requiring a Git clone in the installation destination.

## Solution

Provide a portable Codex-only kit containing editable agent definitions, a development-loop skill, selected third-party skills, locally adapted skills with upstream provenance, and an installation/update script.

The developer invokes the development loop with a ticket identifier and optional instructions. The main agent resolves the ticket using the available tracker tools, discovers relevant projects and rules, and coordinates specialist agents. Scouts perform targeted discovery and return compact evidence. Oracle checks readiness and the approach. Worker implements code using TDD. Writer updates affected documentation. Reviewer coordinates independent specialist analyses and combines their findings.

Unresolved questions return to the developer before dependent implementation proceeds. The workflow creates checkpoint commits on appropriate task branches and permits at most two review rounds per invocation. It uses available automated tests and leaves manual UI validation to the developer.

The kit can be installed globally or into the root from which the developer works on projects. Source-controlled defaults are authoritative; updates overwrite managed destination files. Unrelated installed skills and personal configuration remain outside the kit's ownership.

## User Stories

1. As a developer, I want to start work with a ticket identifier and optional instructions, so that I do not have to request each development stage separately.
2. As a developer, I want to keep my existing grilling, specification, and ticket preparation process, so that prepared tickets can enter implementation directly.
3. As a developer, I want ticket retrieval to use my available GitHub, Gitea, or work MCP tools, so that the workflow is not tied to one tracker.
4. As a developer, I want the workflow to use my existing project-name and path table, so that it can find relevant services and packages.
5. As a developer, I want one ticket to span the projects it actually affects, so that cross-project work is coordinated.
6. As a developer, I want target-project instructions loaded even when Codex starts elsewhere, so that implementation follows service and package rules.
7. As a developer, I want scouts to perform large file searches, so that discovery output does not exhaust the main agent's context.
8. As a developer, I want multiple scouts to investigate independent paths or MCP sources, so that discovery can proceed in parallel when useful.
9. As a receiving agent, I want concise findings with exact source references and uncertainties, so that I can inspect relevant evidence without repeating broad discovery.
10. As a developer, I want oracle to assess readiness and the proposed approach before implementation, so that unresolved decisions reach me early.
11. As a developer, I want agents to ask when missing information makes progress difficult, so that I can provide facts or a cause I already know.
12. As a developer, I want a bug ticket with an established cause to bypass redundant diagnosis, so that preparation work is reused.
13. As a developer, I want bughunter available when the cause is uncertain, so that implementation follows evidence.
14. As a developer, I want worker to use the TDD skill for code behavior changes, so that tests guide implementation.
15. As a developer, I want documentation-only tasks routed to writer and reviewer, so that they do not generate meaningless code tests.
16. As a developer, I want changed behavior reflected in affected project documentation and memory banks, so that future work uses current information.
17. As a developer, I want verification to follow the project's available unit, visual, or end-to-end tests, so that checks fit the actual environment.
18. As a developer, I want manual UI validation left to me, so that the workflow does not assume browser access it lacks.
19. As a developer, I want review to check the ticket specification and documented standards independently, so that compliance on one dimension does not hide failure on another.
20. As a developer, I want review to cover correctness, architecture, types, security, accessibility, reuse, and tests wherever applicable, so that categories are not silently omitted.
21. As a developer, I want reuse review to consider existing code and trusted packages, so that new utilities do not duplicate suitable capabilities.
22. As a developer, I want review findings to include evidence, impact, locations, and corrections, so that fixes are actionable.
23. As a developer, I want duplicate findings consolidated while retaining their review categories, so that I do not spend time addressing the same defect twice.
24. As a developer, I want at most two review rounds in an invocation, so that automatic correction does not become an endless token-consuming loop.
25. As a developer, I want unresolved findings reported after the second review, so that incomplete work is not presented as accepted.
26. As a developer, I want task branches and checkpoint commits, so that implementation and review fixes have inspectable history.
27. As a developer, I want branch selection and naming to follow my workspace conventions, so that the kit supports different VCS environments.
28. As a developer, I want existing edits assessed for relevance, so that useful work is preserved without silently including unrelated changes.
29. As a developer, I want each invocation to handle one ticket in its current workspace or worktree, so that separate terminals can own separate tasks.
30. As a developer, I want editable role instructions, skill assignments, models, and reasoning settings, so that I can tune quality and token usage.
31. As a developer, I want global or workspace-root installation on macOS and WSL Linux, so that I do not have to copy configuration into every service.
32. As a developer, I want an installer that does not require Git in the destination, so that it works with my work filesystem and VCS.
33. As a developer, I want required skills installed from a manifest while unrelated skills remain untouched, so that setup is repeatable without replacing my whole environment.
34. As a maintainer, I want locally adapted skills to record their upstream origin and revision, so that I can compare future upstream changes.
35. As a maintainer, I want generated installation files ignored and maintained source kept separate, so that the repository clearly identifies what is edited and distributed.
36. As a developer, I want to evaluate the kit on ADE before adding more machinery, so that refinements follow real usage.
37. As a developer, I want forked skills to work without a setup ceremony, so that I can invoke them directly with my intent and destination.
38. As a developer, I want to specify an existing ticket or request a new issue when generating a spec, so that the skill performs the requested operation without assuming a fixed publication flow.

## Implementation Decisions

### Distribution and ownership

- Maintain agent definitions and owned or forked skills in a source directory. Keep installation scripts in a separate sibling scripts directory.
- Ignore the entire local agent-installation directory. Installed third-party material is not maintained source.
- Retain a version-controlled skill manifest and the existing skill lock information. Distinguish upstream-installed skills from locally maintained forks and original workflow skills.
- The installer supports global and workspace-root destinations. Installing into individual services is not the default.
- Updates overwrite kit-managed files from the authoritative source. Do not introduce merge prompts or preserve local modifications to managed files as an implicit customization system.
- Leave unrelated installed skills and unrelated personal configuration untouched. A removed manifest entry stops being an installation requirement; do not infer authority to delete arbitrary existing skills.
- Record each fork's upstream repository, original skill path, revision, and a concise account of local changes. Original project requirements need no upstream record.
- Installed lock entries contain content hashes, not proof of an upstream commit pin. Resolve and record revisions for forks before claiming reproducible upstream comparisons.

### Setup-free skill invocation

- Apply the setup-free convention to every maintained skill fork, not only review or the development loop. Remove mandatory setup-skill calls and prerequisite tracker/configuration documents. Optional configuration may refine defaults but is not required to invoke a skill.
- Resolve behavior from explicit user instructions first, then applicable project instructions and available context, then sensible skill defaults. Preserve useful upstream defaults when compatible with those inputs and this specification.
- Support requests such as "to-spec into this TICKET" and "to-spec as new issue". The former updates the identified ticket; the latter creates a new issue in the resolved destination. Do not create a duplicate issue when the user requested an update.
- Read an existing destination before updating it. Preserve unrelated ticket content and discussion; replace or update the relevant specification content according to the request.
- Resolve destinations and operations through available repository metadata, conversation context, and tracker tools. Ask only for information that remains necessary and ambiguous after inspection. Do not substitute a request to run setup for a focused clarification.
- Missing tool access or credentials must be reported as the actual limitation. Defaults do not establish access or justify guessing a destination.
- Publishing defaults, including labels, must yield to explicit requests and workspace conventions. A readiness label is not a prerequisite for using a forked skill.

### Runtime and roles

- Support Codex only. Compatibility targets are the user's 0.153 home installation and 0.154 work installation. Validate supported configuration syntax and capability differences rather than assuming Pi frontmatter works in Codex.
- Use Codex-supported custom agent configuration and skill discovery controls. Required-skill instructions are behavioral guidance, not a claim of enforced isolation from every other skill or tool.
- The main agent owns the user conversation, ticket scope, transitions, clarification, and final reporting.
- Scout owns discovery across files and relevant MCP sources. Assign bounded search questions or regions; use multiple scouts for independent discovery when useful. Return compact findings, exact references, relevant instruction locations, and uncertainty, not exhaustive search output. Findings guide subsequent source inspection and do not replace reading mandatory instructions.
- Oracle checks readiness and the implementation approach. It uses available ticket details, comments, and scout evidence. It returns unresolved decisions to the main agent for grilling; otherwise work proceeds without a routine approval step.
- Worker owns code implementation and corrections, and uses the TDD skill. Documentation-only changes do not require code tests.
- Bughunter uses the diagnosis skill when a cause remains uncertain. Existing investigation in a ticket or its comments can make another diagnosis unnecessary. Discovery of missing information returns to the developer rather than forcing a fixed number of failed attempts.
- Writer handles project documentation, memory-bank updates, and prose such as drafted tickets or comments. Use the installed prose-cleanup skill and the target project's writing conventions.
- Reviewer owns review coordination and aggregation. It may launch bounded specialist analyses. Review children report findings; they do not start repair loops or recursively repeat the coordinating review skill.
- Agent model and reasoning choices are editable. Sol, Terra, Luna, and Astra were discussed as candidates; no final assignments or comparative performance claims have been accepted.

### Development loop

- Expose a development-loop skill accepting a ticket identifier and optional user instructions. Verify the supported invocation syntax in the target Codex versions.
- Resolve tickets through the workspace's available tools and conventions. Do not require a tracker-specific readiness label or a hard-coded issue-tracker document.
- Discover target projects through the existing project table and task evidence. Read applicable service/package agent instructions and referenced rules before dependent work, including projects outside the starting directory.
- Inspect existing edits and their relevance. Preserve unrelated work, incorporate relevant work as appropriate, and ask when missing information prevents a sound decision. A dirty workspace is not an automatic blocker.
- Reuse a branch for the current task. If the current branch belongs to another task or is a base branch, create an appropriate task branch from the configured base while preserving existing work. Branch naming and VCS operations follow user/workspace conventions.
- Record a comparison baseline in conversation context for each affected repository before implementation. Do not introduce persistent run-state machinery.
- Normal sequence: scout as needed, bughunter if needed, oracle, implementation, documentation updates if needed, checkpoint commit, review.
- If corrective findings require another pass: worker corrections, documentation updates if needed, checkpoint commit, second review, then stop.
- A review round includes all of its specialist analyses. Permit at most two rounds per invocation. Track progress in conversation context; no durable cross-session review counter is required.
- Worker can perform normal TDD test-and-fix cycles within a pass. These do not consume additional review rounds. Ask the developer when understanding is blocked; do not add a fixed failed-test retry policy.
- Correct blocking findings and clearly actionable in-scope findings. Keep optional improvements separate. After the second review, report remaining issues without automatically launching a third pass.
- Checkpoint commits include completed task changes and relevant documentation. Review the complete task change against the original baseline, not only the uncommitted tree or latest repair commit.
- Use the configured VCS rather than embedding Git-only commands in generic workflow instructions. Commits on task branches are part of this workflow. Personal/global rules govern pushing and other publication; do not add a duplicate push-approval policy to the kit.
- One invocation handles one ticket. Separate worktrees or terminals are user-managed.
- Report changes, automated verification, checkpoint references, review results, unresolved issues, and any manual validation needed.

### Combined review skill

- Fork Matt Pocock's review skill and combine its standards/spec separation with independent specialist analyses, source-state consistency, evidence requirements, and finding aggregation as defined below.
- Preserve traceability to both requirements and documented standards. Retain useful code-smell heuristics as judgments, not automatic violations; project rules take precedence.
- Adapt fixed-point comparison and task retrieval to supplied workspace/VCS evidence. Remove requirements for Git-only commands, mandatory tracker setup documents, and readiness labels.
- Resolve the exact review scope before analysis. For a pull-request review, use the workspace's configured VCS tools and their usage instructions to retrieve metadata, changed files, and per-file changes. Read direct dependencies needed to understand changed behavior.
- Every round accounts for specification compliance, project standards, general correctness, architecture and maintainability, runtime defects, security, accessibility, type safety, reuse, and test quality.
- Use independent specialists for applicable analyses, inspecting the same checkpoint. State when a category is inapplicable or unavailable and why. Do not prompt the developer to select categories before every review.
- Reuse review considers existing project code, existing dependencies, and trusted packages. Internal packages are a work-specific example. Findings must justify suitability and dependency costs rather than assume adding a dependency is preferable.
- Test review includes unit and available visual or end-to-end tests. Check TMS alignment when relevant information exists. React-specific inspection includes dependencies, cleanup, and stale closures when applicable.
- Combine duplicate findings while preserving their standards/spec and specialist origins. Classify by severity and user impact, distinguishing blocking defects from optional improvements. Use a consistent severity vocabulary without allowing category-specific findings to disappear in aggregation.
- Require exact locations, evidence, impact, and concrete correction guidance. Reject unsupported claims and style-only preferences. State review limits, unread dependencies, and whether blocking defects remain.
- Documentation review checks factual accuracy against code and task evidence, local conventions, consistency, and prose quality. It does not invent a requirement for code tests.

## Testing Decisions

- Test external behavior at the highest useful boundaries. Avoid tests that merely assert prompt wording or mirror implementation internals.
- Proposed primary automated boundary: invoke the installer in temporary global-style and workspace-style destinations, then inspect observable installation results.
- Cover installation of required dependencies and local forks, repeated installation, replacement of managed files, preservation of unrelated installed skills and personal configuration, paths containing spaces, and useful failure reporting for missing prerequisites or failed downloads.
- Exercise forked skills without setup-generated configuration. Verify explicit existing-ticket updates, explicit new-issue creation, preservation of unrelated ticket content, context-based destination resolution, and focused clarification for unresolved destinations. Confirm that no mandatory setup invocation is introduced.
- Exercise supported shell behavior on macOS and WSL Linux. A Linux-only run does not establish macOS compatibility.
- Validate agent and skill discovery using the installed Codex runtime. Confirm required skills and usable configurations, including role-specific models where available, rather than validating only TOML parsing.
- Proposed workflow acceptance boundary: invoke the development loop against representative tasks in disposable projects. Include a prepared code ticket, a ticket needing clarification, a bug with an established cause, a documentation-only ticket, a multi-project change, an existing-edit case, and a review requiring corrections.
- Observe discovery delegation, instruction loading, TDD behavior, documentation updates, branch choice, checkpoint content, full-baseline review, and completion after no more than two review rounds.
- Include a large-search fixture and a bounded MCP discovery scenario to assess whether scouts return actionable references without flooding the coordinator's context. Measure observed context/usage where available without inventing savings guarantees.
- Validate that all review categories are addressed or explicitly marked inapplicable/unavailable, that findings carry evidence, and that duplicates are consolidated without losing standards/spec traceability.
- Distinguish live behavioral evaluations from deterministic tests. Instruction-based review limits and skill discipline are not hard runtime enforcement guarantees.
- Run available project checks for product changes. Do not require browser access or add Storybook/E2E infrastructure merely to satisfy the workflow; the developer performs manual UI validation.
- No implementation or test suite currently exists in this repository. The installed upstream skills provide behavioral guidance, not existing test infrastructure.
- These acceptance boundaries define the proposed implementation validation. No tests have been executed for the proposed kit.

## Out of Scope

- Supporting Pi, Claude Code, or other agent runtimes.
- A persistent workflow engine, durable run database, or hard token-budget enforcement.
- Persistent review counters across new conversations.
- Automatic management of concurrent tickets or worktree lifecycles.
- A new ticket tracker, mandatory readiness labels, or replacement of existing preparation skills.
- Encoding company-specific package catalogs, credentials, MCP endpoints, branch naming, or personal push policy in shared defaults.
- Installing configuration into every service by default.
- Automatic publishing, deployment, or PR creation as the default completion behavior.
- Guaranteed exclusion of all unassigned skills through prompt text alone.
- Automatic merging of local edits to managed installation files.
- A fully automated fork-rebase system for third-party skills.
- Mandatory manual-browser automation or new visual/E2E infrastructure in target projects.
- Final model selection without compatibility checks and practical evaluation.

## Further Notes

- Initial adoption will use ADE work to evaluate usefulness, token consumption, and review quality before adding orchestration machinery.
- Upstream skill sources already recorded locally include Matt Pocock's skills and the prose-cleanup skill from poteto's plugin collection.
- Work-specific review operations are supplied through workspace instructions. The specialist review requirements are fully defined in this specification.
- The project repository and specification issue tracker are https://github.com/what3verCODE/codex-workflows. Use Matt Pocock's default preparation-skill conventions for this project's specification publication without requiring a setup-skill run.
- The distributed development loop does not require readiness labels in target workspaces. This is separate from the preparation-skill defaults used to publish this project's specification.
