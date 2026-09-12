# Source technical review

Repository /home/alexandr/projects/codex-workflow. Original baseline bdef69b9167cd11433e38be93f131b95bf8ecbba; checkpoint 5b0e0e838c6623ad31807a2452650f7dbee9a438. HEAD matched checkpoint and working status was clean before and after review. No repository edits were made. This is a leaf specialist review, without recursive reviewers or repairs, using an existing independent context.

## Finding

P2 at scripts/install.py:62 and scripts/install.py:65, correctness/security and test-quality origins. Destination roots are resolved before check_destination inspects symlinks. A workspace alias pointing at another directory is therefore followed and installation succeeds there, although README.md:28 promises symlink destinations are rejected. The same ordering applies to the global Codex home. The advertised protection covers links below the resolved root but does not cover a linked root or its original ancestors.

Reproduced with a temporary local-only manifest, one example skill, an actual directory and an alias symlink pointing to it. Invoking `python3 scripts/install.py --workspace <temp>/alias --manifest <temp>/manifest.json` returned 0, printed installation into `<temp>/actual`, and created `<temp>/actual/.agents/skills/example/SKILL.md`. This test used no network and touched only /tmp. A user relying on refusal of linked destinations instead writes through the link; existing managed names in the target can be replaced. This is a contract mismatch, not evidence of a remote exploit.

Concrete correction: preserve the user-supplied destination spelling and validate linked roots before resolving, with a deliberate policy for platform path aliases, or explicitly document that root aliases are supported while only links below the resolved root are rejected. Add observable workspace/global-root symlink tests that establish that chosen policy. The existing symlink test covers a skill-directory link and misses this case. Treat as blocking until runtime behavior and the stated protection agree.

## Checks and coverage

`PYTHONDONTWRITEBYTECODE=1 make check` passed all 5 installer integration tests and validated 13 skills and 7 roles. Existing tests exercise global reinstall, authoritative managed-tree replacement, unrelated skill/config preservation, removed manifest requirements, workspace paths with spaces without destination Git, missing Python reporting, pinned download integrity/failure preservation, traversal names and a linked skill destination.

An additional temporary fake Codex executable verified `make run` with a workspace path containing spaces and prompt literals `$(literal)`, backticks and `$HOME`. Received the exact workspace and `$development-loop` prompt with those characters preserved; no shell expansion occurred. A separate local-manifest test reproduced the symlink finding above.

| Category | Result |
| --- | --- |
| Standards | Reviewed available project/spec rules, source separation, managed-file scope and check conventions; no separate finding. |
| Correctness | Reviewed installer staging, manifest validation, rendered TOML, Make argument passing, upstream diff enumeration and smoke discovery parsing; root-link policy finding above. |
| Architecture and maintainability | Reviewed manifest ownership, separate installer/validation/smoke/diff responsibilities and shared manifest validator; no evidence-backed change requested. |
| Runtime defects | Reviewed failed downloads before publication, destination validation, subprocess cleanup/timeouts and fixture refusal of existing roots; no additional finding. Cross-destination transaction is explicitly not promised. |
| Security | Reviewed contained source paths, source/destination links, pinned hashes, subprocess argument lists and Make prompt handling; root-link promise mismatch above. No unsupported exploit claim. |
| Accessibility | Inapplicable; this change provides CLI/configuration/prose, no interactive UI or browser controls. |
| Type safety | Reviewed dynamic manifest key/type validation and TOML parse before installation; no additional actionable issue for the maintained manifest. |
| Reuse | Python standard library covers downloads, hashing, TOML, copies, diffs and subprocesses; no justified new dependency. |
| Test quality | Existing integration tests use observable destinations and preserve unrelated fixtures. Root symlink coverage gap is attached to the same finding. Runtime-role selection and OS coverage limits remain acknowledged. |

Specification/documentation judgments beyond the cited installer contract belong to the other specialist. Read installer, shell wrapper, Makefile, smoke/diff/validation/fixture scripts, complete installer tests, manifest, role templates, code-review skill and smells reference, workflow-context, README and relevant specification requirements. Full original-baseline change inventory was inspected; these technical source files are newly added in that complete range, not only the most recent commit. No unread local executable dependency remains for the installer/management path. Python standard-library, Make, Git and Codex internals were not read. Live upstream network retrieval and actual Codex smoke were not rerun by this specialist; other evaluators own that evidence. No macOS or WSL run was performed here. No visual/E2E/TMS integration applies to the installer boundary.
