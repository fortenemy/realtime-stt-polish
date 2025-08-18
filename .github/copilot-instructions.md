<!-- .github/copilot-instructions.md
     Auto-generated guidance for AI coding agents working in this repository.
     Keep concise and actionable — update when the project gains real source files.
-->

# Copilot instructions for this repository

Short purpose
- This repository currently contains only a brief project note (`CLAUDE.md`) and an MCP log (`mcp-shell.log`). Use these files first to understand the environment and any MCP-related issues before making changes.

What to inspect first (high-value files)
- `CLAUDE.md` — summary of repository state (empty/new). Read for platform notes (Windows) and hints.
- `mcp-shell.log` — runtime log for the MCP Shell Server; it contains actionable errors (example: ENOENT on `D:\ClaudeMCP\Desktop`).

Big-picture (current state)
- No source code or build manifests detected (no `package.json`, `requirements.txt`, `pyproject.toml`). The repo appears to be an initialized workspace used for MCP experiments.
- Platform: Windows. There may be a Python virtualenv `.venv` present in terminals; confirm before running Python commands.

Project-specific patterns & integration points
- MCP (Model Context Protocol) is present in logs: the server may start local Node processes and expect filesystem roots. Example failure to note and search for:
  - "Error: ENOENT: no such file or directory, stat 'D:\\ClaudeMCP\\Desktop'"
  - Server stack: `.../@modelcontextprotocol/server-filesystem/dist/index.js`
- Agents should look for: hardcoded absolute paths in logs/configs, local extension hosts, and Node-based server files referenced by MCP logs.

Developer workflows (how an agent should probe the repo)
- Search for typical project files: `package.json`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Makefile`.
- If none found, ask the user what language/framework they intend to use before creating files.
- To reproduce MCP errors locally, examine `mcp-shell.log` entries and confirm any referenced filesystem paths exist (create them only if the user permits).

Safe-action rules for AI agents (explicit)
- Do not add or modify source files without the user's approval. Small infra fixes (e.g., creating a missing directory reported in logs) are acceptable if the user explicitly consents.
- When diagnosing: prefer read-only operations (file reads, searches) and present findings before making changes.

Immediate tasks an agent can run now
- Read `CLAUDE.md` and `mcp-shell.log` (already present). Quote exact log lines when reporting issues.
- Run a workspace search for common manifests and MCP-related files.

Questions to ask the user before changing the repo
- What language/framework will this project use? (Python/Node/other)
- May I create missing directories referenced in logs (example path above)?
- Should I initialize a package manifest (`package.json`/`requirements.txt`) once the language is chosen?

If you want an expanded version later
- When source files appear, regenerate this doc and include: build/test commands, lint/typecheck steps, key modules and dataflow diagrams, and examples of common edits.
