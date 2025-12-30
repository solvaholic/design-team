---
applyTo: "**/currentstate.json"
---

# Project State Instructions

`currentstate.json` is the **central index** of a design project's state. It tracks progress through design thinking phases and links to detailed artifacts.

## Structure

The file follows the schema in `schemas/currentstate.schema.json` and contains:

**Metadata**: project_name, created_at, updated_at, phase (empathize|define|ideate|prototype|iterate), description

**Assumptions**: Array of hypotheses with certainty (high|medium|low), risk (high|medium|low), validation_plan, and status

**Stakeholders**: Array of user groups/individuals with needs, pain_points, and notes_links to research files

**Research Plan**: Questions to answer with method, status, and findings_link

**Insights**: Synthesized findings with confidence level, sources, and implications

**Ideas**: Solution concepts with impact (high|medium|low), feasibility (high|medium|low), status, and links to idea documents

**Playbacks**: Record of leadership presentations with decisions made

## When Editing

- **Always update `updated_at` timestamp** when making changes
- **Update `phase`** only after completing phase activities and getting LT approval
- **Link to files** using relative paths from project root (e.g., `insights/observation_001.md`)
- **Grade assumptions and ideas** honestly - low certainty/feasibility is valuable information
- **Keep IDs unique** within each array (a1, a2... for assumptions; s1, s2... for stakeholders, etc.)

## DesignTeam Agent Responsibilities

When working with currentstate.json:
1. Read it first to understand where the project is
2. Update it as the project progresses (don't let it get stale)
3. Ensure all artifacts (insights, ideas) are indexed here
4. Validate structure against the schema before saving

## Common Operations

**Adding an assumption:**
```json
{
  "id": "a3",
  "description": "Field techs need offline access",
  "certainty": "low",
  "risk": "high",
  "validation_plan": "Interview 8 field techs about connectivity",
  "status": "open"
}
```

**Recording an insight:**
```json
{
  "id": "i2",
  "title": "Connectivity disrupts workflow",
  "description": "Users lose data when connection drops, creating anxiety",
  "confidence": "high",
  "sources": ["insights/observation_002.md"],
  "implications": "Offline-first design is critical"
}
```

**Grading an idea:**
```json
{
  "id": "idea2",
  "title": "Quick-capture form",
  "description": "3-field form for fast data entry",
  "impact": "high",
  "feasibility": "high",
  "status": "prototyping",
  "idea_doc_link": "ideas/quick_capture.md"
}
```
