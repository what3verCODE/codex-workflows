# Validation evidence

## One-command setup

The root `setup.sh` supports download-and-pipe installation, defaulting to global installation and accepting `--workspace`. Seven integration tests now pass, including piped archive installation, reinstall preservation, the default global argument and failure before installer execution when the archive download fails.

On WSL, an actual run forced the missing-Python path using a local archive of the committed kit. It downloaded uv 0.12.13 and CPython 3.12.14 into temporary directories, then downloaded the pinned upstream skills and installed thirteen skills and seven agents into `/tmp/workflow bootstrap runtime`. The temporary tool directory was removed after completion. This verifies the fallback with real downloads; it does not claim a macOS run or availability of the public `main/setup.sh` URL before publication.

Recorded 2026-09-12. The source baseline is `bdef69b`, the initial specification/lock commit. Findings below distinguish deterministic checks from observed model behavior.

## Installer and source checks

`make check` passes five installer integration tests plus validation of thirteen skill requirements and seven TOML roles. The tests invoke the installer or Make as a subprocess and inspect observable destinations. They cover workspace paths with spaces without a destination Git repository, global destinations, reinstall replacement including stale managed files, preservation of unrelated skills/configuration, removal of manifest requirements without deleting old installations, pinned downloads, hash mismatch, failed download, symlink/path rejection and missing interpreter diagnostics.

An actual `make install WORKSPACE="/tmp/workflow installed kit"` downloaded all pinned upstream files and installed thirteen skills and seven role files. Source validation checks names, required skill references, role metadata and local links; it does not establish model behavior.

`make diff-upstream UPSTREAM_CHECKOUT=/tmp/workflow-matt-skills` compared all maintained files with the recorded upstream Git objects. The audit restored upstream UI metadata and preparation invocation policies. It also restored the original extensive user-story wording and diagnosis minimization criterion. Diagnostic phases remain upstream text, with an assignment-boundary paragraph and one VCS-neutral bisection substitution. See [provenance](../PROVENANCE.md) for each retained adaptation.

## Runtime and OS matrix

| Environment | Observed result |
| --- | --- |
| WSL2, Codex 0.154.0 | Actual installation and runtime skill discovery passed. A live bounded scout used the role-instruction fallback because the host's spawn tool had no named-role selector. |
| WSL2, Codex 0.153.4 | Cached installed binary ran the skill-discovery smoke check successfully. This is 0.153.4 evidence, not a run of 0.153.0. |
| macOS, user-reported test | Public test-branch installer returned thirteen skills and seven roles. Codex prompt discovery included development-loop. The scout reported direct selection through `agent_type: "scout"`, no TOML fallback and no file edits. Exact CLI version and tool trace were not captured. |

WSL kernel was `6.18.33.2-microsoft-standard-WSL2`, x86_64 with glibc 2.39; Python was 3.12.3. `make smoke` creates a temporary installation and Codex home, reads the actual `skills/list` app-server result, and checks the model-visible prompt for the installed development-loop skill. `CODEX_BIN` selects another installed binary without replacing the user's runtime. User-level skills can remain visible despite a temporary Codex home; the smoke test filters exact installation paths.

The supported prompt form is `$development-loop TICKET-ID optional instructions`. The CLI receives it as quoted prompt text. Prompt rendering verifies discovery, not completion of a live ticket. The live 0.154 scout found `/tmp/workflow installed kit/.agents/skills/development-loop/SKILL.md` after receiving the installed scout TOML instructions in a child. The live session reported 240034 input tokens, 222208 cached input tokens and 899 output tokens. These are whole-session counters, not a measurement of savings or a budget guarantee.

The tested WSL host could not select named roles directly. Fallback execution cannot apply role-level sandbox or skill-enable settings; parent settings remain effective. Defaults inherit the parent model, so no comparative model-quality claims or unverified assignments are made. Native scout selection was subsequently reported on macOS; role-specific model overrides and skill controls remain unverified. Standard TOML role files follow the official configuration documentation, but parsing and file presence do not establish their activation in this host.

## Behavioral evaluations

Disposable repositories and a JSON tracker stub were created outside the source tree. Their fixture baseline files are evaluation inputs, not durable state installed by the workflow.

| Scenario | Actual observation | Evidence |
| --- | --- | --- |
| Prepared code | Oracle readiness, observed negative-value regression failure, minimal implementation, four passing tests, memory update and scoped checkpoint | [Code](evaluations/code.md), [worker](evaluations/worker.md) |
| Existing edits | Reused task branch and relevant implementation, preserved unrelated notes byte-for-byte, demonstrated test sensitivity against isolated original source | [Code](evaluations/code.md) |
| Multi-project | One ticket updated two repositories with separate original baselines and checkpoints; both passed four tests | [Code](evaluations/code.md) |
| Clarification | Missing discount semantics produced a focused question; dependent fixture files remained unchanged | [Code](evaluations/code.md) |
| Prepared bug | Reused established cause, observed `None != 0` regression, minimal fix and two passing tests | [Preparation](evaluations/preparation.md) |
| Uncertain bug | Actual empty-input reproduction and distinguishing probes established cause; no application fix | [Preparation](evaluations/preparation.md) |
| Documentation only | Source-grounded examples, independent factual/prose review, no code tests | [Preparation](evaluations/preparation.md) |
| Existing/new ticket | Executed stub read, re-read, conditional update and create; preserved unrelated body, comments and labels | [Preparation](evaluations/preparation.md) |
| Ticket planning | Two stub tickets with textual and stub-native blocking relationships | [Preparation](evaluations/preparation.md) |
| Large discovery | Billing scout read its table, package rules and source without searching 1500 archive files | [Preparation](evaluations/preparation.md) |
| Review correction | Independent analyses caught duplicate code/docs defects; observed red/green partial correction, checkpoint, full original-baseline review and stop after round two with a remaining P2 | [Review](evaluations/review.md) |

Code evaluations completed one combined review round with no blocking findings across the four final code checkpoints. Reviews accounted for all requested categories, marking UI accessibility inapplicable and unavailable visual/TMS evidence accurately. The correction scenario deliberately retained a defect to exercise the second-round stop. This was a controlled worker shortfall, not a naturally observed error rate. Its final P2 was left in the disposable fixture as intended; it is not a defect shipped in the installer.

Thread limits required reuse of existing evaluator contexts for some specialists. Reviews were independent of the relevant implementation authors, but this does not fully verify fresh specialist dispatch. The diagnosis evaluator saw source before establishing its first red reproducer, so that run is not a blind diagnosis evaluation. Clarification and ambiguous-destination checks did not include a real human reply/resumption. Live tracker/MCP operations, bounded MCP retrieval, non-Git VCS execution and manual UI validation were not exercised. The later macOS checks are user-reported in the matrix above. Raw evaluation reports retain these limits and observations from before the later upstream audit; they are historical evidence, not current skill instructions.

## Issue status

The implementation covers the installer, discovery guidance, setup-free preparation, readiness/TDD/checkpoints, diagnosis handoff, combined review, documentation and development loop requested in #2–#9. The user accepted the macOS installation checks and approved promotion to main. Remaining environment and behavioral limits above are recorded separately from that acceptance; unrun checks are not represented as passing.

## Source review

Two independent reviewers inspected the complete `bdef69b..5b0e0e8` source change. [Specification review](evaluations/source-specification.md) found no actionable defect or unrequested fork changes. [Technical review](evaluations/source-technical.md) covered the remaining categories and found one P2 documentation contract mismatch: the installer resolves an explicitly supplied root alias before rejecting symlinks beneath it, while the README had claimed blanket symlink rejection. The README now describes the actual boundary. Generated whitespace was also cleaned up. The original source baseline remains fixed for the correction review.

## Documentation-only unslop scope

The macOS scout test exposed the upstream unslop description, which required application to every answer. The kit now maintains a fork changing only that description to documentation and memory-bank writing. Reviewer no longer requires unslop unconditionally. Routine answers, status updates and scout reports do not activate it. Upstream cleanup rules are unchanged. Existing independent user/global installations can still expose their own unslop instructions; the kit does not overwrite unrelated installations.

## macOS acceptance follow-up

After updating the temporary installation, the user reported that scout ran without invoking unslop. Oracle then identified missing project context and discount rules and requested an input/current/expected example instead of inventing behavior. The user accepted the installation and agreed to move forward. These are user-reported observations, not captured tool traces or complete end-to-end workflow verification.
