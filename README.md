# Portable Codex workflow kit

Install editable Codex roles and skills, then run one ticket through discovery, implementation, documentation, checkpoint commits and at most two review rounds.

## Install with one command

Install globally with:

```sh
curl -fsSL https://raw.githubusercontent.com/what3verCODE/codex-workflows/main/setup.sh | sh
```

Run the same command again to update to the published kit. No repository clone, Git, Make or preinstalled Python is required. The installer uses an existing Python 3.11+ when available; otherwise it downloads temporary uv and Python tools and removes them afterward. It leaves shell profiles unchanged using uv's [unmanaged installation mode](https://docs.astral.sh/uv/reference/installer/#unmanaged-installations). This installs the workflow kit for your existing Codex installation.

To install into your current working directory:

```sh
curl -fsSL https://raw.githubusercontent.com/what3verCODE/codex-workflows/main/setup.sh | sh -s -- --workspace
```

You can still supply an explicit destination with `--workspace "/path/to/workspace"`. Both forms install skills and roles beneath the selected workspace.

To pin a version, use that tag or commit in both the script URL and `CODEX_WORKFLOW_REF` on the receiving shell. The script needs `curl`, `tar` and `mktemp`, provided by typical macOS and WSL installations. Advanced archive mirrors can set `CODEX_WORKFLOW_ARCHIVE_URL`; use only a source you trust to execute installer code.

## Manage the kit

Run `make` to see the available commands. Use this repository as the place to edit and update the kit.

```sh
make install                         # Install into this workspace
make install WORKSPACE="/path/to/workspace"
make install-global                  # Install for your user
make update                          # Reapply source changes to this workspace
make update-global                   # Reapply source changes globally
make check                           # Tests and source validation
make smoke                           # Isolated installed-runtime discovery checks
make fixtures                        # Disposable projects for behavioral evaluation
make diff-upstream                   # Inspect every maintained fork change
make run TICKET="TICKET-42"           # Open Codex with the loop
```

The repository Make commands need Make and Python 3.11 or newer, plus HTTPS access to the pinned GitHub skill sources. macOS users can obtain Make through Command Line Tools and Python through their usual package manager. WSL Ubuntu/Debian users need `make` and a supported `python3`. The scripts use the standard library and require no package installation. `make fixtures` additionally needs Git to create disposable evaluation repositories. Installation destinations need neither Git nor a clone of this repository. You can run Make from a downloaded source archive.

Workspace installation writes `.agents/skills/<name>` and `.codex/agents/<name>.toml` beneath `WORKSPACE`. Start Codex from that workspace root when working across services. Global installation writes skills to `~/.agents/skills` and roles to `$CODEX_HOME/agents`, falling back to `~/.codex/agents`. `INSTALL_HOME` and `CODEX_DIR` override those global destinations for testing or nonstandard layouts.

`make update` and `make update-global` reinstall the current source and pinned requirements. They do not fetch new kit revisions. Obtain the desired repository revision first, edit its sources if needed, then run the matching update target.

The manifest declares ownership of the named skill directories and role files. Reinstall overwrites those managed files, including local modifications and stale files within a managed skill. It preserves other skills, role files, personal configuration, credentials and policy. Removing a manifest requirement stops installing it and does not delete its old destination. Explicit destination roots are resolved to their canonical paths. Symlinks beneath those roots are rejected rather than followed. All downloads and configurations are checked before destination changes; installation is not a transaction across every destination.

## Use the workflow

Restart Codex after installation so it reloads available skills and roles. Invoke the skill with ordinary prompt text:

```text
$development-loop https://github.com/owner/project/issues/42
$development-loop TICKET-42 preserve the public API
```

The CLI form quotes the prompt so your shell preserves `$`:

```sh
codex '$development-loop TICKET-42 preserve the public API'
```

The loop reads the ticket and comments using available tracker tools. Scouts find relevant projects and rules. Bughunter investigates only when the cause is uncertain. Oracle checks readiness, worker implements through TDD, and writer updates affected documentation. Documentation-only work goes directly through writing and review. Missing understanding pauses dependent work for your answer.

The coordinator preserves existing edits, follows each project's VCS and branch conventions, and records original baselines in the conversation. It checkpoints completed work before review. Reviewer combines independent analyses of the complete ticket change. If corrections are needed, the loop updates code and docs, checkpoints them and reviews once more against the original baselines. It stops after the second review and reports remaining findings. These are instructions followed by the model, not runtime-enforced counters or guarantees. Manual UI validation remains yours.

Start task discovery with one of these installed entry skills:

```text
$grill-me assess this plan
$grill-with-docs sharpen this design and record the glossary and decisions
$wayfinder map the open decisions for this larger effort
```

Use `grill-me` for most plan discussions, `grill-with-docs` when you also want domain terminology and ADRs captured, and `wayfinder` when discovery spans multiple sessions and needs a map of decision tickets. They use `grilling` as shared questioning guidance. Wayfinder plans by default; implementation starts after the decisions are ready.

For an open decision, start a standalone council consultation:

```text
$council-mode Which programming language should I use for this project? Here are my goals and constraints: ...
```

Council accepts questions without candidate answers. Five read-only advisors explore options independently, each using a stable thinking style: Contrarian, First-principles thinker, Expansionist, Outsider and Executor. All receive the same facts and constraints and may discover any viable options. The host can run them in batches when slots are limited; missing perspectives are reported as an incomplete council.

Advisors then challenge material disagreements or shared unsupported assumptions when evidence could resolve them. The main agent returns a recommendation, alternatives, assumptions and unresolved decisions. It normally stops after at most two passes; a third requires your request and a remaining factual question that could affect the recommendation. These are behavioral limits, like the development loop's review cap.

You can use council in a separate session while grilling a plan. Bring the question, project facts, constraints and open points from that conversation; no prior grilling session or ticket is required. Council asks for essential missing context and returns a self-contained brief you can paste back into planning. It does not start implementation or adopt a decision for you.

Turn the agreed outcome into a specification and implementation tickets:

```text
$to-spec into https://tracker.example/issues/17
$to-spec as new issue in the current repository
$to-tickets split the agreed spec into tracer-bullet tickets
```

Existing-ticket requests update the relevant specification after reading the ticket and preserve unrelated content and discussion. New-issue requests create a new issue in the resolved destination. Drafts do not publish automatically. No tracker setup document or readiness label is required.

For individual roles, ask Codex in ordinary language, for example `Have scout locate the billing implementation and its project rules` or `Have bughunter diagnose this failure and return an implementation handoff`. There is no kit-specific slash command for a role. In the tested WSL 0.154 host, named-role selection was unavailable. The macOS tester subsequently reported direct scout selection through `agent_type: "scout"`, without fallback. On the WSL host, the loop instead supplied the installed role instructions to a child. This fallback inherits the parent's sandbox and skill availability; it cannot apply role-level sandbox or `skills.config` settings. Explicit model/reasoning overrides can be forwarded when the host's spawn tool supports them.

The kit also includes focused tools for work across frontend, services and CLI projects:

| Skill | Use |
| --- | --- |
| `verify-this` | Compare baseline and changed behavior to verify a fix or performance claim. |
| `handoff` | Save current task state and references for another session, including checkpoints and remaining review work. |
| `cli-for-agents` | Design commands with flags, useful help, retry-safe behavior and unattended operation. |
| `improve-codebase-architecture` | Survey maintenance hotspots and discuss concrete refactoring candidates in an HTML report. |
| `make-pr-easy-to-review` | Prepare accurate PR descriptions, verification evidence and reviewer reading guidance. Writer uses it during normal PR preparation; history rewriting is optional. |
| `why` | Investigate documented intent behind legacy code using history and relevant external evidence, with explicit uncertainty. |

Invoke `handoff` and `improve-codebase-architecture` explicitly when needed. The other additions can apply when the current task fits. PR preparation follows existing publication authorization and does not start another correctness review round. Framework-specific commands and conventions still come from each project's instructions.

For an agreed specification spanning multiple tickets, explicitly invoke `$implement-spec` with the spec or ticket graph. It reuses the existing roles, integrates predecessors and checks their agreed prerequisites before starting dependent tickets, and reviews the combined result. Independent tickets can run in parallel in available isolated contexts; otherwise it works sequentially. Additional working copies remain user-managed. Use `$development-loop` for a single ticket.

`resolving-merge-conflicts` handles in-progress merge, rebase, update or integration conflicts through the project's VCS. It preserves both changes' intent where possible, runs relevant checks and respects publication boundaries when completing an operation.

## VCS and review systems

Skills follow each project's chosen VCS and code-review host. They use native task identifiers, comparisons and checkpoints without requiring Git, a staging area, a task branch or a branch named main. Co-located metadata and hosting URLs do not override the project's working tool. Review requests can be pull requests, merge requests, changelists or patch reviews.

A centralized submit counts as publication and follows existing authorization. Local file snapshots can support comparison and handoff when no VCS is present; unavailable history remains an explicit limitation. Prototype and research artifacts can live in task-scoped storage instead of throwaway branches.

This kit's own source repository and upstream attribution use GitHub. Installer-source comparison commands are maintenance tools for this repository, not instructions for a project's VCS.

## Customize

Edit `kit/agents/*.toml` for role behavior, `model` and `model_reasoning_effort`. The current trial configuration is:

| Role | Model | Reasoning |
| --- | --- | --- |
| scout | `gpt-5.6-terra` | medium |
| oracle | `gpt-6-astra` | medium |
| advisor | `gpt-6-astra` | medium |
| worker | `gpt-5.6-terra` | high |
| bughunter | `gpt-6-astra` | high |
| writer | `gpt-5.6-sol` | medium |
| reviewer | `gpt-6-astra` | medium |
| review_specialist | `gpt-5.6-terra` | high |

Use Astra with medium reasoning for the main session through your Codex model settings. The installer configures child roles and does not change the main session's configuration. These assignments are a trial, not a benchmarked optimum. Check model availability in your runtime; remove both overrides from a role to inherit the parent settings.

Other role settings include `description` for role selection, `developer_instructions` for behavior, `sandbox_mode` for execution restrictions, `mcp_servers` for MCP configuration, and `skills.config` for skill enablement. See the [custom agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents). Keep concurrency settings in the main `.codex/config.toml`, under `[agents]`. Edit `manifest.json` to change required skills for a role, add upstream requirements, or select local forks. The installer adds supported `skills.config` entries with resolved skill paths. Required-skill instructions guide behavior; they do not guarantee exclusion of other skills or tools.

Unslop applies to documentation and memory-bank writing, not routine answers, scout findings or agent reports. Its original cleanup rules are preserved.

Edit maintained skill instructions under `kit/skills`. `.agents/` and `.codex/` are generated installation directories and are ignored in this repository. Upstream revisions, changes and licenses are documented in [PROVENANCE.md](PROVENANCE.md).

`make diff-upstream` reads each fork's pinned revision and prints changes to every upstream file, including supporting files and invocation metadata. It does not edit the kit. For an offline comparison, use `make diff-upstream UPSTREAM_CHECKOUT="/path/to/mattpocock/skills" POTETO_CHECKOUT="/path/to/poteto/plugins"` with both checkouts at their recorded revisions. The comparison reads committed upstream objects, so local edits in that checkout cannot change the reference.

## Compatibility and evidence

The targets are Codex 0.153 and 0.154 on macOS and WSL Ubuntu/Debian. See [validation evidence](docs/validation.md) for actual runtime/OS results, behavioral observations and missing checks. `make check` validates installation behavior and source structure. `make smoke` inspects what the installed Codex runtime discovers. Neither proves model behavior; the disposable scenarios exercise that separately.

Configuration references: [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills). These describe the configuration shape; the evidence report distinguishes it from what the installed versions actually accept.
