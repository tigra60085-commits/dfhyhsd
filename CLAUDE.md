# CLAUDE.md

This file provides guidance to AI assistants (Claude Code and similar) working in this repository.

## Repository Overview

A Vanilla JS / HTML / CSS Todo application with `localStorage` persistence. No build tools or frameworks — static files served directly.

**File structure:**
```
index.html          — entry point
css/style.css       — all styles (CSS custom properties, flexbox)
js/app.js           — all application logic
.vscode/launch.json — VS Code Chrome debug config (port 8080)
```

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

## Tech Stack

| Area | Choice |
|---|---|
| Language | Vanilla JavaScript (ES2020+, `'use strict'`) |
| Markup | HTML5 |
| Styles | CSS3 with custom properties |
| Build | None — static files, no bundler |
| Package manager | None |
| Tests | None yet |
| Lint | None yet |

## Running Locally

Serve the repository root on port 8080 (matching the VS Code debug config):

```bash
# Option A — Node.js serve
npx serve . -p 8080

# Option B — Python
python3 -m http.server 8080
```

Then open `http://localhost:8080` or press F5 in VS Code (Chrome debugger).

## Application Architecture

All state lives in `js/app.js`:
- `todos` — in-memory array of `{ id, text, completed }`
- `currentFilter` — `'all' | 'active' | 'completed'`

Persistence: `localStorage` key `"todos"` (JSON). Read once on load (`loadTodos`), written after every mutation (`saveTodos`).

Rendering is a full re-render on every mutation (`render()`). No virtual DOM.

## Conventions for AI Assistants

1. **No framework** — keep everything in plain JS/HTML/CSS; do not introduce npm, bundlers, or frameworks without discussion.
2. **Port 8080** — development server runs on port 8080.
3. **Workspace root** — `index.html` is at the repo root; `css/` and `js/` are subdirectories.
4. **Branch targeting** — commit and push to the designated `claude/…` feature branch; never directly to `main` or `master`.
5. **Minimal footprint** — prefer editing existing files over creating new ones.
6. **Security** — sanitize any user-supplied text before DOM insertion (use `textContent`, not `innerHTML`).
