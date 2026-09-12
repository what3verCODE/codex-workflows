---
name: verify-this
description: "Verify a behavior or performance claim with comparable baseline and changed-state evidence, returning VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Use when a fix, speedup, or observable result needs proof."
---

# Verify This

Verification is not a recap. It proves or disproves a specific claim with repeatable evidence.

## When To Use

- The user asks "verify this", "prove it works", "did this fix it", or "show me the evidence".
- A bug fix needs a before/after repro.
- A UI, CLI, API, performance, or memory claim needs measurement.
- A test passes but the user-visible behavior still needs confirmation.

Translate the requested outcome into an observable claim using the task's existing acceptance criteria. Ask only when the intended result remains unclear. Subjective claims such as "the code is cleaner" belong in design review.

## Workflow

1. Restate the claim in falsifiable form: condition, metric, and threshold.
2. Pick the smallest local surface that can disprove it.
3. Capture a baseline from the old state: a fixed earlier revision, saved file snapshot, recorded failing state, or current broken repro.
4. Capture treatment from the changed state with the same command, data, warmup, and environment.
5. Compare raw artifacts: numbers, screenshots, terminal transcripts, HTTP responses, profiles, heap snapshots, or test output.
6. Return exactly one verdict: `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

Reuse current task artifacts when their revisions, commands, data and environment establish the comparison. Preserve the active working tree; run the old state in an isolated baseline when available. If a comparable baseline cannot be obtained, report INCONCLUSIVE rather than treating a passing current-state check as comparative proof. Verification produces evidence; corrections follow the existing task scope.

## Local Surfaces

- Code behavior: focused unit/integration tests or a minimal repro script.
- CLI/TUI behavior: the project's terminal harness, PTY tools, transcript, or demo recording.
- UI behavior: the project's browser harness, screenshots, accessibility snapshots, or browser traces.
- API behavior: local HTTP/RPC request and response diff.
- Performance: same-machine baseline/treatment timings or CPU profiles.
- Memory: heap snapshots before and after the suspected operation.

## Artifact Layout

When safe to write artifacts:

```text
/tmp/verify-this/<claim-slug>/
├── claim.md
├── timeline.md
├── baseline/
├── treatment/
├── diff/
└── verdict.md
```

Use a unique task directory and retain only the evidence needed for the claim. Follow existing workspace rules and user authorization for artifacts that contain sensitive data; redact secrets. Reuse authorized artifact storage without repeating approval requests.

## Verdict Rules

- `VERIFIED`: baseline and treatment differ in the predicted direction, by the claimed threshold, with no obvious confound.
- `NOT VERIFIED`: the behavior is unchanged, moves the wrong way, or misses the threshold.
- `INCONCLUSIVE`: no valid baseline, noisy signal, failed measurement, or an environment difference invalidates the comparison.

## Output

Use this shape:

```text
VERIFIED | NOT VERIFIED | INCONCLUSIVE
Claim: <falsifiable claim>

Evidence:
<metric/artifact>: baseline=<...>, treatment=<...>, delta=<...>, threshold=<...>

Reasoning:
<one tight paragraph naming the evidence and any confounds>
```

Do not soften a negative result. A clear `NOT VERIFIED` is useful.
