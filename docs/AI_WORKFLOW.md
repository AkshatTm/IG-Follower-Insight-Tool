# AI Workflow and Model Roles

## Purpose

This document captures how AI tools were used in this project, what each model was responsible for, and how quality and ownership were controlled.

## Multi-Model Delivery Strategy

The project used specialized models for distinct phases rather than relying on a single model for all tasks.

| Phase | Tool | Model | Primary Output |
| --- | --- | --- | --- |
| Planning | Antigravity | Opus 4.6 | Module plans, screen flow, requirement decomposition |
| Execution | GitHub Copilot | Sonnet 4.6 | Implementation of screens, parser, and state flow |
| Testing and Debugging | Jules | Gemini 3.1 Pro | Test scenarios, defect identification, debugging loops |
| Finalization | GitHub Copilot | GPT-5.3-Codex | Requirement-gap fixes, documentation, release polish |

## Prompting Approach

1. Product prompts defined desired user experience and constraints.
2. Module prompts defined implementation boundaries and output structure.
3. Debug prompts focused on observed failures and expected behavior.
4. Finalization prompts focused on readiness, clarity, and maintainability.

## Quality Gates

To maintain reliability in AI-assisted coding, the following gates were applied:

- Requirement traceability against module specs
- Static error checks before and after code edits
- Runtime validation of parser and persistence behavior
- Manual UX verification across all screens
- Documentation completeness for handoff and long-term maintenance

## Ownership and Accountability

AI provided acceleration, not autonomous ownership.

- The repository author owns final architecture and scope decisions.
- Model outputs are reviewed before acceptance.
- Security, privacy, and data handling decisions are human-approved.

## Reproducibility Notes

To reproduce this workflow in future projects:

1. Define model roles before coding starts.
2. Keep module prompts versioned in the repo.
3. Require validation evidence for every accepted change.
4. Reserve final pass for consistency, docs, and release standards.