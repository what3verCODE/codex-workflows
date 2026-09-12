# Source specification and documentation review

No actionable findings in the assigned categories. No blocking implementation defects identified by this review. This does not close the unverified acceptance checks recorded in `docs/validation.md`.

Comparison is `/home/alexandr/projects/codex-workflow`, original baseline `bdef69b`, fixed checkpoint `5b0e0e838c6623ad31807a2452650f7dbee9a438`. Reviewed the complete change, not a repair-only range. HEAD was the supplied checkpoint and the working tree was clean before and after inspection. Final `git diff --quiet 5b0e0e838c6623ad31807a2452650f7dbee9a438` exited zero. No repository edits, publication or child agents.

## Evidence considered

- Issue bodies and comments from `/tmp/codex-workflow-issues.json`, the portable-workflow specification, and supplied steering about Make management and retaining upstream defaults.
- Make targets, README, provenance, manifest, installation/validation/smoke/upstream-comparison/fixture scripts and installer integration tests.
- All role instructions, original workflow skills, maintained fork instructions and upstream comparison output. Prior reads covered TDD references, agent-writing references and the documentation evaluation records.
- Validation and behavioral reports, including their explicit limits on macOS, native roles, live tracker/MCP, non-Git VCS, fresh specialist contexts and human clarification resumption.

The Make commands expose installation, authoritative updates, checks, runtime discovery, fixtures, upstream comparison and invocation. Documentation correctly distinguishes source updates from fetching a newer repository revision. Manifest ownership and replacement semantics preserve unrelated installed material; the instructions keep task state and review counts in conversation context. Workflow instructions specify original-baseline reviews, documentation-only routing, independent review, evidence reuse, existing-edit handling and the two-round stop.

Executed `make diff-upstream UPSTREAM_CHECKOUT=/tmp/workflow-matt-skills` against the pinned upstream commit. Also compared every original upstream file through `git show` and checked every local fork's `upstream.json` against its manifest origin. All metadata records agreed. Changed upstream files were only `SKILL.md` for TDD, diagnosis, review, to-spec and to-tickets, and `SKILL-MECHANICS.md` for writing-for-agents. All existing supporting files and upstream UI metadata matched byte-for-byte. The to-spec/to-tickets explicit-invocation policies therefore remain preserved. Review's extracted smell reference and attribution records are additional local files. The observed differences match the documented workflow/Codex adaptations; no extra editorial rewrite was found.

The restored extensive-story wording and diagnosis minimization requirement are upstream choices explicitly retained by user steering. Historical evaluation comments criticizing their proportionality do not constitute current defects or authorization to rewrite them. The documentation labels those reports historical and records the later upstream audit.

## Coverage and limits

Specification and documentation were reviewed. Other technical/standards categories belong to the other assigned specialist and coordinator. No new runtime discovery or installer tests were run in this read-only source review; existing test code and recorded outcomes were inspected. No network sources were required for the provenance comparison because the pinned Git objects were available locally. Upstream standard-library implementation internals were not read.

This reviewer previously evaluated disposable preparation fixtures, but did not implement this source change. The source review used the fixed final files and supplied requirements directly. Environmental and behavioral validation gaps are candidly documented and remain acceptance limits, rather than being presented as source defects or silently treated as passing checks.
