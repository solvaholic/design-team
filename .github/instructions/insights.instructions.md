---
applyTo: "**/insights/*.md"
---

# Insights Artifacts Instructions

Files in `projects/[project]/insights/` contain research findings from the Empathize and Define phases.

## Types of Insight Files

**Observation notes** — Field observations of stakeholders in their environment  
**Interview notes** — Conversations with stakeholders about needs, behaviors, frustrations  
**Empathy maps** — Structured visualizations of what stakeholders say/think/do/feel  
**Research synthesis** — Pattern analysis and insight extraction across multiple sources

## When Creating Insight Files

Use the templates in `templates/insights/`:
- `observation_template.md` for field observations
- `interview_template.md` for user interviews
- `research_synthesis_template.md` for synthesizing findings

## Key Guidelines

- **Link to currentstate.json**: Observation and interview notes should be linked from stakeholder `notes_links` array
- **Use stakeholder language**: Capture direct quotes, don't paraphrase
- **Document evidence**: What you saw, heard, or measured - not interpretations
- **Tag stakeholders**: Always note which stakeholder group/individual this relates to
- **Date everything**: Include when observation/interview occurred

## Structure

Observation and interview files are **primary data** — what was actually observed or said.

Synthesis files are **derived insights** — patterns and implications you've identified. These should:
- Reference multiple primary sources
- Identify patterns across sources  
- Answer "why" not just "what"
- Include implications for design
- Be indexed in currentstate.json insights array

## DesignTeam Agent (Maya) Responsibilities

When working with insights:
1. Create observation/interview notes as you gather research
2. Link notes from stakeholder profiles in currentstate.json
3. Look for patterns across multiple sources
4. Create synthesis documents that transform observations into insights
5. Grade insight confidence based on evidence strength
6. Update currentstate.json insights array with synthesized findings
