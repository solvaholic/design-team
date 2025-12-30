# Entry Points

Multiple ways to start and interact with the design thinking workflow system.

## 1. VS Code Chat (/solve)

**Primary workflow interface** - Type `/solve` in Copilot Chat while working in a project.

### New Project
```
User: /solve
DesignTeam: No project found. Let's start one. What problem are you exploring?
User: Our mobile checkout has a 60% abandonment rate
DesignTeam: [creates project structure, initializes currentstate.json]
Great! Now let's identify stakeholders...
```

### Existing Project
```
User: /solve
DesignTeam: Checking current state... You're in Ideate phase with 4 graded ideas.
Next step: Present to LT for prototype approval. Creating playback document...
```

**When to use:** Working locally in VS Code, want interactive conversation, need to see/edit artifacts

## 2. GitHub Issues

**Start new projects remotely** - Create issue with design problem, assign to Copilot.

### Workflow

1. **User creates issue** using "Design Problem" template
   - Fill in project name, problem statement, context
   - Select urgency and starting phase
   - Submit issue

2. **GitHub Actions trigger** (`.github/workflows/design-project-init.yml`)
   - Parses issue body
   - Creates project folder structure
   - Initializes `currentstate.json`
   - Creates branch and pull request
   - Comments on issue with next steps

3. **User continues work** in VS Code or PR
   - Open workspace in VS Code/Codespaces
   - Navigate to project folder
   - Type `/solve` to advance
   - Or interact with @DesignTeam in PR comments

### Example Issue Body
```markdown
**Project Name:** mobile-checkout-redesign

**Problem Statement:** 
Our mobile checkout has 60% cart abandonment. Analytics show users 
drop off at payment method selection. Support tickets mention confusion 
about saved payment options.

**Context:**
- Q2 priority for growth team
- Can't change payment processor (compliance constraints)
- Want to test solutions with 200 users before full rollout

**Urgency:** Standard

**Starting Phase:** ☑ Empathize
```

**When to use:** Starting new projects, want async workflow, collaborating across teams, using Codespaces

## 3. Pull Request Comments

**Continue work on existing projects** - Interact with @DesignTeam in PR.

Once a project PR exists (created via issue workflow or manually):

```
User comment in PR:
@DesignTeam I completed interviews with 5 customers. Notes are in 
insights/interviews-*.md. What's next?

DesignTeam response:
Great! I see 5 interview notes. Let me synthesize the key insights...
[applies insight-synthesis skill, creates research_synthesis.md, 
updates currentstate.json]

I've identified 3 key insights:
1. Users expect payment options to match their banking apps
2. Privacy concerns about storing payment info
3. Time pressure during checkout (mobile context)

Next: Let's grade our assumptions about payment preferences. I'll update 
currentstate.json with certainty/risk scores.
```

**When to use:** Async collaboration, want conversation history visible to team, working in browser

## 4. Spaces (Future)

**Team collaboration hub** - Post design problems to Space, get guided workflow.

_Note: Implementation pending GitHub Spaces integration_

Planned workflow:
1. User posts problem statement to design Space
2. Bot creates project and PR automatically
3. Team discusses in Space, work happens in VS Code
4. Updates posted back to Space thread
5. Leadership reviews playbacks in Space

**When to use:** Cross-functional collaboration, org-wide visibility, async + sync mix

## Comparison Matrix

| Entry Point | Best For | Interaction Style | Visibility |
|-------------|----------|-------------------|------------|
| `/solve` in VS Code | Active development | Synchronous chat | Personal |
| GitHub Issues | Starting projects | Async, structured | Team/public |
| PR Comments | Ongoing work | Async conversation | Team/public |
| Spaces (future) | Collaboration | Mixed sync/async | Org-wide |

## Choosing an Entry Point

**Starting new project remotely?** → GitHub Issue  
**Working locally with files?** → `/solve` in VS Code  
**Collaborating asynchronously?** → PR comments  
**Need org-wide visibility?** → Spaces (when available)

All entry points converge on the same workflow and state management, so you can switch between them as needed.

## Examples

### Example 1: Solo Developer
1. Create issue: "Improve error handling UX"
2. GitHub Actions creates project PR
3. Open Codespace, type `/solve`
4. DesignTeam guides through research
5. Present to @LT in VS Code when ready

### Example 2: Cross-Functional Team
1. Product manager creates issue with problem statement
2. Designer opens workspace, runs `/solve` to conduct research
3. Designer posts synthesis in PR comments
4. Team discusses in PR, @DesignTeam provides facilitation
5. Engineer reviews prototype in PR before building

### Example 3: Leadership Review
1. Team completes Empathize phase
2. Riley (DesignTeam) creates playback document
3. Team presents to @LT via `/solve` or PR comment
4. @LT reviews playback, provides decision
5. Project advances to Define phase

## Integration with Existing Tools

The design workflow integrates with:
- **VS Code** - Primary development environment
- **GitHub** - Version control, PRs, Issues, Actions
- **Copilot Chat** - AI interaction via `/solve` and agents
- **Codespaces** - Remote development environment

No additional tools required. Everything works within GitHub/VS Code ecosystem.
