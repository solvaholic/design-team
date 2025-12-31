# Design Team

An AI-powered design thinking workflow system that guides projects through structured research, ideation, and validation.

## What is this?

Design Team helps you solve problems systematically using design thinking principles. Instead of jumping straight to solutions, you'll:

1. **Empathize** - Understand users and their needs through research
2. **Define** - Synthesize insights and validate assumptions  
3. **Ideate** - Generate and evaluate solution concepts
4. **Prototype** - Build and test ideas with users
5. **Iterate** - Refine based on feedback

The system uses AI agents (powered by GitHub Copilot) to guide you through each phase, maintain structured state, and coordinate with stakeholders and leadership.

## Try it out

**In VS Code:**

1. Open this workspace
2. Type `/solve` in Copilot Chat
3. Describe a problem you're exploring
4. The DesignTeam will guide you through the process

**Via GitHub Issue:**

1. Create a new issue using the "Design Problem" template
2. Assign it to @copilot
3. A project folder and PR will be created automatically
4. Continue work in VS Code or PR comments

## How it works

- **Three AI Agents**: @DesignTeam (five designers), @Stakeholders (user personas), @LT (leadership)
- **Structured State**: Every project has `currentstate.json` tracking progress, insights, ideas, and decisions
- **Design Skills**: Reusable methods like empathy mapping, assumption grading, insight synthesis
- **One Command**: Type `/solve` to check state, identify gaps, and advance to the next step

## What you'll create

Each project produces:
- Research artifacts (observations, interviews, synthesis)
- Graded assumptions (certainty/risk assessment)
- Evaluated ideas (impact/feasibility matrix)
- Prototype iterations with user feedback
- Leadership presentations with go/no-go decisions

All stored as markdown and JSON in Git, versioned and collaborative.

## Documentation

- [Data Structures](docs/DATA_STRUCTURES.md) - Schema and templates
- [Agent System](.github/agents/README.md) - How agents work together
- [Skills Framework](.github/skills/README.md) - Design methods and techniques
- [Workflow Orchestration](docs/WORKFLOW.md) - The reflect-make-observe loop
- [Entry Points](docs/ENTRY_POINTS.md) - Ways to interact with the system
- [Integration Layer](docs/INTEGRATION.md) - How it all connects
- [Git Workflow](docs/GIT_WORKFLOW.md) - Managing projects in version control

## Status

🚧 **Experimental** - This system is newly built and untested. Expect rough edges, missing features, and evolving patterns.

Feedback welcome! Create an issue or start a discussion.

## Requirements

- VS Code with GitHub Copilot
- Python 3.11+ (for helper scripts)

---

*Built with GitHub Copilot, designed for design thinking.*
