# idea2web

A real reusable skill for generating full-stack web applications from a one-line idea.

## What it is

`idea2web` is a packaged skill that turns a vague product idea into a practical full-stack web app scaffold.

It is not just a concept note or a prompt draft. It is an actual skill with workflow instructions, templates, scripts, config, and references for generating usable applications.

## Install

```bash
npx skills add https://gitlab.chehejia.com/ai-market/lixiang-skills-marketplace/-/tree/master/packages/idea2web --depth 1 --single-branch
```

## What this skill does

From a short request like:
- "Build me an internal dashboard"
- "Create a small CRUD tool"
- "Generate a simple web app for tracking tasks"

`idea2web` helps produce:
- structured requirement clarification
- architecture planning
- API and file structure design
- full-stack code generation
- deployment/startup guidance

## Default stack

By default, the skill generates a practical full-stack stack such as:
- React (Vite)
- FastAPI
- SQLite
- Tailwind CSS

It can also adapt in specific cases such as Vue or Streamlit-oriented requests.

## Workflow

The skill follows a four-stage workflow:

1. **Requirement clarification**
   - extract entities and operations
   - ask a small number of focused questions
   - produce a structured PRD

2. **Architecture planning**
   - choose the stack
   - design schema and REST API
   - generate API spec and file tree

3. **Code generation**
   - generate the project files directly
   - include backend, frontend, config, and seed data

4. **Delivery**
   - provide startup scripts
   - provide beginner-friendly usage guidance

## Why I built it

I care about making repeated work more structured and reusable. A lot of software ideas die before they become a usable first version. `idea2web` exists to compress that gap and turn vague intent into something buildable.

## Repository contents

This skill includes real implementation assets such as:
- `SKILL.md`
- generation scripts
- config files
- templates
- references
- evals

## Positioning

`idea2web` is best understood as a reusable skill for product-to-build workflows, not just a demo repo.

## Related themes

- reusable skills
- AI workflow systems
- product-to-build automation
- practical full-stack generation
