# Web Research Agent

A small research agent that searches the web and produces a structured research report using a language model.

## Setup

1. Create and activate a Python 3.11 virtual environment (from project root):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r web-research-agent\requirements.txt
```

3. Create a `.env` file in the `web-research-agent` folder and add any required API keys (example):

```
OPENAI_API_KEY=your_key_here
```

## Usage

Run the agent from the project root:

```powershell
python web-research-agent\agent.py --query "your research query"
```

## Notes

- The code expects several third-party packages listed in `requirements.txt`.
- If you created `.venv` at the workspace root, select it as the VS Code interpreter for proper linting and IntelliSense.