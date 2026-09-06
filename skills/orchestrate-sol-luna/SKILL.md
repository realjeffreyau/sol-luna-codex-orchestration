---
name: orchestrate-sol-luna
description: Orchestrate complex or high-risk coding changes with GPT-5.6 Sol for repository analysis, planning, delegation, review, and acceptance while GPT-5.6 Luna at max reasoning performs implementation and tests. Accept invocation from Sol at any reasoning effort, reusing active high-or-stronger Sol sessions and upgrading lower-effort callers to an xhigh supervisor. Use when the user explicitly requests Sol/Luna orchestration, a planner/implementer model split, or this skill by name for a coding change.
---

# Orchestrate Sol and Luna

Use one `gpt-5.6-sol` supervisor and one `gpt-5.6-luna` worker at `max` reasoning.
Sol owns decisions; Luna alone performs repository and global writes. Preserve
the user's requested mode, authorization, and safety boundaries.

## Enforce the model contract

1. Require `model="gpt-5.6-sol"` for the supervisor, reusing an active Sol
   effort of `high`, `xhigh`, `max`, or `ultra`; otherwise spawn Sol at `xhigh`.
   Require the implementer profile `model="gpt-5.6-luna"` and
   `reasoning_effort="max"`.
2. Never reject a Sol `low` or `medium` caller; route it through one spawned
   Sol `xhigh` supervisor. A non-Sol caller also spawns that supervisor.
3. Use the installed `luna_implementer` custom agent for Luna. Use exact direct
   model overrides only when callable and custom-agent selection is unavailable.
4. Require every spawned agent to verify its active model and effort before any
   write. Never silently substitute a model or lower effort; stop and name the
   unavailable configuration, offering a fallback only as an explicit choice.
5. Do not use this workflow for read-only questions or reviews unless explicitly
   requested; the handoff is otherwise unnecessary.

## Apply the efficiency gate and split modes

Use split orchestration only when its planning quality is justified. Historical
evidence (not a new benchmark) measured a tiny fixture at about 106 seconds with
the split versus 35 seconds with Luna alone, so avoid ceremony for routine work.

Classify after the gate:

- **Default bypass:** when the user has not explicitly invoked Sol/Luna, a clear
  localized low-risk task (roughly one or two small files or one bounded
  subsystem) with straightforward reversible behavior and no material
  trust/data/release risk uses the normal single-agent workflow.
- **Compact split:** an explicit Sol/Luna invocation always honors the split,
  but uses compact mode for that same clear localized low-risk shape. Explicit
  invocation forces the split; it does not force full ceremony.
- **Full split:** use for ambiguity, cross-cutting or interacting files/systems,
  architecture/API/schema/auth/security/data migration/behavioral migration or
  release risk, difficult debugging, or any materially uncertain classification.

## Route exactly one supervisor

- Reuse an active Sol at `high`, `xhigh`, `max`, or `ultra`; do not spawn a
  redundant supervisor or duplicate its exploration/review.
- If the caller is Sol at `low`/`medium` or is not Sol, spawn exactly one
  `sol_supervisor` with `model="gpt-5.6-sol"`, `reasoning_effort="xhigh"`, and
  `fork_turns="none"`. Give it a complete self-contained brief; do not rely on
  inherited context.
- The primary waits for that supervisor rather than exploring the same paths.
  Do not spawn extra supervisors or auxiliary agents; the single Luna
  implementer described below is the only additional agent.

## Bound discovery and build the packet

Sol batches independent read-only checks, reuses supplied/current evidence, and
does not reread unchanged skills, source, or instructions. Stop discovery when
the exact targets, interfaces, invariants, dirty-state constraints, and focused
tests are known; do not map unrelated code. Start Luna once the packet is
actionable.

Before planning, inspect actual `AGENTS.md`/repository instructions, version
control state, relevant code/tests/interfaces, and the smallest checks covering
the change. Resolve material ambiguity from evidence and distinguish evidence
from inference. Do not edit implementation files.

Pass Luna this complete, compact packet with every label shown:

```text
Objective
Acceptance criteria
Non-goals
Repository instructions
Current worktree constraints
Relevant files and symbols
Observed behavior and evidence
Implementation sequence
Interfaces and invariants to preserve
Required verification commands
Risks and edge cases
Expected worker report
```

In compact mode, genuinely empty values may be literal `None` and other values
may be one-line, but every label remains present. Never omit a criterion,
constraint, safety boundary, or unresolved uncertainty; use exact paths, symbols,
commands, and distilled evidence rather than raw logs.

## Delegate implementation to Luna

Select the `luna_implementer` custom agent with the packet, `fork_turns="none"`,
and no direct model/effort override unless custom selection is unavailable.
Tell Luna to reread named files canonically, preserve unrelated changes, make the
smallest coherent change, batch independent reads/checks, run focused checks
before broad suites, and stop on a material blocker instead of guessing. Luna
must report changed files, decisions, commands/outcomes, and unresolved risks;
the profile's model verification happens before writes. Luna is the only writer.

## Verify and correct by mode

Always inspect the real diff/state and check every criterion, invariant, user
constraint, and required acceptance boundary; never accept a summary alone.

- **Compact:** independently run the cheapest meaningful sentinel(s), validate
  worker-reported broader results against real artifacts, and avoid duplicating
  an unchanged passing suite.
- **Full:** independently rerun risk-critical commands and validate the other
  worker results against actual artifacts.
- **Correction:** use the same Luna worker, send concrete file/symbol failures,
  allow at most two targeted passes, and rerun affected checks plus required
  final sentinels—not unrelated unchanged checks. Continue only with clear
  progress; Sol never takes over implementation.

Return only after acceptance or a concrete blocker. Do not claim completion when
checks failed, were skipped without explanation, or criteria remain unmet.

## Control coordination cost

Use brief plans/reviews in compact mode and full analysis only for full mode.
While delegated work is healthy, wait in 45–55-second intervals and report only
real milestones or meaningful stalls; still send commentary often enough not to
leave the user without an update for about 60 seconds. Keep noisy worker output
in its thread and return distilled evidence. Preserve the full packet and all
safety/acceptance standards while reducing redundant coordination.
