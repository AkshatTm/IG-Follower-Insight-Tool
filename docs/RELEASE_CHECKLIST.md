# Release Checklist

## Pre-Release

- Confirm roadmap scope for this release is frozen.
- Verify changelog entry is updated.
- Validate documentation links and commands.

## Quality Gates

- Run static error checks across project.
- Run parser and persistence validation tests.
- Perform manual 4-screen UX regression pass.
- Verify export outputs (TXT, CSV, clipboard) match expected format.

## Security and Privacy Checks

- Ensure no personal Instagram export files are committed.
- Confirm no secrets or credentials are introduced.
- Re-check `.gitignore` coverage for local artifacts.

## Packaging and Tagging

- Build release artifact (if distributing executable).
- Tag release version in git.
- Publish release notes with feature and fix summary.

## Post-Release

- Monitor issues and user feedback.
- Triage bug reports into next milestone.
- Capture lessons learned into roadmap updates.