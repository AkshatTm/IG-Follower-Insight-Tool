# Instagram Red Flags

Instagram Red Flags is a modern desktop application built with Python and CustomTkinter to analyze Instagram connection exports, identify non-followers, filter VIP accounts, and export action-ready lists.

This repository is also a prompt-engineering showcase project that demonstrates how multiple AI systems can be orchestrated across planning, implementation, testing, and finalization.

## AI Build Attribution (Showcase)

This project was developed through a human-led, AI-assisted workflow:

| Phase | Tooling | Model | Responsibility |
| --- | --- | --- | --- |
| Planning | Antigravity | Opus 4.6 | Product framing, module breakdown, implementation plans |
| Execution | GitHub Copilot | Sonnet 4.6 | Core feature implementation and iteration |
| Testing and Debugging | Jules | Gemini 3.1 Pro | Validation, debugging, and quality checks |
| Final Hardening and Documentation | GitHub Copilot | GPT-5.3-Codex | Requirement alignment, fixes, and production-style docs |

Human ownership remained central throughout: final decisions, acceptance criteria, and repository stewardship are all maintained by the project author.

## Core Features

- Upload Instagram export files (`followers_1.json` and `following.json`)
- Robust JSON parsing for multiple Instagram export structures
- Quick analysis summary with non-follower count
- Deep Scan module for VIP whitelisting (`whitelist.json` persistence)
- Export options:
	- Text export from quick analysis
	- CSV export from filtered final list
	- Clipboard copy for clean username lists
- Restart flow to rerun analysis without restarting the app

## Tech Stack

- Python 3.10+
- CustomTkinter 5.2+
- Standard library modules: `json`, `csv`, `os`, `webbrowser`, `tkinter.filedialog`

## Project Structure

```text
.
|-- main.py
|-- requirements.txt
|-- src/
|   |-- app.py
|   |-- parser.py
|   |-- whitelist.py
|   |-- components.py
|   |-- theme.py
|   `-- screens/
|       |-- screen_upload.py
|       |-- screen_results.py
|       |-- screen_filter.py
|       `-- screen_export.py
|-- docs/
|   |-- Module 1.md
|   |-- Module 2.md
|   |-- PROJECT_SHOWCASE.md
|   |-- AI_WORKFLOW.md
|   |-- ARCHITECTURE.md
|   |-- TESTING.md
|   |-- ROADMAP.md
|   `-- RELEASE_CHECKLIST.md
`-- test_data/
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AkshatTm/IG-Follower-Insight-Tool.git
cd IG-Follower-Insight-Tool
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

## Usage Flow

1. Open the app and follow the instructions to download Instagram JSON exports.
2. Upload `followers_1.json` and `following.json`.
3. Run quick analysis to view non-follower insights.
4. Open Deep Scan to whitelist VIP accounts you want to keep following.
5. Export the final clean list as CSV or copy it to your clipboard.

## Data Privacy

- All analysis is local on your machine.
- No external API calls are required for parsing and filtering.
- Keep your Instagram export files private and avoid committing personal data.

## Documentation Index

- Showcase summary: [docs/PROJECT_SHOWCASE.md](docs/PROJECT_SHOWCASE.md)
- AI development workflow: [docs/AI_WORKFLOW.md](docs/AI_WORKFLOW.md)
- Technical architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Testing strategy: [docs/TESTING.md](docs/TESTING.md)
- Product roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- Release checklist: [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md)

## Project Status

Current status: Active and showcase-ready, with iterative hardening planned via roadmap milestones.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening issues or pull requests.

## License

This project is licensed under the terms in [LICENSE](LICENSE).

