# Source history and repository evidence

## What this source contains

- Native revision or change history, including descriptions, dates, authors and diffs
- Review descriptions, comments and discussion through the project's configured review tools
- Inline code comments, TODOs, FIXMEs, deprecation notes
- ADRs (architectural decision records) if the repo keeps them
- Tests. Names and assertions often encode the edge cases that motivated a change
- Related files modified in the same commits (co-change signal)
- CHANGELOG entries, release notes in the repo
- Issue/ticket IDs mentioned in commit messages and PR bodies

Source history ties evidence to the changed code. It can be incomplete because of retention, imports, squashing, shallow copies or missing review records.

## How to search it

Use the project's chosen VCS and review host. Their native tools may expose revisions, changelists, patch sets, bookmarks or snapshots instead of Git branches and commits. A Git-backed host or co-located metadata does not override the project workflow.

Expand the seed change history with the available operations:

- Follow a file's history through renames and moves.
- Find revisions that introduced or removed the target text or behavior.
- Attribute the relevant lines to their originating changes.
- Inspect complete changes and their descriptions, including related files.
- Compare fixed earlier and later states of the target.
- Open linked review discussions, tickets and decision records through available tools.

Resolve syntax from project instructions, tool schemas or native help. Use only operations supported by the actual VCS. If line attribution, search history or review access is unavailable, use remaining sources and report the limitation. Preserve history without creating branches, modifying working state or submitting changes merely to inspect it.

Local file snapshots can establish a before/after change when no VCS is present, but they do not establish authorship or rationale by themselves. Seek explicit intent in supplied change notes or linked decisions and distinguish missing history from a search that found no rationale.

Look for out-of-band docs:

```bash
# ADRs often live in docs/adr/ or similar
rg -l -i 'architecture.decision' --glob '*.md'

# TODOs and FIXMEs near the target
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>

# Related tests. Names often encode the "why"
rg -l '<symbol>' --glob '*test*'
```

## What good evidence looks like here

- A PR description that explains the problem being solved, not just the change ("This fixes the pagination bug that caused X")
- A long review thread where alternatives were debated
- An inline comment near the target line that explains a non-obvious constraint
- A test named `test_handles_edge_case_when_X` that reveals an edge case motivating the code
- A commit message that references a ticket or incident ID
- A CHANGELOG entry that summarizes the user-visible rationale

## Common pitfalls

- **Squash-merge flatlands.** If the repo squashes PRs, individual commits in the branch history are lost. Fall back to PR body and comments.
- **Misleading commit messages.** "Small refactor" sometimes hides an intentional behavior change. Look at the diff, not the message.
- **Cargo-culted patterns.** The author may have copied a pattern without understanding why. Check if the pattern originated earlier in the codebase and investigate *that* commit.
- **Bot commits and auto-merges.** Dependabot, Renovate, and automated backports usually don't carry motivation. Skip them when trying to find intent.
- **Treating code as evidence of intent.** The code itself isn't evidence for why it exists. Evidence comes from commit messages, PRs, comments, tests, docs. Don't cite "the function is named X" as evidence of intent.

## What to return

Every commit/PR/comment that bears on the question, with:
- The exact text (quoted)
- The native revision or change identifier / review URL / file:line
- Author and date
- Whether it's direct (explicitly addresses the question) or circumstantial
