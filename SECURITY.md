# Security policy

## Scope

This repository is a local guidance and configuration package. It does not
operate a hosted service, store application data, manage credentials, grant
permissions, or provide model access. The host environment remains responsible
for authorization, filesystem access, model selection, and external side
effects.

The package includes a custom-agent profile for a specific requested model and
reasoning effort. Model availability is environment-dependent. A host that
cannot select the requested configuration should report the mismatch rather
than silently substituting another model or effort.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting or Security Advisories for this
repository when available:

    https://github.com/realjeffreyau/sol-luna-codex-orchestration/security/advisories/new

If private reporting is unavailable, open a minimal public issue without
exploit details or sensitive data and request a private reporting channel. Do
not publish credentials, tokens, personal data, private workspace paths, or
complete exploit instructions in a public issue.

## Release hygiene

Before contributing or publishing:

- scan current tracked files and reachable history for secrets, private paths,
  personal data, placeholders, and incorrect attribution;
- review the complete diff and package layout;
- run the dependency-free tests and read-only CI checks; and
- review any host configuration before installing the separate custom-agent
  profile.
