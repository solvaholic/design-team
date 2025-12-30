---
applyTo: "**/ideas/*.md"
---

# Ideas Artifacts Instructions

Files in `projects/[project]/ideas/` contain solution concepts and prototype iterations.

## Types of Idea Files

**Idea documents** (`idea_name.md`) — Solution concept with rationale, benefits, open questions  
**Prototype documents** (`idea_name-###.md`) — Specific prototype iteration with goals, scope, learnings

## When Creating Idea Files

Use the templates in `templates/ideas/`:
- `idea_template.md` for new solution concepts
- `prototype_template.md` for each prototype iteration

## Key Guidelines for Ideas

- **One idea, one file**: Each solution concept gets its own document
- **Link to insights**: Show which insights or stakeholder needs this addresses
- **Grade honestly**: Impact and feasibility ratings should be realistic, not optimistic
- **Document reasoning**: Explain why this idea would work, not just what it is
- **Track status**: Ideated → Prototyping → Iterating → Validated/Invalidated/Implemented
- **Index in currentstate.json**: Every idea should be in the ideas array with link to document

## Key Guidelines for Prototypes

- **Sequential numbering**: idea_name-001.md, idea_name-002.md, etc.
- **State learning goals**: What questions must this prototype answer?
- **Appropriate fidelity**: Match fidelity to learning goals (use lowest that answers questions)
- **Document feedback**: Capture what worked, what didn't, user quotes
- **Synthesize learnings**: Don't just record feedback - extract what it means
- **Link from idea doc**: Parent idea document should link to all prototype iterations

## DesignTeam Agent Responsibilities

**Alex (Ideate phase)**:
- Create idea documents as concepts emerge
- Grade ideas for impact and feasibility  
- Document why each idea would address user needs
- Update currentstate.json ideas array

**Sam (Prototype phase)**:
- Create prototype documents with clear learning goals
- Define appropriate fidelity and scope
- Plan iteration with stakeholders

**Maya + Sam (Iterate phase)**:
- Document user feedback in prototype files
- Synthesize what was validated/invalidated
- Update idea status in currentstate.json based on findings
- Decide whether to refine, pivot, or proceed

## Example Progression

1. `quick_capture.md` — Idea doc: 3-field form concept, graded high impact/high feasibility
2. `quick_capture-001.md` — Low-fi prototype: paper sketches, test with 5 users
3. `quick_capture-002.md` — Medium-fi prototype: clickable mockup with refined flow
4. `quick_capture-003.md` — High-fi prototype: working code, performance testing
