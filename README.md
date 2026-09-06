# Sol-Luna Codex Orchestration

[![Validate](https://github.com/realjeffreyau/sol-luna-codex-orchestration/actions/workflows/validate.yml/badge.svg)](https://github.com/realjeffreyau/sol-luna-codex-orchestration/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A versioned Codex skill package for planning and implementing complex or
high-risk coding work with one Sol supervisor and one Luna implementation
worker.

> This is an unofficial community project. It is not affiliated with,
> endorsed by, or sponsored by OpenAI, Codex, GPT-5.6 Sol, GPT-5.6 Luna, or
> any model provider.

## Purpose

The skill keeps a difficult change bounded from discovery through acceptance:

- Sol inspects the real repository, resolves decisions, and creates a complete
  implementation packet.
- Luna is the only write-capable worker. It rereads named files, implements the
  packet, runs proportionate checks, and reports evidence.
- Sol reviews the actual diff and verifies the acceptance boundary instead of
  accepting a worker summary on its own.

The workflow is designed for cross-cutting changes, security-sensitive work,
release preparation, difficult debugging, and other tasks where a separate
planning and implementation boundary is useful.

## Architecture

| Role | Responsibility | Requested configuration |
| --- | --- | --- |
| Sol supervisor | Ground-truth discovery, decisions, packet construction, diff review, and acceptance verification | gpt-5.6-sol at the active high-or-stronger effort when available; lower-effort callers are routed through an xhigh supervisor |
| Luna worker | Implementation and tests after the packet is actionable | Custom agent luna_implementer with model gpt-5.6-luna and model reasoning effort max |

The contract is intentionally narrow: exactly one Sol supervisor and one Luna
worker participate in a run. Sol owns decisions. Luna alone performs repository
and global writes, and Luna must not delegate or spawn another agent.

The skill requires the host to select the requested model and effort exactly.
Model access is environment-dependent: the names gpt-5.6-sol and
gpt-5.6-luna identify the requested settings, not a promise that those models
are available in every Codex environment. If the requested configuration cannot
be selected, the workflow stops and reports the mismatch. There is no silent
model substitution or lowering of reasoning effort.

## The implementation packet

The packet passed from Sol to Luna preserves these labels in this exact order:

1. Objective
2. Acceptance criteria
3. Non-goals
4. Repository instructions
5. Current worktree constraints
6. Relevant files and symbols
7. Observed behavior and evidence
8. Implementation sequence
9. Interfaces and invariants to preserve
10. Required verification commands
11. Risks and edge cases
12. Expected worker report

Keeping every label makes constraints, evidence, and verification commands
survive the handoff without relying on an abbreviated summary.

## Compact and full modes

The skill applies an efficiency gate before choosing the amount of ceremony.

- Compact mode still uses the Sol/Luna split when the skill is explicitly
  invoked, but is appropriate for a clear, localized, low-risk change. It keeps
  the complete packet and performs the cheapest meaningful independent checks.
- Full mode is appropriate for ambiguity, interacting files or systems,
  architecture, authentication, security, data changes, difficult debugging,
  and release risk. It includes bounded discovery, complete evidence, actual
  diff review, and risk-critical verification.

After a local correction, only affected checks and required final sentinels are
rerun. A correction pass never authorizes an extra writer or a model change.

## Install

The skill and the Luna custom agent are separate artifacts. Install both into
the corresponding Codex locations:

    git clone https://github.com/realjeffreyau/sol-luna-codex-orchestration.git
    mkdir -p ~/.codex/skills ~/.codex/agents
    cp -R sol-luna-codex-orchestration/skills/orchestrate-sol-luna ~/.codex/skills/orchestrate-sol-luna
    cp sol-luna-codex-orchestration/skills/orchestrate-sol-luna/assets/agents/luna-implementer.toml ~/.codex/agents/luna-implementer.toml

Review an existing installed skill directory or
~/.codex/agents/luna-implementer.toml before updating it. Existing profiles
should be compared and reviewed rather than silently overwritten. A copied
skill directory does not install the custom agent, and copying the custom
agent does not install the skill.

Start a new Codex session, or reload the host's skill inventory if it caches
skill availability. Installation is deliberately ordinary file copying. This
package has no installer, package manager, daemon, telemetry, service, or
model-access mechanism. It does not grant permissions, bypass host
authorization, or change the default model. It does not modify
~/.codex/config.toml.

## Invoke

Invoke the skill directly or include it with the surrounding request:

    Use $orchestrate-sol-luna to implement this coding task.

    Use $orchestrate-sol-luna to plan and implement the requested change,
    preserving the repository constraints and reporting verification evidence.

The host should show the skill as available after installation. The exact
routing behavior still depends on the host's model catalog, custom-agent
support, authorization, and callable-tool context.

## Requirements

- A Codex or compatible host that can load skill directories.
- Custom-agent support for the luna_implementer profile when the full contract
  is required.
- Environment access to the requested Sol and Luna model identifiers, with Luna
  selectable at max reasoning effort. Availability is not universal and is
  not supplied by this repository.
- Python 3.10 or newer for the dependency-free package test command.

The skill itself has no runtime dependency. Python is used only for the
included validation tests; no Python package needs to be installed.

## Validate locally

From the repository root, run the same package test used by CI:

    python3 -m unittest discover -s tests -v

For a working-tree review, also run:

    git diff --check

The package tests cover:

- skill frontmatter and the required packet-label order;
- the packaged Luna name, model, max effort, and no-delegation instruction;
- the packaged interface metadata and byte-stable source snapshots;
- release version consistency and the documented safety boundaries;
- the complete public package layout; and
- read-only GitHub Actions configuration.

## Security boundaries and limitations

This repository publishes instructions and configuration metadata. It does not
run an orchestration service, store task state, handle credentials, grant
permissions, or make unavailable tools callable. The host remains responsible
for authentication, authorization, filesystem access, model access, and any
external side effects.

Do not place credentials, tokens, private workspace contents, or sensitive task
payloads in issues or pull requests. Review the skill and the custom-agent
profile before installing them. The workflow must stop on a model or effort
mismatch; it must not silently substitute another model. The one-worker
boundary is a safety and review contract, not a general-purpose multi-agent
runtime.

The package does not claim that gpt-5.6-sol, gpt-5.6-luna, custom agents, or
multi-agent support are publicly available in every environment. It documents
the behavior requested by this release and leaves capability checks to the
host.

## Troubleshooting

Skill not listed after installation:

1. Confirm the directory contains
   skills/orchestrate-sol-luna/SKILL.md and
   skills/orchestrate-sol-luna/agents/openai.yaml.
2. Start a new session or reload the host's skill inventory.
3. Check that the host recognizes the directory as a skill root.

The Luna worker cannot be selected:

1. Confirm the separate custom-agent file is installed at
   ~/.codex/agents/luna-implementer.toml.
2. Review that its name is luna_implementer, its model is gpt-5.6-luna, and
   its model reasoning effort is max.
3. Check the host's custom-agent support and model catalog. Do not replace the
   requested model with an unverified alternative.

An existing profile differs:

Compare the existing file with the profile shipped in this repository, decide
which version is authorized for the environment, and make the update manually.
The installation instructions never assume that an existing profile may be
overwritten.

Validation fails:

Run python3 -m unittest discover -s tests -v from the repository root and read
the first failing contract. The tests are standard-library only, so a failure
normally indicates a package layout, metadata, or source-integrity problem.

## Version and license

The current public release is 0.1.0. See CHANGELOG.md for the release notes,
LICENSE for the MIT terms, and NOTICE.md for provenance and non-affiliation
notices.

## Contributing and security reports

Keep changes focused and preserve the distinction between the skill package,
the custom agent, and host-managed configuration. See CONTRIBUTING.md before
opening a pull request. Report security concerns according to SECURITY.md and
do not disclose sensitive material publicly.
