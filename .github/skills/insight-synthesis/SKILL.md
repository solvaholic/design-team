---
name: insight-synthesis
description: Transform raw research into actionable insights that inform design decisions. Use during Define phase after completing research.
---

# Insight Synthesis

## Overview
Transform raw research data into actionable insights that inform design decisions.

## When to Use
- During Define phase after completing research
- When transitioning from Empathize to Define
- Before ideation to ground solutions in user needs
- When research feels overwhelming or unclear

## How to Apply

### 1. Gather All Research
Collect from `projects/[project_name]/insights/`:
- Observation notes
- Interview transcripts
- Empathy maps
- Survey results
- Stakeholder feedback

### 2. Identify Patterns
Look across research for:
- **Repeated themes** — What comes up multiple times?
- **Behaviors** — What do users consistently do?
- **Pain points** — What frustrates users?
- **Workarounds** — What makeshift solutions exist?
- **Emotional intensity** — What generates strong reactions?
- **Contradictions** — Where do words and actions diverge?

### 3. Synthesize Insights
An insight is NOT just a finding. Transform observations into understanding:

**Observation**: "Users check their work 3-4 times"
**Insight**: "Users lack confidence in the system's accuracy, creating anxiety and inefficiency"

**Observation**: "Users prefer mobile for field work"
**Insight**: "Context switching between devices disrupts workflow because data doesn't sync reliably"

Good insights answer "why" and have implications for design.

### 4. Grade Confidence
For each insight:
- **High**: Multiple sources, consistent pattern, strong evidence
- **Medium**: Some evidence, but limited sample or mixed signals
- **Low**: Hypothesis based on thin evidence, needs validation

### 5. Identify Implications
For each insight, ask:
- What does this mean for our design?
- What opportunities does this create?
- What constraints does this impose?
- What should we prioritize?

### 6. Document
Create synthesis document in `insights/` folder and update currentstate.json:

```json
{
  "id": "i1",
  "title": "Lack of system confidence creates inefficiency",
  "description": "Users check work multiple times due to past system errors, creating anxiety and wasted time",
  "confidence": "high",
  "sources": ["insights/observation_001.md", "insights/interview_003.md"],
  "implications": "Reliability and clear feedback are more important than features"
}
```

## Synthesis Framework

### Pattern → Insight → Implication

**Pattern**: What we observed across multiple sources
**Insight**: Why it happens and what it means
**Implication**: What we should do about it

### Example

**Pattern**: 6 out of 8 field techs use paper notes despite having mobile devices

**Insight**: Mobile interface requires too many steps and focus for field context where attention is divided and conditions are suboptimal (gloves, sunlight, distractions)

**Implication**: Design for quick capture with minimal interaction; offline-first; large touch targets; high contrast for outdoor visibility

## Tips
- Involve the whole DesignTeam (multiple perspectives)
- Focus on why, not just what
- Look for surprising findings, not just confirmations
- One observation may support multiple insights
- Keep insights user-centered, not feature-centered
- Link every insight to source evidence
- Update insights as you learn more
