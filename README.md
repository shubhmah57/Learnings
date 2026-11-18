# Artificial Intelligence Learnings

This repository contains hands-on Python exercises and small applications developed while learning modern AI and agent frameworks. The examples cover LLM integrations, tool use, agent workflows, retrieval and document handling, memory, and Model Context Protocol (MCP).

## What is covered

- **OpenAI Agents SDK** — agents, guardrails, structured outputs, multi-agent orchestration, evaluator/aggregator workflows, and web research.
- **Document analysis** — a Gradio chat interface for asking questions about documents, with response evaluation examples.
- **LangChain and LangGraph** — tool calling, graph-based conversations, checkpointing, human-in-the-loop workflows, and MCP adapters.
- **Model Context Protocol** — MCP clients and servers, including an expense-management example and long-term memory experiments.
- **Other practice projects** — command-line chatbot and Kubernetes pod-status/tool-calling examples.
- **Shared utilities** — model configuration and helpers for PDF reading and OpenAI client setup.

The code is organized as learning exercises; individual scripts may require different API keys, services, or configuration.

## Project layout

| Path | Contents |
| --- | --- |
| `openaiagentsframework/` | OpenAI Agents SDK examples, document analyzer, structured outputs, and agent patterns |
| `langchain/` | LangChain and LangGraph exercises, including human-in-the-loop and tool workflows |
| `modelcontextprotocol/` | MCP clients, servers, expense management, and memory experiments |
| `generalpractice/` | Command-line chatbot and Kubernetes-related practice |
| `utils/` | Shared model configuration and helper functions |
| `main.py` | Gradio entry point for the document analyzer |

## Requirements and setup

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- API credentials for the model or external services used by the example you want to run

From the repository root in PowerShell:

```powershell
uv sync
Copy-Item .env.example .env
```

Add your own credentials to `.env` as needed. Never commit `.env` or paste real API keys into source files. The example environment file lists the current configuration variables; some exercises may need additional provider-specific packages or services.

Run the document analyzer:

```powershell
uv run python main.py
```

Other exercises are separate scripts under their respective folders. Check each script for its required environment variables and services before running it.

## Pushing changes to GitHub

This working copy is already a Git repository with an `origin` remote configured. From the repository root in PowerShell:

```powershell
git status --short
git remote -v
```

Review the changes and ensure you do not publish `.env`, credentials, local databases, logs, or personal documents. Stage only the files you intend to publish (do not use `git add .` without reviewing everything):

```powershell
git add README.md
# Stage any other intended files by path, for example:
# git add openaiagentsframework/
git diff --cached
git commit -m "Update project README and examples"
git push -u origin main
```

If GitHub requests authentication, sign in through Git Credential Manager or use GitHub CLI (`gh auth login`). If the push is rejected because the remote has commits not present locally, fetch and reconcile those commits before retrying; do not force-push unless you explicitly intend to overwrite remote history.
