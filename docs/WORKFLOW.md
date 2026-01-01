# Workflow Orchestration

The design thinking workflow is orchestrated through a single prompt file `/solve` that analyzes project state and advances through phases systematically.

## The /solve Command

Type `/solve` in VS Code Copilot Chat to:
- Check current project state
- Identify what's missing or incomplete
- Execute the next logical step
- Update project state
- Communicate progress

The prompt invokes the `@DesignTeam` agent, which coordinates the appropriate team members (Maya, Jordan, Alex, Sam, Riley) based on the current phase and needs.

## Reflect-Make-Observe Loop

Each invocation of `/solve` follows this pattern:

### 1. Reflect
- Read `currentstate.json` to understand phase and progress
- Run `validate_state.py` to identify structural gaps
- Run `check_completion.py` to evaluate phase readiness
- Analyze what's missing based on design phase

### 2. Make
- Execute the next step based on gaps identified:
  - **Empathize**: Guide stakeholder definition, facilitate research
  - **Define**: Synthesize insights, grade assumptions
  - **Ideate**: Generate ideas, evaluate impact/feasibility
  - **Prototype**: Plan fidelity, build artifacts
  - **Iterate**: Collect feedback, refine solutions
- Coordinate agents (@DesignTeam, @Stakeholders, @LT)
- Apply relevant skills from `.github/skills/`
- Create or update artifacts

### 3. Observe
- Update `currentstate.json` with new information
- Link artifacts to state (insights, ideas, playbacks)
- Grade assumptions and ideas
- Document decisions and learnings

## Phase Progression

Projects move through phases with leadership gates:

```
Empathize → [playback] → Define → [playback] → Ideate → 
[playback] → Prototype → [playback] → Iterate → [playback] → Done
```

At each playback gate:
1. Riley prepares presentation using playback-preparation skill
2. Creates playback document in `playbacks/`
3. Presents to @LT agent
4. LT makes go/no-go/pivot decision
5. State updated with decision and next phase

## Helper Scripts

Python utilities support the workflow:

**validate_state.py** - Check schema compliance and identify gaps
```bash
python3 scripts/validate_state.py --project my-project
```

**check_completion.py** - Evaluate phase completion criteria
```bash
python3 scripts/check_completion.py --project my-project --phase empathize
```

**find_similar.py** - Search for overlapping projects
```bash
python3 scripts/find_similar.py --project my-project --threshold 0.3
```

**scaffold_artifact.py** - Create new artifacts from templates
```bash
# New project
python3 scripts/scaffold_artifact.py --type project --name my-project --problem "..."

# New insight
python3 scripts/scaffold_artifact.py --type insight --name user-observation --project my-project --insight-type observation

# New idea
python3 scripts/scaffold_artifact.py --type idea --name quick-capture --project my-project

# New prototype
python3 scripts/scaffold_artifact.py --type prototype --name quick-capture --project my-project --iteration 1

# New playback
python3 scripts/scaffold_artifact.py --type playback --name empathize-complete --project my-project
```

## Continuous Progress

The `/solve` prompt assumes **you want to make progress**. It won't ask permission for routine tasks - it will:
- Create missing artifacts
- Update state automatically
- Coordinate with other agents
- Apply appropriate skills

It only stops to ask when:
- Critical decisions are needed
- Leadership approval required
- User input necessary (names, priorities, etc.)

This keeps momentum and reduces friction.

## Usage Patterns

### Starting Work
```
User: /solve
DesignTeam: Checking project state... Found stakeholders defined but no research notes. 
Let me guide you through an observation exercise using empathy-mapping skill.
```

### Mid-Phase Work
```
User: /solve
DesignTeam: I see we have 5 observation notes but no synthesis yet. I'll apply the 
insight-synthesis skill to identify patterns... [creates synthesis document, updates 
currentstate.json with 3 insights]
```

### Phase Gates
```
User: /solve
DesignTeam: Empathize phase completion criteria met. Riley is preparing the playback 
for LT... [creates playback document] Ready to present to @LT for approval to advance 
to Define phase.
```

### Stuck or Uncertain
```
User: /solve
DesignTeam: I checked for similar projects using find_similar.py and found 2 related 
efforts. Should we coordinate with those teams or continue independently?
```

## Automation Opportunities

Future enhancements could add:
- File watcher that triggers `/solve` when artifacts are saved
- Scheduled checks (daily standup: "here's what needs attention")
- Slack/Teams integration posting progress updates
- Automatic duplicate detection on project creation

For now, manual invocation via `/solve` keeps control with the user while still providing systematic guidance.
