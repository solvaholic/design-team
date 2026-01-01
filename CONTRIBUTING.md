# Contributing to Design Team

This repository demonstrates GitHub Copilot's custom instructions, skills, and agents features in a complete design thinking workflow system.

## How This Repository Uses Copilot Features

### Repository Instructions
[.github/copilot-instructions.md](.github/copilot-instructions.md) provides global context about the design system structure, agents, and workflows.

### Path-Specific Instructions
[.github/instructions/](.github/instructions/) contains rules for working with specific file types:
- `agents.instructions.md` - Creating/editing agent personas
- `currentstate.instructions.md` - Updating project state
- `ideas.instructions.md` - Documenting solution concepts
- `insights.instructions.md` - Recording research findings
- `playbacks.instructions.md` - Preparing leadership presentations
- `skills.instructions.md` - Defining reusable methods

### Agent Skills
[.github/skills/](.github/skills/) provides reusable design methods:
- `empathy-mapping` - Understanding stakeholder perspectives
- `assumption-grading` - Prioritizing validation efforts
- `idea-evaluation` - Assessing solution concepts
- And 5 more specialized skills

### Custom Agents
[.github/agents/](.github/agents/) defines three collaborative AI personas:
- `@DesignTeam` - Five designers guiding the process
- `@Stakeholders` - User representatives providing feedback
- `@LT` - Leadership making strategic decisions

## Extending the System

### Adding a New Skill

1. Create a directory in `.github/skills/` named after the skill
2. Add a `SKILL.md` file following [skills.instructions.md](.github/instructions/skills.instructions.md)
3. Include: purpose, when to use, step-by-step process, examples
4. Update [.github/skills/README.md](.github/skills/README.md) with a summary
5. Reference it in [.github/copilot-instructions.md](.github/copilot-instructions.md)

**Key principles for skills:**
- Keep focused on one specific activity
- Provide clear decision criteria
- Include concrete examples
- Make it reusable across projects

### Adding Path-Specific Instructions

1. Create `[pattern].instructions.md` in `.github/instructions/`
2. Define clear rules using "always" and "never" language
3. Keep under 2 pages - be concise and task-focused
4. Document commands and workflows that actually work
5. Add to `.github/instructions/` directory

The system automatically applies instructions based on file patterns defined in instruction file headers.

### Creating a New Agent

1. Create `[name].agent.md` in `.github/agents/`
2. Follow the structure in [agents.instructions.md](.github/instructions/agents.instructions.md)
3. Define persona, capabilities, and context access
4. Add to [.github/agents/README.md](.github/agents/README.md)
5. Configure in `.vscode/settings.json` if needed

**Agent design principles:**
- Give each agent a specific role and perspective
- Define what context they can access
- Establish clear boundaries between agents
- Make personas consistent and memorable

### Updating Project Templates

Templates in `templates/` provide starting structures:
- `project/` - New project scaffolding
- `insights/` - Research artifact templates
- `ideas/` - Solution documentation templates
- `playbacks/` - Leadership presentation templates

When improving templates:
- Test with real projects first
- Keep placeholders clearly marked
- Include helpful comments and examples
- Update corresponding scripts if structure changes

## Best Practices

### Instruction Priority

When multiple instructions apply, they combine in this order:
1. Personal instructions (user-level, highest priority)
2. Repository instructions (this file and path-specific)
3. Organization instructions (lowest priority)

Avoid conflicts - make instructions complementary.

### Writing Effective Instructions

- **Be explicit**: Use "always" and "never" for clarity
- **Be searchable**: Use terms that match what people look for
- **Be concise**: Target 1-2 pages maximum
- **Be testable**: Include examples of correct behavior
- **Version everything**: All instructions live in Git

### Testing Changes

Before committing instruction/skill/agent changes:
1. Test with an example project
2. Verify agents can access needed context
3. Check that instructions don't conflict
4. Update documentation to reflect changes
5. Run helper scripts to validate structure:
   ```bash
   python3 scripts/validate_state.py --project test-project
   ```

## Python Helper Scripts

Scripts in `scripts/` support the workflow:
- `validate_state.py` - Check project structure and completeness
- `check_completion.py` - Evaluate phase readiness
- `find_similar.py` - Search for related projects
- `scaffold_artifact.py` - Create from templates

When modifying scripts:
- Accept project names without `projects/` prefix
- Maintain backward compatibility
- Update documentation in [docs/WORKFLOW.md](docs/WORKFLOW.md)
- Test with both short names and full paths

## Documentation

- **Official Copilot Docs**:
  - [Custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
  - [Path-specific instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions#creating-path-specific-custom-instructions-1)
  - [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
  - [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

- **Project-Specific**:
  - [README.md](README.md) - Project overview and quick start
  - [docs/WORKFLOW.md](docs/WORKFLOW.md) - Detailed workflow orchestration
  - [docs/DATA_STRUCTURES.md](docs/DATA_STRUCTURES.md) - Schema and state management
  - [docs/ENTRY_POINTS.md](docs/ENTRY_POINTS.md) - Ways to interact with the system

## Questions?

- Check existing documentation first
- Look at similar implementations in the repository
- Test in a test project before modifying shared components
- Create an issue for feature requests or bugs

---

*This repository serves as both a working design system and a reference implementation of GitHub Copilot's extensibility features.*
