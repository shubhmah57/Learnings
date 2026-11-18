# Artificial Intelligence Learnings

Python exercises and small projects exploring:

- OpenAI agents, structured outputs, and multi-agent workflows
- LangChain and LangGraph tools, memory, and human-in-the-loop flows
- MCP clients and servers
- Document analysis and web search

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
Copy-Item .env.example .env
uv run python main.py
```

Add required API keys to `.env`. Never commit credentials.
