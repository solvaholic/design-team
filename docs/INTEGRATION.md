# Integration Layer

The integration layer connects AI agents (DesignTeam, Stakeholders, LT) to the design thinking workflow using GitHub Copilot's custom instructions system.

## Architecture

```
.github/
  copilot-instructions.md          → Repository-wide context
  instructions/
    currentstate.instructions.md   → Working with project state
    insights.instructions.md       → Creating research artifacts
    ideas.instructions.md          → Developing solutions
    playbacks.instructions.md      → Leadership presentations
  agents/
    design-team.agent.md           → Five-person design team
    stakeholders.agent.md          → User representatives
    lt.agent.md                    → Leadership decision-makers
  skills/
    empathy-mapping/SKILL.md       → Research techniques
    needs-articulation/SKILL.md    → User needs extraction
    assumption-grading/SKILL.md    → Risk assessment
    ... (8 skills total)
```

## How It Works

### 1. Repository-Wide Instructions

[.github/copilot-instructions.md](.github/copilot-instructions.md) provides baseline context:
- Repository structure and purpose
- Available agents and their roles
- Design thinking phases
- Skills framework overview
- General guidance

This is loaded for **all** files in the workspace.

### 2. Path-Specific Instructions

When working with specific file patterns, additional context is injected:

| Pattern | Instructions | Purpose |
|---------|-------------|---------|
| `**/currentstate.json` | [currentstate.instructions.md](.github/instructions/currentstate.instructions.md) | Structure, grading scales, common operations |
| `**/insights/*.md` | [insights.instructions.md](.github/instructions/insights.instructions.md) | Research documentation guidelines |
| `**/ideas/*.md` | [ideas.instructions.md](.github/instructions/ideas.instructions.md) | Solution concepts and prototypes |
| `**/playbacks/*.md` | [playbacks.instructions.md](.github/instructions/playbacks.instructions.md) | Leadership presentations |

### 3. Agent System

Agents are invoked with `@AgentName` in GitHub Copilot Chat:

**@DesignTeam** — Five designers guiding the process
- Maya: Empathy and research (Empathize, Define)
- Jordan: Systems thinking (Define)
- Alex: Creative ideation (Ideate)
- Sam: Prototyping and building (Prototype)
- Riley: Facilitation and synthesis (all phases, playbacks)

**@Stakeholders** — User personas providing feedback
- Adapts to stakeholder definitions in currentstate.json
- Only sees their own profile and relevant artifacts
- Provides authentic user perspective during research and validation

**@LT** — Leadership making strategic decisions
- Pat: Product strategy
- Casey: Operations and feasibility
- Morgan: User value advocacy
- Only sees playbacks and high-level state
- Makes go/no-go decisions at phase gates

### 4. Skills Framework

Agents apply skills from `.github/skills/` as needed:
- **empathy-mapping** — Says/thinks/does/feels structured observation
- **needs-articulation** — Distinguishing wants from underlying needs
- **assumption-grading** — Certainty and risk assessment
- **assumption-validation** — Testing high-risk assumptions
- **insight-synthesis** — Transforming observations into actionable insights
- **idea-evaluation** — Impact/feasibility grading
- **prototype-planning** — Fidelity and scope decisions
- **playback-preparation** — Leadership presentations

## Usage Patterns

### Starting a New Project

```
1. User: "Create a new project for improving our onboarding flow"
2. @DesignTeam: Creates project structure, initializes currentstate.json
3. @DesignTeam (Maya): Guides user through stakeholder identification
4. @Stakeholders: Provides perspective on pain points and needs
```

### Conducting Research

```
1. User works in insights/ folder creating observations
2. Path-specific instructions guide artifact structure
3. @DesignTeam (Maya) applies empathy-mapping skill
4. Updates currentstate.json with synthesized insights
```

### Reviewing with Leadership

```
1. @DesignTeam (Riley) creates playback in playbacks/
2. Path-specific instructions guide presentation structure
3. User invokes @LT to review
4. @LT sees only playback content, makes decisions
5. @DesignTeam updates currentstate.json with decisions
```

## Context Boundaries

Agents have intentionally restricted access:

**LT Agent**:
- ✅ Can see: playbacks/, high-level currentstate.json (phase, assumptions count, decisions)
- ❌ Cannot see: Detailed insights/, ideas/, stakeholder profiles

**Stakeholders Agent**:
- ✅ Can see: Their own stakeholder profile, artifacts they've been shown
- ❌ Cannot see: Other stakeholders, design team discussions, internal deliberations

**DesignTeam Agent**:
- ✅ Can see: Everything in the project
- Responsibility: Synthesize and present appropriately to other agents

This mirrors real organizational dynamics and prevents information overload.

## Troubleshooting

**Problem**: Agent doesn't seem to have necessary context  
**Solution**: Check that you're in the correct file type (path-specific instructions may not be loaded). Explicitly reference currentstate.json or relevant artifacts.

**Problem**: LT agent asking for details not in playback  
**Solution**: This is correct behavior - LT only sees playbacks. DesignTeam should provide necessary context in the playback document itself.

**Problem**: Agent behavior doesn't match persona  
**Solution**: Check `.github/agents/[name].agent.md` for current instructions. File may have been edited.

**Problem**: Skill not being applied correctly  
**Solution**: Review `.github/skills/[name]/SKILL.md` for proper usage. Skills are guidance, not strict procedures.

## Configuration Files

**.vscode/settings.json** — VS Code workspace settings
- Python analysis mode
- File associations for custom extensions
- GitHub Copilot configuration

## Future Enhancements

Once workflow orchestration (Step 5) is implemented:
- Automated phase transitions based on completion criteria
- Proactive agent suggestions during work
- State consistency validation
- Automated playback scheduling

Once entry points (Step 6) are implemented:
- Start projects from GitHub issues
- Post updates to Spaces
- Invoke agents from VS Code chat or command palette
