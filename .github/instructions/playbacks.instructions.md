---
applyTo: "**/playbacks/*.md"
---

# Playback Artifacts Instructions

Files in `projects/[project]/playbacks/` contain presentations to leadership (LT agent) and their decisions.

## Purpose

Playbacks are **phase gate reviews** where:
- DesignTeam presents findings, insights, or recommendations
- LT evaluates strategic fit, feasibility, and user value
- LT makes go/no-go decisions and sets direction

## When Creating Playback Files

Use the template in `templates/playbacks/playback_template.md`

Create a playback:
- At the end of each design phase (Empathize, Define, Ideate, Prototype, Iterate)
- Before major resource commitments
- When needing strategic direction or approval
- When presenting recommendations to leadership

## Key Guidelines

- **Concise presentation**: 10-15 minutes of content, leadership time is limited
- **Clear decision request**: What specific decision or approval are you asking for?
- **Show evidence**: Use quotes, data, visuals - not just assertions
- **Be honest about confidence**: State certainty levels and remaining assumptions
- **Frame options**: Present alternatives with clear recommendation
- **Document decisions**: Capture what LT decided and rationale
- **Index in currentstate.json**: Record in playbacks array with decisions made

## Structure

**Context** (2 min) — Where we are, what we've done, what we need  
**Key Findings** (5 min) — Top insights/results with supporting evidence  
**Recommendations** (3 min) — What to do next, why, what's needed  
**Decision Needed** (2 min) — Specific ask, options, implications

## Critical Constraint

**LT only sees playback files and high-level currentstate.json metadata.**

They don't have access to:
- Detailed research notes in insights/
- Full idea documents in ideas/
- Raw stakeholder data

This means your playback must be **self-contained and clear** or LT can't make informed decisions.

## DesignTeam Agent (Riley) Responsibilities

When preparing playbacks:
1. Use playback-preparation skill from `.github/skills/`
2. Synthesize key findings (don't overwhelm with detail)
3. Make clear recommendation with rationale
4. Anticipate LT's questions (strategy, resources, risks, confidence)
5. Present to LT agent
6. Document their decisions in the playback file
7. Update currentstate.json with decisions from playbacks array

## LT Agent Behavior

LT will:
- Ask questions about research depth, strategic fit, feasibility
- Challenge assumptions and confidence levels
- Make decisions balancing strategy (Pat), operations (Casey), and user value (Morgan)
- Set expectations and constraints for next steps

Expect tough but fair scrutiny. This is leadership's job.
