# VCS-neutral managed skills

The user requested a VCS-agnostic kit. The audit covered all 25 manifest-selected skills, including supporting references and agent instructions. Source attribution and this repository's installer-maintenance tools can name GitHub or Git; operational skill workflows must use the target project's chosen VCS and review host.

| Finding | Change |
| --- | --- |
| workflow-context always created a task branch and assumed staging | Resolve native task/change identifiers and pending work; branches and staging are optional. Respect the chosen working tool even with co-located Git metadata. |
| Checkpoints could imply a centralized submit | Treat shared submits as publication; use available local snapshots or review artifacts when submission is outside scope. |
| PR preparation executed git and gh commands | Use native review metadata, pending changes and complete content snapshots for before/after identity. Support pull/merge requests, changelists and patch reviews. |
| Architecture survey required git log | Use native change history, or report unavailable history and survey from task evidence and observed friction. |
| why history reference required git/gh | Use available native history and review operations, with explicit missing-history limits. Supporting investigator and incident/analytics references use source-history terminology. |
| prototype and wayfinder mandated throwaway branches | Preserve runnable artifacts in project storage, native isolated changes or local snapshots. Prototype is now a local fork, including its logic/UI references. |
| Handoff, verification and ticket integration assumed Git-shaped state | Use fixed revisions, change identifiers, pending work, snapshots and the project's native integration context. |

Verification passed: seven installer/bootstrap tests, source validation for 25 skills and seven roles, and Codex 0.154.0 discovery of all 25 skills in a disposable installation. Independent static review found no blocking assumption in four scenarios: Jujutsu co-located with .git and hosted on GitHub; Perforce without submit authorization; SVN without a task branch; and no VCS with supplied snapshots. These scenarios were reviewed as instructions, not executed against live VCS installations.

The managed definitions are synchronized into the workspace and global skill locations. Global agent configuration and unrelated extra skills remain unchanged. Those unmanaged extras can still contain Git-specific instructions, including resolving-merge-conflicts, scaffold-exercises, implement and implement-spec; they are outside this kit's manifest and this adaptation.

The installation rollback snapshot is `/tmp/vcs-neutral-kit-backup-wzr_j34e`. It contains affected installation paths, including the former global copies and update records. It is temporary storage, not a durable archive.

The user subsequently selected resolving-merge-conflicts and implement-spec for adoption. Both now have VCS-neutral maintained forks, bringing the kit to 27 skills. Implement-spec remains explicitly invoked and coordinates a complete ticket graph through the existing roles. Unmanaged implement and scaffold-exercises remain outside the kit.
