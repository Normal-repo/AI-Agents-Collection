# AI Agents Collection

Project workspace for experimenting with small AI agents. This repository contains one agent implementation in `web-research-agent` that performs web search and generates a structured research report using a language model.

## Repository Structure

- `web-research-agent/` - Web research agent source, `agent.py`, `requirements.txt`, and README for the agent.
- `.venv/` (recommended) - Virtual environment (not committed).
- `.gitignore` - Project git ignore rules.

## Prerequisites

- Python 3.11 installed on your system.
- (Optional) Git for version control.

## Quickstart

1. From the project root, create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Or on Unix/macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install the agent dependencies:

```powershell
pip install -r web-research-agent\requirements.txt
```

3. Create a `.env` file in `web-research-agent/` with any required API keys (for example):

```
GROQ_API_KEY=api_key_here
```

4. Run the web research agent:

```powershell
python web-research-agent\agent.py --query "latest advances in AI agents 2024"
```

## Development Notes

- The agent expects third-party packages listed in `web-research-agent/requirements.txt`.
- Select the `.venv` interpreter in VS Code for linting and IntelliSense.
- If you add files that should be ignored, update `.gitignore`.

## Contributing

PRs and issues are welcome. Keep changes focused and add tests where appropriate.

## License

This repository does not include a license file. Add a `LICENSE` if you want to open-source this project.
