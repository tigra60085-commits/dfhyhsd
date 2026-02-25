# CLAUDE.md

This file provides guidance to AI assistants (Claude Code and similar) working in this repository.

## Repository Overview

This is a newly initialized web project repository. As of February 2026, the repository is in its early bootstrapping phase with no application source code committed yet.

**Current state:**
- `.gitkeep` — placeholder to track the empty root directory in git
- `.vscode/launch.json` — VS Code Chrome debugger configuration targeting `http://localhost:8080`

## Development Environment

### VS Code Debug Configuration

The repository includes a VS Code launch configuration (`.vscode/launch.json`) for debugging against a local development server:

- **Type:** Chrome browser debug session
- **URL:** `http://localhost:8080`
- **Web root:** workspace root (`${workspaceFolder}`)

To use it: start your local development server on port 8080, then run the "Launch Chrome against localhost" debug configuration in VS Code (F5).

## Git Workflow

### Branches

- `main` — primary integration branch (hosted on `origin`)
- `master` — local default branch
- Feature and AI-assisted work branches follow the pattern: `claude/<description>-<session-id>`

### Commit Conventions

Use clear, imperative commit messages describing what the commit does:
```
Add user authentication module
Fix null pointer in order processing
Update README with setup instructions
```

### Pushing Changes

Always push with tracking set:
```bash
git push -u origin <branch-name>
```

## Conventions for AI Assistants

1. **No source code yet** — do not assume any framework, language, or build system is in place. Ask or infer from context when development begins.
2. **Port 8080** — the development server is expected on port 8080 based on the VS Code debug config.
3. **Workspace root** — the web root is the repository root (`/`); keep this in mind when placing source files.
4. **Branch targeting** — all AI-assisted changes must be committed and pushed to the designated feature branch (never directly to `main` or `master`).
5. **Minimal footprint** — avoid creating files that aren't directly required. Prefer editing existing files over creating new ones.
6. **Security** — do not introduce OWASP top-10 vulnerabilities; validate at system boundaries (user input, external APIs).

## Future Setup Checklist

When the project tech stack is decided, update this file to include:
- [ ] Language / framework and version
- [ ] Package manager and install command (`npm install`, `pip install -r requirements.txt`, etc.)
- [ ] Build command
- [ ] Test command and test runner
- [ ] Lint / format command
- [ ] Environment variable requirements (`.env.example`)
- [ ] Deployment instructions
