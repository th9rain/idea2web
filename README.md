# idea2web

[English](README.md) | [简体中文](README.zh-CN.md)

> Turn a rough product idea into a practical full-stack web app scaffold.

`idea2web` is a reusable skill and CLI workflow for taking a short product prompt, turning it into a structured build plan, and generating a usable starter application.

It is aimed at the gap between "I have an idea" and "I have something concrete I can run, inspect, and extend."

## What it does

From a short request such as:
- "Build an internal dashboard"
- "Create a CRUD tool for task tracking"
- "Generate a small operations app for approvals"

`idea2web` helps produce:
- structured requirement clarification
- a lightweight PRD
- architecture and API planning
- full-stack project scaffolding
- startup and delivery guidance

## Default stack

The current template path is optimized for a practical default stack:
- React + Vite
- FastAPI
- SQLite
- Tailwind CSS

The repository is organized so the workflow can evolve toward additional stacks later, but the current public path is intentionally narrow and usable.

## Workflow

`idea2web` follows four stages:

1. **Requirement clarification**
   - extract entities, operations, and constraints
   - surface missing assumptions
   - produce a structured PRD

2. **Architecture planning**
   - choose a stack
   - shape the data model and API
   - produce an implementation plan and file tree

3. **Code generation**
   - generate backend, frontend, config, and seed assets
   - render project templates into a runnable scaffold

4. **Delivery**
   - provide startup scripts
   - provide beginner-friendly usage guidance

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate a project in one shot:

```bash
python -m scripts quick --user-input "Build an internal task dashboard" --output-dir ./my-app
```

Run the staged flow manually:

```bash
python scripts/generator.py analyze --user-input "Build an internal task dashboard" --output prd.json
python scripts/generator.py plan --prd prd.json --output architecture.json
python scripts/generator.py generate --architecture architecture.json --output-dir ./my-app
```

## Repository structure

```text
idea2web/
|-- README.md
|-- LICENSE
|-- SKILL.md
|-- requirements.txt
|-- config/
|-- evals/
|-- references/
|-- scripts/
`-- templates/
```

## Key files

- `SKILL.md` - reusable skill definition for product-to-build workflows
- `scripts/` - CLI entrypoints and generation pipeline
- `templates/react-fastapi/` - concrete scaffold for the current default stack
- `config/` - generation defaults, ordering, and stack metadata
- `references/` - implementation notes, deployment guidance, and generation rules
- `evals/` - evaluation cases for checking workflow quality

## What this repo is not

This repo is not:
- a finished no-code product builder
- a generic website generator for every framework
- a polished SaaS platform

It is a practical starting point for repeatable "idea to runnable app" generation workflows.

## Why this repo exists

A lot of product ideas die before they become a usable first version.

`idea2web` exists to compress that gap:
- turn vague requests into structured requirements
- turn structure into implementation decisions
- turn decisions into a starter codebase that can actually be extended

## Current limitations

Right now, the strongest path in this repo is the React + FastAPI scaffold. That is deliberate.

It is better for a public repository to have one clear, reusable path than to pretend to support every stack equally well.

## Suggested GitHub metadata

**Repository description**

> Turn product ideas into practical full-stack web app scaffolds.

**Suggested topics**

```text
code-generation
full-stack
app-generator
fastapi
react
vite
tailwindcss
developer-tools
workflow-automation
```

## Related themes

- reusable skills
- AI workflow systems
- product-to-build automation
- practical full-stack generation

## License

MIT
