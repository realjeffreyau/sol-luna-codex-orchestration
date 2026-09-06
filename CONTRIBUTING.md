# Contributing

Thanks for helping improve Sol-Luna Codex Orchestration.

## Before you start

- Read README.md and the complete skill instructions in
  skills/orchestrate-sol-luna/SKILL.md.
- Search existing issues and pull requests before opening a new one.
- Keep each change focused on one behavior, documentation correction, test
  contract, or release concern.
- Never commit credentials, private workspace paths, user payloads, generated
  local state, or host configuration.
- Preserve the distinction between this package and the Codex host's own
  configuration, permissions, model catalog, and custom-agent inventory.

## Development workflow

1. Fork the repository and create a short-lived branch from main.
2. Make the smallest change that solves the problem.
3. Run python3 -m unittest discover -s tests -v.
4. Review the complete diff, including hidden community and workflow files.
5. Open a pull request with the reason for the change and the checks run.

The three supplied source files are release inputs. Do not hand-edit or
normalize them silently. An intentional source change should explain the
behavioral impact, update the relevant tests and changelog, and receive an
explicit versioning decision.

## Pull-request checklist

- [ ] The change is scoped and clearly described.
- [ ] Package tests pass.
- [ ] Documentation matches the actual package.
- [ ] No secrets, personal data, private paths, or machine-specific URLs were added.
- [ ] The one-Sol/one-Luna and no-delegation boundaries remain intact.
- [ ] Exact model and max-effort requirements remain explicit.
- [ ] The complete diff has been reviewed.

Use SECURITY.md for security-sensitive reports instead of posting details in a
public issue or pull request.
