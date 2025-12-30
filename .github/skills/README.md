# Design Skills

Reusable design thinking skills that agents and users apply throughout the design process.

## Overview

Skills are **how-to guides** for specific design activities. They provide structured approaches to common design challenges, ensuring consistent, high-quality work across projects.

## Available Skills

### Research & Empathy

**[empathy-mapping](empathy-mapping/SKILL.md)**  
Create structured visualizations of stakeholder perspectives (says, thinks, does, feels) to build deep understanding.

**When to use**: During Empathize, after observations/interviews, when validating assumptions

---

**[needs-articulation](needs-articulation/SKILL.md)**  
Distinguish user wants from underlying needs to guide solution design.

**When to use**: After research, when users make feature requests, during Define phase

---

### Assumptions

**[assumption-grading](assumption-grading/SKILL.md)**  
Assess assumptions on certainty and risk to prioritize what to validate.

**When to use**: Project start, Define phase, before phase transitions, when deciding what to research

---

**[assumption-validation](assumption-validation/SKILL.md)**  
Test whether assumptions are true before making commitments.

**When to use**: When assumptions have low certainty + high risk, before major resource commitments

---

### Synthesis

**[insight-synthesis](insight-synthesis/SKILL.md)**  
Transform raw research into actionable insights that inform design decisions.

**When to use**: Define phase, after completing research, when research feels overwhelming

---

### Ideation

**[idea-evaluation](idea-evaluation/SKILL.md)**  
Systematically assess ideas on impact and feasibility to prioritize prototyping.

**When to use**: Ideate phase, when deciding which ideas to pursue, when stakeholders ask for prioritization

---

### Validation

**[prototype-planning](prototype-planning/SKILL.md)**  
Define what to build, at what fidelity, to learn what you need without over-investing.

**When to use**: Before any prototype, when transitioning to Prototype phase, when scope is unclear

---

**[playback-preparation](playback-preparation/SKILL.md)**  
Create clear presentations for leadership that communicate findings and enable decisions.

**When to use**: End of each phase, before major commitments, at key decision points

---

## How to Use Skills

### For DesignTeam Agent
Reference skills when guiding the design process:
- "Let me apply the empathy-mapping skill to synthesize these observations"
- "Following the assumption-grading approach, I'll assess our assumptions"
- "Using prototype-planning, I'll define what we should build"

### For Stakeholders Agent
Use relevant skills when appropriate:
- empathy-mapping — Help designers understand your perspective
- assumption-validation — Test assumptions about your stakeholder group
- needs-articulation — Express what you truly need

### For Users
Follow skills when working independently:
1. Read the skill document
2. Follow the step-by-step process
3. Create artifacts in the appropriate project folder
4. Update currentstate.json as needed

## Skill Structure

Each skill follows this format:

**Purpose** — What this skill accomplishes  
**When to Use** — Situations where this skill applies  
**How to Apply** — Step-by-step process  
**Examples** — Concrete illustrations  
**Tips** — Best practices and common pitfalls

## Adding New Skills

As you discover needs for additional skills:

1. **Identify the need**: What activity lacks clear guidance?
2. **Create the skill directory**: `.github/skills/skill-name/` (lowercase, hyphens for spaces)
3. **Create SKILL.md**: Add YAML frontmatter with `name` and `description`
4. **Test it**: Apply it to a real project
5. **Refine it**: Update based on what works
6. **Reference it**: Update agent instructions and README if agents should use it

Skills should be:
- **Actionable**: Clear steps, not just concepts
- **Focused**: One skill, one activity
- **Reusable**: Apply across different projects
- **Practical**: Based on real design work, not theory

### Skill File Format

Each skill must have:
- **Directory**: `.github/skills/[skill-name]/`
- **File**: `SKILL.md` (must be named exactly this)
- **Frontmatter**: YAML with `name` (lowercase, hyphens) and `description` (when to use)

## Philosophy

Skills are:
- **Tools, not rules**: Adapt to context
- **Starting points**: Customize for your needs
- **Shared language**: Common vocabulary across agents and users
- **Living documents**: Update as you learn

---

**Version**: 1.0  
**Last Updated**: 2025-12-29
