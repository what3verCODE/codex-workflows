# Workflow kit

Skills and subagent roles that take a ticket from description to a reviewed change. Works with Codex and Claude Code, and with any VCS.

- **Upstream skills, unchanged.** Skills from [mattpocock/skills](https://github.com/mattpocock/skills), [poteto/plugins](https://github.com/poteto/plugins) and [ponytail](https://github.com/DietrichGebert/ponytail) are installed byte-for-byte at pinned revisions (`sources.json`). Nothing is forked.
- **A thin layer of our own** (`kit/`): the workflow skills and the roles that tie upstream skills together.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/what3verCODE/codex-workflows/main/setup.sh | sh                          # global, Codex + Claude Code
curl -fsSL https://raw.githubusercontent.com/what3verCODE/codex-workflows/main/setup.sh | sh -s -- --agent codex     # global, Codex only
curl -fsSL https://raw.githubusercontent.com/what3verCODE/codex-workflows/main/setup.sh | sh -s -- --workspace       # current directory
```

Run it again to update. It needs `curl`, `tar` and Python 3.11+ (downloaded temporarily through uv if missing). No git, Node or clone needed. Restart the agent afterwards.

| | Codex | Claude Code |
| --- | --- | --- |
| Skills, global | `~/.agents/skills` | `~/.claude/skills` |
| Roles, global | `$CODEX_HOME/agents/*.toml` (default `~/.codex`) | `~/.claude/agents/*.md` |
| Workspace | `.agents/skills`, `.codex/agents` | `.claude/skills`, `.claude/agents` |

The installer owns only what it installed, recorded in `.workflow-kit.json` in each directory. Reinstalling replaces those entries, removes ones that were dropped from the kit, and leaves your own skills, roles and config alone. If anything fails, the previous install is restored.

**Ponytail hooks.** The kit installs ponytail's skills. Its hooks (session activation, mode tracking) come only with the native plugin. Optional:

```sh
claude plugin marketplace add DietrichGebert/ponytail && claude plugin install ponytail@ponytail
codex plugin marketplace add DietrichGebert/ponytail && codex plugin add ponytail@ponytail   # then trust hooks in /hooks
```

If you install the plugin, the plugin's skills and the kit's copies are duplicates; that is harmless, but you can drop ponytail from `sources.json`.

## Use

**Once per repo**, run `/setup-matt-pocock-skills` (Claude) or `$setup-matt-pocock-skills` (Codex). For a non-GitHub tracker, choose **Other** and describe it; matt's skills read it from `docs/agents/issue-tracker.md`. Put your VCS commands in `AGENTS.md`/`CLAUDE.md` (see below).

| Goal | Skill |
| --- | --- |
| Implement one ticket | `$dev-loop TICKET-42` |
| Review a change | `$review since <baseline>` |
| Sharpen a plan | `$grill-me`, `$grill-with-docs`, `$wayfinder` |
| Decide between options | `$council-mode <question>` |
| Plan → spec → tickets | `$to-spec`, `$to-tickets` |
| Find a bug's cause | `$diagnosing-bugs` |
| Cut code | `$ponytail-audit`, `$ponytail-review` |
| Resolve merge/rebase conflicts | `$fix-merge-conflicts` |
| Write a PR / review-request body | `$pr` |
| Improve the agent setup after a session | `$retro` |

Claude Code uses `/name` instead of `$name`.

### dev-loop

1. You (the main agent) read the ticket, rules and code. A **scout** searches only when the search is broad. A **bughunter** runs only when a bug's cause is unclear.
2. The task gets a size:
   - **Small** (add a field or flag, an obvious fix): the main agent builds it directly.
   - **Medium**: a short plan, then one **worker**.
   - **Large**: a plan you approve, then workers.
3. Build with `ponytail` (smallest complete change) and `tdd`.
4. Checkpoint, then `review`. Fix must/should findings, then review once more. Two rounds max.
5. Report: changed files, checks actually run, open findings, baseline → checkpoint. The review-request description is drafted with `pr`.

### review

Runs matt's `code-review` (standards + spec) and a **reviewer** with `ponytail-review` (bugs, risk, scale, tests, lean) in parallel. Then the main agent re-checks every finding against the code and drops the ones it cannot confirm. You get a numbered list marked confirmed/likely, with a verdict.

## Roles

| Role | Does | Skills |
| --- | --- | --- |
| scout | Read-only search; returns `path:line` and rules | vcs-bridge |
| worker | Implements a brief; smallest diff, test-first; reports real check output | ponytail, tdd, vcs-bridge |
| reviewer | Read-only review with concrete failing cases | ponytail-review, vcs-bridge |
| bughunter | Reproduces and finds root cause; no fix | diagnosing-bugs, vcs-bridge |
| advisor | One council perspective, read-only | none |

Each role is defined once in `kit/agents/<role>.md` (frontmatter + instructions). The installer writes Codex TOML and Claude Code Markdown from it. `readonly: true` becomes `sandbox_mode = "read-only"` in Codex and blocks edit tools in Claude Code.

Models are inherited from the main session by default. To pin one, add any of these to a role's frontmatter: `codex_model`, `codex_effort`, `claude_model`.

## Any VCS

Upstream skills talk about git and GitHub. The kit's `vcs-bridge` skill maps that to the project's real tools: diff against the recorded baseline, local checkpoint instead of commit, review request instead of PR, your tracker instead of GitHub Issues. It reads the mapping from the project's `AGENTS.md`/`CLAUDE.md`, so describe your VCS there, e.g.:

```md
VCS: `snap` (not git). Status `snap status`, diff `snap diff <rev>`, checkpoint `snap save -m <msg>`. Ask before `snap submit`.
```

For a spec split into several tickets, run `dev-loop` once per ticket.

## Maintain

```sh
make install [WORKSPACE=/path] [AGENT=codex|claude|all]
make install-global [AGENT=...]
make check        # installer tests + source validation (offline)
make smoke        # fresh install, then check Codex discovers every skill
make fixtures     # disposable scenarios, incl. flag-field speed benchmark, planted review bug, non-git project
make bump         # pin all upstream sources to their latest commit
make run TICKET=ID
```

- **Update upstream skills:** `make bump` pins every source to its latest commit; then `make check smoke`. Official plugins track upstream `main`, so bump regularly to stay identical to them.
- **Add a skill:** add `name: path` under the right source, or a new source.
- **Our own skills and roles:** edit `kit/skills` and `kit/agents`.
- **Generated, git-ignored:** `.agents/`, `.codex/`, `.claude/skills`, `.claude/agents`.
