# Portable Codex workflow kit

Install editable Codex roles and skills, then run one ticket through discovery, implementation, documentation, checkpoint commits and at most two review rounds.

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

Installation needs Make and Python 3.11 or newer, plus HTTPS access to the pinned GitHub skill sources. macOS users can obtain Make through Command Line Tools and Python through their usual package manager. WSL Ubuntu/Debian users need `make` and a supported `python3`. The scripts use the standard library and require no package installation. `make fixtures` additionally needs Git to create disposable evaluation repositories. Installation destinations need neither Git nor a clone of this repository. You can run Make from a downloaded source archive.

Workspace installation writes `.agents/skills/<name>` and `.codex/agents/<name>.toml` beneath `WORKSPACE`. Start Codex from that workspace root when working across services. Global installation writes skills to `~/.agents/skills` and roles to `$CODEX_HOME/agents`, falling back to `~/.codex/agents`. `INSTALL_HOME` and `CODEX_DIR` override those global destinations for testing or nonstandard layouts.

`make update` and `make update-global` reinstall the current source and pinned requirements. They do not fetch new kit revisions. Obtain the desired repository revision first, edit its sources if needed, then run the matching update target.

The manifest declares ownership of the named skill directories and role files. Reinstall overwrites those managed files, including local modifications and stale files within a managed skill. It preserves other skills, role files, personal configuration, credentials and policy. Removing a manifest requirement stops installing it and does not delete its old destination. Symlink destinations are rejected rather than followed. All downloads and configurations are checked before destination changes; installation is not a transaction across every destination.

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

Preparation skills remain directly usable:

```text
$grilling assess this plan
$to-spec into https://tracker.example/issues/17
$to-spec as new issue in the current repository
$to-tickets split the agreed spec into tracer-bullet tickets
```

Existing-ticket requests update the relevant specification after reading the ticket and preserve unrelated content and discussion. New-issue requests create a new issue in the resolved destination. Drafts do not publish automatically. No tracker setup document or readiness label is required.

For individual roles, ask Codex in ordinary language, for example `Have scout locate the billing implementation and its project rules` or `Have bughunter diagnose this failure and return an implementation handoff`. There is no kit-specific slash command for a role. In the tested 0.154 host, named-role selection was unavailable. The loop instead supplied the installed role instructions to a child. This fallback inherits the parent's sandbox and skill availability; it cannot apply role-level sandbox or `skills.config` settings. Explicit model/reasoning overrides can be forwarded when the host's spawn tool supports them.

## Customize

Edit `kit/agents/*.toml` for role behavior and optional `model` and `model_reasoning_effort` overrides. Defaults inherit the parent settings, so the kit makes no unverified model assignment. Check your runtime's available models before adding an override. Edit `manifest.json` to change required skills for a role, add upstream requirements, or select local forks. The installer adds supported `skills.config` entries with resolved skill paths. Required-skill instructions guide behavior; they do not guarantee exclusion of other skills or tools.

Edit maintained skill instructions under `kit/skills`. `.agents/` and `.codex/` are generated installation directories and are ignored in this repository. Upstream revisions, changes and licenses are documented in [PROVENANCE.md](PROVENANCE.md).

`make diff-upstream` reads each fork's pinned revision and prints changes to every upstream file, including supporting files and invocation metadata. It does not edit the kit. For an offline comparison, use `make diff-upstream UPSTREAM_CHECKOUT="/path/to/mattpocock/skills"` with that checkout at the recorded revision. The comparison reads committed upstream objects, so local edits in that checkout cannot change the reference.

## Compatibility and evidence

The targets are Codex 0.153 and 0.154 on macOS and WSL Ubuntu/Debian. See [validation evidence](docs/validation.md) for actual runtime/OS results, behavioral observations and missing checks. `make check` validates installation behavior and source structure. `make smoke` inspects what the installed Codex runtime discovers. Neither proves model behavior; the disposable scenarios exercise that separately.

Configuration references: [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills). These describe the configuration shape; the evidence report distinguishes it from what the installed versions actually accept.
